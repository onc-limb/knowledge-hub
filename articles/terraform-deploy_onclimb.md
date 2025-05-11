---
title: Terraformで環境構築したらデプロイ失敗した
emoji: 📝
type: tech
topics:
  - terraform
  - aws
published: true
---
## はじめに
こんにちは、onclimbです。
普段はWebのバックエンドエンジニアをしていますが、最近AWSを触るようになりました。
Terraformを使用してコード管理しながらインフラリソースを構築しようとした時の失敗と解消方法を記載します。

## やろうとしたこと

- ECR のリポジトリ作成
- ECS-fargate のクラスター作成
- CloudFront 作成
- ACM で証明書作成

## 失敗
ドキュメントを見ながらこれらを Terraform で記載して、問題なく`terraform apply`を、と思ったらなんとエラーが。

調べてみると

> InvalidViewerCertificate: The specified SSL certificate doesn't exist, isn't in us-east-1 region, isn't valid, or doesn't include a valid certificate chain.

有効な証明書がないとのこと。

あれ？ACM はちゃんと作成するように書いたよな？

マネコンを見に行くと「検証保留中」の記載が、、、時間がかかってるだけ？それとも。。

あ、DNS の設定をしていない！

ということで Route53 で ACM の証明書をチェックするための CNAME レコードを DNS に登録していなかったことが原因で検証ができていなかったらしい。

Route53にACMの証明書のCNAMEを登録したのち、改めて`terraform apply`を実行したら構築できました。

## 結論
わかってしまえば単純なことだが、デプロイできると思ってたものが失敗した時の気持ちたるや、焦りがすごい。

name resolve など DNS 周りはちゃんと勉強しなければなーと思いました。
