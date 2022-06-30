#!/usr/bin/env python3

import urllib.request
import json
import time

# APIのBase Pathを設定
BASE_PATH = 'https://public.api.aibo.com/v1'

# ポーリング間隔（秒）
POLLING_INTERVAL = 1


# トークンの取得
def aibo_get_token(client_id, client_secret, code):
    post_url = BASE_PATH + '/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded' }
    data = 'client_id=' + client_id + '&' + 'client_secret=' + client_secret + '&' + 'grant_type=authorization_code' + '&' + 'code=' + code

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
    return body


# トークンの更新
def aibo_update_token(client_id, client_secret, refresh_token):
    post_url = BASE_PATH + '/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded' }
    data = 'client_id=' + client_id + '&' + 'client_secret=' + client_secret + '&' + 'grant_type=refresh_token' + '&' + 'refresh_token=' + refresh_token

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
    return body


# DeviceIDの取得
def aibo_get_device(access_token):
    get_url = BASE_PATH + '/devices'
    headers = {'Authorization': 'Bearer ' + access_token}

    # GET API
    req = urllib.request.Request(get_url)
    req.headers = headers
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
    return body


# aiboのWeb API実行
def aibo_control(access_token, deviceId, api_name, arguments):
    post_url = BASE_PATH + '/devices/' + deviceId + '/capabilities/' + api_name + '/execute'
    headers = {'Authorization': 'Bearer ' + access_token}
    data = '{"arguments":' + arguments + '}'

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
    return body


# aiboのWeb API実行結果の取得
def aibo_get_execution(access_token, executionId):
    get_url = BASE_PATH + '/executions/' + executionId
    headers = {'Authorization': 'Bearer ' + access_token}
    # GET API
    req = urllib.request.Request(get_url)
    req.headers = headers
    with urllib.request.urlopen(req) as res:
        body = res.read()
        body = body.decode()
        body = json.loads(body)
    if body['status'] == 'FAILED':
        print(body['result'])
    return body


# aiboのWeb API実行(実行完了までWaitし、結果取得を行う)
def aibo_control_sync(access_token, deviceId, api_name, arguments):
    post_url = BASE_PATH + '/devices/' + deviceId + '/capabilities/' + api_name + '/execute'
    headers = {'Authorization': 'Bearer ' + access_token}
    data = '{"arguments":' + arguments + '}'

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        body = body.decode()
        body = json.loads(body)
        print(body)

    # 実行結果の取得
    execution_status = 'ACCEPTED'
    while execution_status == 'ACCEPTED' or execution_status == 'IN_PROGRESS':
        execution_status = aibo_get_execution(access_token, body['executionId'])
        execution_status = execution_status['status']
        print(execution_status)
        time.sleep(POLLING_INTERVAL)
    if execution_status == 'SUCCEEDED':
        return True
    else:
        return False


# aiboのCognition API実行・結果取得(実行完了までWaitし、結果取得を行う)
def aibo_cognition_sync(access_token, deviceId, api_name):
    post_url = BASE_PATH + '/devices/' + deviceId + '/capabilities/' + api_name + '/execute'
    headers = {'Authorization': 'Bearer ' + access_token}
    data = '{}'

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        body = body.decode()
        body = json.loads(body)
        print(body)

    # 実行結果の取得
    execution_status = 'ACCEPTED'
    while execution_status == 'ACCEPTED' or execution_status == 'IN_PROGRESS':
        execution_status = aibo_get_execution(access_token, body['executionId'])
        print(execution_status['status'])
        time.sleep(POLLING_INTERVAL)
    if execution_status['status'] == 'SUCCEEDED':
        return execution_status['result']
    else:
        return False
