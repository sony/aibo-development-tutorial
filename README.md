<h1 align="center">
    <br>
    <img width="400" src="https://developer.aibo.com/images/pink.png" alt="">
    <br>
</h1>

aiboの連携アプリ 開発チュートリアル 
=================

## このドキュメントについて

このドキュメントでは、aiboの連携アプリの開発をはじめる方に向けて、連携アプリの例 （以下、サンプルアプリ） を紹介しています。

## aiboの連携アプリとは

aiboの連携アプリとは、公開されている aibo の API を用いて開発できるアプリケーションです。[API のドキュメント](https://developer.aibo.com/jp/docs#aibo-web-api-%E3%81%A8%E3%81%AF)にあるように、aiboに様々な動作を実行させたり、aibo から通知を受け取ったりすることができます。

ベーシックプランに加入している aibo をお持ちの方ならどなたでも、aiboの連携アプリを開発またはご利用いただけます。

詳しくは [aiboの連携アプリについて (日本)](https://aibo.sony.jp/developer/linkable-app/) をご覧ください。
## サンプルアプリ
***
### [気分屋aibo](./sample/sample1/README_python_ja.md)

#### 内容 

* aiboに「おはよう」と言うと、aiboの気分に応じてさまざなふるまいを実行してくれるアプリを作ります。
* 連携アプリを使用するaiboオーナーとaiboを連携させる仕組みを[Google Cloud Platform](https://cloud.google.com/)を使って構築します。

#### 学べること

* aibo Action API、Events APIを使った連携アプリの開発
* Google Cloud Platformを使った開発方法

#### 難易度 
このサンプルアプリは、プログラミング初心者に向けて書かれています。
下記のような経験がある方を想定しています。

- Webサイトを作ったことがある。
- プログラミングについてわからないことがあれば自分で調べることができる。

#### 開発環境

* コードエディタ (Microsoft Visual Studio Codeなど)
* Google Cloud Platform
* 使用するプログラミング言語: Python 3

#### さっそくはじめよう
[気分屋aiboの開発をはじめる](./sample/sample1/README_python_ja.md)
***

## 連携アプリの開発について 

aibo の API を利用するには aibo デベロッパープログラムの規約に同意する必要があります。詳しくは [aibo デベロッパーサイト (日本)](https://developer.aibo.com/jp/) をご覧ください。

上記のaibo デベロッパーサイト では、aibo Web APIやEvents API、aiboの連携アプリに関するドキュメントを参照できます。また連携アプリの開発で必要になる情報の設定や、掲載申請などをすることができます。他にも、現在公開されている連携アプリの一覧を見ることもできます。

### :warning: 注意

* AWS や GCP などの特定のサービスのご利用を推奨するものではありません。
* クラウドサービスをご利用になる場合、利用方法によってはクラウド使用料が有料になる場合があります。
使用料の上限を設定するなど、利用方法をご確認の上自己責任でご利用ください。
* このリポジトリではコントリビューションやバグレポートを受け付けていません。Issue はオフになっています。
* 開発者同士のコミュニティとして [Stack Overflow](https://ja.stackoverflow.com/questions/tagged/aibo-developer) での `aibo-developer` タグをご利用ください。