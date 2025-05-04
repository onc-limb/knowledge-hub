## はじめに

私は成長の記録をブログに残していこうと思っています。
そしてブログサイト自体を自作してしまえば、それ自体が勉強になるのではないかということで作成しています。
つまりブログサイトが出来上がるまでブログを公開できないのです、、、笑
（この記事もいつか公開されるのだろうか？）

とりあえず今はNotionに書き留めています。
しかし、公開していないと三日坊主で書かなくなってしまう気がする、なんとか早く公開できないか考えた結果、
Notionに記載した内容をそのままアプリケーションに取り込むことはできないのか？
Notion APIというものがあるではないですか！ということで早速使ってみました。

## Notion APIとは

Notion APIはAPIを叩くことでNotion上のページやデータベースにアクセスし、データの取得、挿入、更新などが可能なものです。
詳しい内容は分かりやすくまとめている方がいっぱいいるのでここでは割愛します。
とりあえず、個人で利用する分にはNotion同様無料で使用可能です！

## 導入手順

### 前提

Notionのアカウントは作成済み
APIを叩くアプリケーションはgo言語で実装
APIの使用ケースはページの取得のみ

### API Keyの取得

Notion APIを取得するにはインテグレーションを作成する必要がある。
インテグレーションを作成したら、integration secretを記録しておく←これがAPI Key
インテグレーションの作成は以下のURLから可能です。

[https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

### 環境変数にAPI Keyを設定

.envにAPI Keyを設定する

```go
// .env
NOTION_API_KEY="***********"
```

※本番環境等ではインフラ構成に従って環境変数に設定すること

### NotionAPIライブラリを取得

NotionAPIをGo言語で扱うためのライブラリとして今回はnotionapi([https://github.com/jomei/notionapi](https://github.com/jomei/notionapi))を利用しました。

```bash
go get github.com/jomei/notionapi
```

このライブラリの使用方法は簡単で、

- API Keyを指定してClientインスタンスを作成する。
- 操作対象をdatabase、page、blockから選択して、関数を呼ぶ

これだけです！

Clientインスタンスの作成

```go
func NewClient() (client *NotionClient) {
	apiKey := os.Getenv("NOTION_API_KEY")
	return &NotionClient{
		client: notionapi.NewClient(notionapi.Token(apiKey)),
	}
}
```

page情報の取得

```go
func (nc NotionClient) GetPage(pageId string) (*notionapi.Page, error) {
	return nc.client.Page.Get(context.Background(), notionapi.PageID(pageId))
}
```

どんな情報が取得できるかはNotion APIの公式リファレンスを確認するのが良いかと思います！

## 最後に

これでNotion APIから記事の情報を取得することができました！
これですぐにブログが公開できる！と思ったのですが、APIを使用するにあたっての大変な部分はここからでした。

取得されるデータの型がわからない、、、
もちろんリファレンスに型は載っているが、blockを取得する場合BlockTypeがいくつもありそれぞれのTypeで持っているフィールドが異なっています。
つまり、notionapi.Blockの持つGetType()でブロックのタイプを特定し、タイプごとに処理を分岐させる必要があるのでした。。。

これを自前のDBに保存する時とか、フロントエンドに受け渡す時とか、どうやって扱えばいいんやろか・・・考えることは多いですね。。

今回はとりあえず記事を書くときに使用する最低限のblockだけ実装しました！
