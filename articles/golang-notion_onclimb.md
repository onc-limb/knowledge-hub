---
title: NotionAPIを利用してブログ記事を入稿する
emoji: ""
type: tech
topics:
  - golang
  - notion
published: true
---

## はじめに
こんにちは、onclimbです。
私は自分の考えや、書籍や記事で得た知識をNotionに書き留めています。

Notion に記載した内容をそのままアプリケーションに取り込むことはできないのか？と考え、その方法を探していると、
Notion API というものがあるではないですか！ということで早速使ってみました。

## Notion API とは

Notion API は API を叩くことで Notion 上のページやデータベースにアクセスし、データの取得、挿入、更新などが可能なものです。
詳しい内容は分かりやすくまとめている方がいっぱいいるのでここでは割愛します。
とりあえず、個人で利用する分には Notion 同様無料で使用可能です！

## 導入手順

### 前提

Notion のアカウントは作成済み
API を叩くアプリケーションは go 言語で実装
API の使用ケースはページの取得のみ

### API Key の取得

Notion API を取得するにはインテグレーションを作成する必要がある。
インテグレーションを作成したら、integration secret を記録しておく ← これが API Key
インテグレーションの作成は以下の URL から可能です。

[https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

### 環境変数に API Key を設定

.env に API Key を設定する

```go
// .env
NOTION_API_KEY="***********"
```

※本番環境等ではインフラ構成に従って環境変数に設定すること

### NotionAPI ライブラリを取得

NotionAPI を Go 言語で扱うためのライブラリとして今回は notionapi([https://github.com/jomei/notionapi](https://github.com/jomei/notionapi))を利用しました。

```bash
go get github.com/jomei/notionapi
```

このライブラリの使用方法は簡単で、

- API Key を指定して Client インスタンスを作成する。
- 操作対象を database、page、block から選択して、関数を呼ぶ

これだけです！

Client インスタンスの作成

```go
func NewClient() (client *NotionClient) {
	apiKey := os.Getenv("NOTION_API_KEY")
	return &NotionClient{
		client: notionapi.NewClient(notionapi.Token(apiKey)),
	}
}
```

page 情報の取得

```go
func (nc NotionClient) GetPage(pageId string) (*notionapi.Page, error) {
	return nc.client.Page.Get(context.Background(), notionapi.PageID(pageId))
}
```

どんな情報が取得できるかは Notion API の公式リファレンスを確認するのが良いかと思います！

## 最後に

これで Notion API から記事の情報を取得することができました！
これですぐにブログが公開できる！と思ったのですが、API を使用するにあたっての大変な部分はここからでした。

取得されるデータの型がわからない、、、
もちろんリファレンスに型は載っているが、block を取得する場合 BlockType がいくつもありそれぞれの Type で持っているフィールドが異なっています。
つまり、notionapi.Block の持つ GetType()でブロックのタイプを特定し、タイプごとに処理を分岐させる必要があるのでした。。。

これを自前の DB に保存する時とか、フロントエンドに受け渡す時とか、どうやって扱えばいいんやろか・・・考えることは多いですね。。

今回はとりあえず記事を書くときに使用する最低限の block だけ実装しました！
