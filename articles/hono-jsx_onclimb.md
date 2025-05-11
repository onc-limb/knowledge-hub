---
title: hono-jsxにReactを導入しようとした話
emoji: ""
type: tech
topics:
  - hono
published: false
---

## はじめに

こんにちは、onc-limb です！

最近 TypeScript のサーバーサイドフレームワークの hono が気になって、色々試しに実装してみています。

今回は hono が jsx を返せることを知り、hono だけで一つのサービスを作ろうと試みている中で、「クライアントサイドでも型セーフに javascript を書きたい」と思い、CSR 部分だけ React を導入しようとした話です。

いや、hono だけではなくなってるやん。。。そうなんよね。

## hono/jsx と React

そもそも、hono が jsx を返せるのにどうして React を入れようと思ったか。

それは hono の jsx が完全な HTML を生成する SSR を前提として作られているから。

どう言うことか？

私は、プレースホルダーや変数が使える HTML が返せるよくらいで認識しました。

クライアントサイドでプログラムを動かすには JavaScript を組み込まなければいけないが、

動的に JacaScript を組み込むには DOM が必要らしい。

（ここら辺は React エンジニアにとっては周知の内容らしいが、無知なので今後調べます。）

もちろん hono/jsx で生成する HTML の中に直接 JavaScript をゴリゴリ書いたら、クライアントサイドで動くものはできるが、型チェックができない、状態管理ができないなど、現在において味わう必要のない苦労が発生する。

それなら React を入れてしまおうと。

## Form を作ろうとしたら、型が合わない、、、？

サンプルとして、簡単な Form のバリデーションをクライアント側でさせるように React を導入しようとした。

やったことは単純で、下記コマンドで React をインストールして利用するだけ。

```jsx
bun add react react-dom
bun add -d @types/react @types/react-dom
```

しかし、実際には

```jsx
<form onSubmit={handleSubmit}>・・・</form>
```

このよくみる form タグの onSubmit が型エラーを吐き続けてしまった。

なんでやろなーと調べた結果、form の onSubmit に渡す型が、hono/jsx と react で異なっており、form タグでは hono/jsx の定義を参照していた。（onSubmit 関数は React の型で作成していた）

これは JSX というのは同じでも、hono/jsx の作者は React の機能は参考にしたが、コードまではみていない(見たら引っ張られてしまうから敢えて見なかった)らしい。

加えて React は結構独自の路線を走っていて、React 特有の関数や型を定義しているが(まあ、それが React の強みでもあるが)、hono は一貫して「web 標準に準拠」を貫いている。

## 解決方法と結論

思想の違いもあり、型定義に差分が生まれてしまうのはしょうがないが、じゃあ hono/jsx と React は一緒に使うことはできないのか。

そんなことはないはず。

`Module Augmentation`機能で onSubmit 型だけ React の型を使用するように定義しなおせば良い。

けど、今後も競合するような関数が多くあるんだろうなーと。

そこでちゃんと調べたら、先人がライブラリを作っているではないですか。

hono/middleware の react-render というライブラリが！

最初から調べればよかったと思いながら導入を考えていると、hono 公式にも hono/jsx/dom というものが、、、

なんと hono がちゃんと dom 上で動くライブラリを用意してくれていたのだ。

これに気づくのに数時間、仕事だったら「何やってんだオメー」となってしまうが、これはあくまで趣味なので OK。むしろ曖昧理解だった SSR、CSR の違いや DOM の役割を勉強する機会になりました。

hono/jsx/dom 具体的な導入方法はまた別で。
