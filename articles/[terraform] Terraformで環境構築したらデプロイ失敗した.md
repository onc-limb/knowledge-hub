やろうとしたこと

- ECRのリポジトリ作成
- ECS-fargateのクラスター作成
- CloudFront作成
- ACMで証明書作成

ドキュメントを見ながらこれらをTerraformで記載して、問題なく`terraform apply`を、と思ったらなんとエラーが。

調べてみると

> InvalidViewerCertificate: The specified SSL certificate doesn't exist, isn't in us-east-1 region, isn't valid, or doesn't include a valid certificate chain.

有効な証明書がないとのこと。

あれ？ACMはちゃんと作成するように書いたよな？

マネコンを見に行くと「検証保留中」の記載が、、、時間がかかってるだけ？それとも。。

あ、DNSの設定をしていない！

ということでRoute53でACMの証明書をチェックするためのCNAMEレコードをDNSに登録していなかったことが原因で検証ができていなかった。

わかってしまえば単純なことだが、デプロイできると思ってたものが失敗した時の気持ちたるや、焦りがすごい。

name resolveなどDNS周りはちゃんと勉強しなければなーと思った。
