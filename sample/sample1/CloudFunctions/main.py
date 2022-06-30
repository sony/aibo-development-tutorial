#!/usr/bin/env python3

import json
import aibo_api_ctrl
import datetime
import random
from google.cloud import firestore

# 連携アプリの情報
CLIENT_ID = 'クライアントIDを入力'
CLIENT_SECRET = 'クライアントシークレットを入力'

# DB名（Google Firestoreのコレクション名）
DB_NAME = 'aibo_sample_devices'


# アプリケーション（aiboにやってもらいたいことを書く）
def aibo_app(access_token, device_id, eventId):
    # 「おはよう」と言われたとき
    if eventId == 'voice_command::goodmorning':
        # aiboの気分を0から2の整数でランダムに設定
        kibun = random.randint(0, 2)

        # 気分に応じてふるまいを実行
        if kibun == 0:
            print("とっても喜ぶ")
            res = aibo_api_ctrl.aibo_control_sync(access_token, device_id, 'play_motion', '{"Category":"overJoyed","Mode":"NONE"}') # とっても喜ぶ
        elif kibun == 1:
            print("顔を洗う仕草をする")
            res = aibo_api_ctrl.aibo_control_sync(access_token, device_id, 'play_motion', '{"Category":"washFace","Mode":"NONE"}') # 顔を洗う仕草をする
        else:
            print("ブルッと震える")
            res = aibo_api_ctrl.aibo_control_sync(access_token, device_id, 'play_motion', '{"Category":"jiggle","Mode":"NONE"}') # ブルッと震える
        return res
    else:
        return True


# アプリケーションの実行（aiboからのイベント通知を受けた時の処理）
def aibo_api_execute(request_json):
    # イベントIDの取得
    eventId = request_json['eventId']

    # DeviceIdの取得
    deviceId = request_json['deviceId']

    # aibo情報の検索
    db = firestore.Client()
    doc_ref = db.collection(DB_NAME).document(deviceId)
    doc = doc_ref.get()
    if doc.exists:
        aibo_info = doc.to_dict()
        print(aibo_info)
    else:
        # 未登録のaiboの場合の例外処理
        print('aiboが登録されていません')
        # 406 Not Acceptable のレスポンス
        headers = {
        }
        return ('Not Acceptable', 406, headers)

    # 一旦トークンをデータベースからロード
    access_token = aibo_info['access_token']

    # トークン情報検証のための準備
    expires_in = int(aibo_info['expires_in'])  # トークンの有効期限
    date_last_update = datetime.datetime.strptime(aibo_info['update_date'], '%Y-%m-%d %H:%M:%S') # トークンの取得日
    date_now = datetime.datetime.now()  # 現在日時の取得

    # トークンが有効期限切れでないかを検証する（1分の余裕を持って計算）
    expire_delta = date_now - date_last_update  # 最終アップデート日時からの差分
    if expire_delta.seconds > (expires_in - 60):
        print("トークン期限切れ")
        # トークンの再取得
        response_token = aibo_api_ctrl.aibo_update_token(CLIENT_ID, CLIENT_SECRET, aibo_info['refresh_token'])
        response_token = response_token.decode()
        response_token = json.loads(response_token)
        # トークンのアップデート(DBを更新)
        doc_ref.set({
            'device_id': deviceId,
            'access_token': response_token['access_token'],
            'refresh_token': response_token['refresh_token'],
            'expires_in': response_token['expires_in'],
            'update_date': date_now.strftime('%Y-%m-%d %H:%M:%S')
        })
        access_token = response_token['access_token']

    # リフレッシュトークンの有効期限切れ時の処理は省略

    # アプリケーションを実行
    res = aibo_app(access_token, deviceId, eventId)
    return res


# 連携処理の実行（フロントエンドから認可コードを受けた時の処理）
def aibo_oauth_execute(request_json):
    # トークンの取得
    response_token = aibo_api_ctrl.aibo_get_token(CLIENT_ID, CLIENT_SECRET, request_json['code'])
    response_token = response_token.decode()
    response_token = json.loads(response_token)
    print(response_token)

    # DeviceIDの取得
    response_device = aibo_api_ctrl.aibo_get_device(response_token['access_token'])
    response_device = response_device.decode()
    response_device = json.loads(response_device)

    # 日時の取得
    date = datetime.datetime.now()
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    print(date)

    # DeviceをDBに登録
    db = firestore.Client()
    for aibo_cnt in response_device['devices']:
        doc_ref = db.collection(DB_NAME).document(aibo_cnt['deviceId'])
        doc_ref.set({
            'device_id': aibo_cnt['deviceId'],
            'access_token': response_token['access_token'],
            'refresh_token': response_token['refresh_token'],
            'expires_in': response_token['expires_in'],
            'update_date': date
        })
    return True


# メインの処理
def hello_world(request):
    # Set CORS headers for preflight requests（CORS対応：プリフライト）
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # リクエスト情報の取得
    request_json = request.get_json()
    print(request_json)

    # エンドポイントの検証
    if 'eventId' in request_json and request_json['eventId'] == 'endpoint_verification':
        print("エンドポイントの検証")
        return request_json

    # aibo APIの実行
    if 'eventId' in request_json:
        print("aibo APIの実行")
        res = aibo_api_execute(request_json)
        # レスポンス
        if res:
            headers = {
            }
            return ('Sucess!', 200, headers)
        else:
            headers = {
            }
            return ('Failed', 500, headers)

    # OAuth認証
    if 'code' in request_json:
        print("連携処理の実行")
        aibo_oauth_execute(request_json)
        # レスポンス（CORS有効）
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': '*',
        }
        return ('Sucess!', 200, headers)

    # 例外時のレスポンス(404を返す)
    print("例外発生")
    headers = {
    }
    return ('Not Found', 404, headers)