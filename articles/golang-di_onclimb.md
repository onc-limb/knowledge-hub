---
title: "gqlgenとgormでDB操作の依存性注入(DI)を行う"
emoji: ""
type: "tech"
topics: ["golang", "graphql"]
published: true
---

## はじめに
こんにちは、onclimb です。
仕事では TypeScript のフレームワークである NestJS を使用しています。

NestJS では依存性注入を@Module デコレーターを使ってモジュールごとに行いますが、go 言語ではどのように実装すれば良いかわからなかったので試してみました。

## 背景：

開発言語　 go 言語

フレームワーク　 gqlgen、gorm

依存性注入はなぜ必要なのかは別の記事で記述して、今回は具体的な手法を記述します。

今回やりたいこと

- DB 操作は repository からのみ行う。
- domain に repository のインターフェースのみ定義して、usecase は domain を参照する。
- repository は domain に定義したインターフェースを継承して実装する。

## 結論

repository, usecase に New 関数を定義して、`特定のインスタンスを`フィールドに継承したインスタンスを作成することで解決した。

Repository の作成

```go
package repository

type Repository struct {
	DB *gorm.DB
}

func NewRepository(db *gorm.DB) *Repository {
	return &Repository{DB: db}
}

```

usecase の作成

```go
package usecase

type Usecase struct {
	Repo domain.Repository
}

func NewUsecase(repo domain.Repository) *Usecase {
	return &Usecase{Repo: repo}
}
```

domain にインターフェースの作成

```go
package domain

type Repository interface {
	// DBに接続する関数の型を定義する
}
```

gqlgen が自動生成している Resolver 型に Repository フィールドを追加

```go
package graph

type Resolver struct {
	*gorm.DB
	Repository domain.Repository // 追加
}
```

main 関数で DB の接続情報を持った Repository インスタンスを Resolver に注入する。

```go
package main

func main() {
	// 無関係のコードは割愛
	// dsnは事前に定義
	db, _ := gorm.Open(postgres.Open(dsn), &gorm.Config{}) 
	repo := infra.NewRepository(db)

	// graphqlのresolverにrepository設定
	graphqlHandler := handler.NewDefaultServer(graph.NewExecutableSchema(graph.Config{Resolvers: &graph.Resolver{Repository: repo}}))

	// 以下で起動処理
```

あとは今後作成する usecase や repository の関数のレシーバーに Usecase 型や Repository 型を指定してやれば、レシーバーから DI した DB インスタンスや Repository インスタンスにアクセスすることができる。

```go
package usecase

func (u *Usecase) Get(id uint) (data, error) {
	retrun u.Repository.Find(id)
}
```

```go
package repository

func (r *Repository) Find(id uint) (data, error) {
	result := r.DB.First(&data, id)
	if result.Error != nil {
		panic()
	}
	return data, nil
}
```

この方法が本当に良いのか、一般的なのかはわかりませんが、ソースコード上 usecase や resolver が repository に依存することがなくなったので今回はよしとします。

go 言語は仕様で package の循環参照が禁止されているので、依存性違反はできないようになっていますね。

個人開発のような小規模なアプリなら package を一つにまとめちゃったほうが早いし楽なのかもしれません。（そもそも小規模アプリに go 言語は採用しないかもしれませんが…）
