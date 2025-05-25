---
title: go buildコマンドの挙動を確認してみる1
emoji: 📝
type: tech
topics:
  - golang
published: true
---
## はじめに
Go言語を使用するにあたって、基本文法やイディオムなど理解するべき事項はたくさんありますが、そのうちの一つがコマンドラインツールだと思います。
様々なコマンドラインツールが言語標準として用意されているのはGo言語の強みの一つだと思うので、コマンドラインツールを理解することがGo言語をマスターするための一歩となるだろう。

今回は最もよく使われるであろう`go build`コマンドについて見ていこうと思います。
コンパイラ、リンカの挙動や各OS向けの挙動などは複雑になってくると思うので、今回は全体的な流れだけを追っていきます。

## 前提
参照ソースコード：執筆時点の[goのコード](https://github.com/golang/go)
※バージョンアップ等によって、コードが変更されることがあると思うので、ご了承ください。

コマンドラインの処理には、go runtimeの初期化処理などもありますが、今回は対象にしていません。

## goコマンドの実行の流れ
Go言語でプログラムを書いたあと、実行するために`go build`コマンドを実行します。
このコマンドを入力した際、プログラムではどのような挙動をしているのでしょうか。

対象コード
- src/cmd/go/main.go

goコマンドを実行するとき、最初にコマンドの初期化を行います。
これにより、各パッケージで定義された挙動がコマンドに登録されます。
```go
func init() {
	base.Go.Commands = []*base.Command{
		bug.CmdBug,
		work.CmdBuild,
		clean.CmdClean,
		// 以下、省略
	}
}
```

CLIから入力されたコマンドを解析し、対応するコマンド処理を実行します。
```go
func main() {
	// 省略　各種設定処理

	// コマンド引数の取得
	args := flag.Args()
	if len(args) < 1 {
		base.Usage()
	}

	// 省略

	//　引数からコマンドの特定
	cmd, used := lookupCmd(args)
	cfg.CmdName = strings.Join(args[:used], " ")

	// 省略

	// コマンドの実行
	invoke(cmd, args[used-1:])
	base.Exit()
}
```

GOROOTの解析や各種フラグの解析などは大幅に省略しましたが、ざっくりとみるとこんな感じです。

## go buildの実行の流れ
それでは本格的にgo buildコマンドの実行の流れを見ていきましょう。

対象コード
- src/cmd/go/internal/work/build.go
```go
func runBuild(ctx context.Context, cmd *base.Command, args []string) {
```

【初期化処理】
- go.workファイルの初期化処理(modload.InitWorkfile())
- ビルドシステムの実行環境を初期化し、ビルドに必要な全設定を検証(BuildInit())
- 実行可能なビルダーインスタンスの作成(NewBuilder(""))
```go
	modload.InitWorkfile()
	BuildInit()
	b := NewBuilder("")
	defer func() {
		if err := b.Close(); err != nil {
			base.Fatal(err)
		}
	}()
```

【ビルド対象パッケージの解析】
- コマンドライン引数で指定されたディレクトリを解析し、依存関係を含むパッケージツリーを構築する。(load.PackagesAndErrors(ctx, load.PackageOpts{AutoVCS: true}, args))
- パッケージのエラーチェック(load.CheckPackageErrors(pkgs))
- -oオプションが未指定かつ、ビルド対象が一つのmainパッケージの場合の出力ファイル名決定
```go
	pkgs := load.PackagesAndErrors(ctx, load.PackageOpts{AutoVCS: true}, args)
	load.CheckPackageErrors(pkgs)

	explicitO := len(cfg.BuildO) > 0

	if len(pkgs) == 1 && pkgs[0].Name == "main" && cfg.BuildO == "" {
		cfg.BuildO = pkgs[0].DefaultExecName()
		cfg.BuildO += cfg.ExeSuffix
	}
```

【使用コンパイラのチェック】
- 使用するコンパイラに合ったフラグを設定しているかをチェック。
- 誤った設定をしている場合はユーザーに通知
```go
	// sanity check some often mis-used options
	switch cfg.BuildContext.Compiler {
	case "gccgo":
		if load.BuildGcflags.Present() {
			fmt.Println("go build: when using gccgo toolchain, please pass compiler flags using -gccgoflags, not -gcflags")
		}
		if load.BuildLdflags.Present() {
			fmt.Println("go build: when using gccgo toolchain, please pass linker flags using -gccgoflags, not -ldflags")
		}
	case "gc":
		if load.BuildGccgoflags.Present() {
			fmt.Println("go build: when using gc toolchain, please pass compile flags using -gcflags, and linker flags using -ldflags")
		}
	}
```

【依存関係解決モードの設定】
- 依存関係解決をビルドモードに設定
```go
	depMode := ModeBuild
```

【パッケージのフィルタリング】
- 不正なパッケージの除外
- テスト用パッケージの除外
```go
	pkgs = omitTestOnly(pkgsFilter(pkgs))
```

【dev/null制御】
- -o /dev/null (windowsなら-o null)が指定された場合、ファイル出力をスキップするための設定
```go
	// Special case -o /dev/null by not writing at all.
	if base.IsNull(cfg.BuildO) {
		cfg.BuildO = ""
	}
```

【カバレッジ計測準備】
- -coverが設定されたいたら、カバレッジ計測用のパッケージを追加
```go
	if cfg.BuildCover {
		load.PrepareForCoverageBuild(pkgs)
	}
```

【出力先ごとにビルドアクションの生成】
- 出力先ごとに、エラーチェックを行う。
- mainのビルドアクションを生成する(&Action{Mode: "go build"})
- 依存パッケージのビルドアクションを生成する(append(a.Deps, b.AutoAction(ModeInstall, depMode, p)))
- ビルド実行(b.Do(ctx, a))
```go
	if cfg.BuildO != "" {
		// If the -o name exists and is a directory or
		// ends with a slash or backslash, then
		// write all main packages to that directory.
		// Otherwise require only a single package be built.
		if fi, err := os.Stat(cfg.BuildO); (err == nil && fi.IsDir()) ||
			strings.HasSuffix(cfg.BuildO, "/") ||
			strings.HasSuffix(cfg.BuildO, string(os.PathSeparator)) {
			if !explicitO {
				base.Fatalf("go: build output %q already exists and is a directory", cfg.BuildO)
			}
			a := &Action{Mode: "go build"}
			for _, p := range pkgs {
				if p.Name != "main" {
					continue
				}

				p.Target = filepath.Join(cfg.BuildO, p.DefaultExecName())
				p.Target += cfg.ExeSuffix
				p.Stale = true
				p.StaleReason = "build -o flag in use"
				a.Deps = append(a.Deps, b.AutoAction(ModeInstall, depMode, p))
			}
			if len(a.Deps) == 0 {
				base.Fatalf("go: no main packages to build")
			}
			b.Do(ctx, a)
			return
		}
		if len(pkgs) > 1 {
			base.Fatalf("go: cannot write multiple packages to non-directory %s", cfg.BuildO)
		} else if len(pkgs) == 0 {
			base.Fatalf("no packages to build")
		}
		p := pkgs[0]
		p.Target = cfg.BuildO
		p.Stale = true // must build - not up to date
		p.StaleReason = "build -o flag in use"
		a := b.AutoAction(ModeInstall, depMode, p)
		b.Do(ctx, a)
		return
	}

	a := &Action{Mode: "go build"}
	for _, p := range pkgs {
		a.Deps = append(a.Deps, b.AutoAction(ModeBuild, depMode, p))
	}
	if cfg.BuildBuildmode == "shared" {
		a = b.buildmodeShared(ModeBuild, depMode, args, pkgs, a)
	}
	b.Do(ctx, a)
}
```

## まとめ
今回、go buildコマンドの処理の流れを見てきました。
初期化処理から始まり、対象パッケージの解析やフラグ、モードによる設定制御を行った後、ビルドアクションを生成して、ビルドを実行するという流れはなんとなく掴めたかと思います。

どのようなエラーチェックを行なっているか、どのような設定が読み込まれているかをみることで、実際にエラーに直面したときの原因分析の助けになればと思っています。

正直「ビルドアクションの生成」「ビルドアクションの実行」をより深掘りしていかないと、go buildコマンドによって、Goの実行ファイルがどのようにビルドされるかを理解したとは言えないかなとも思うので、今後はより深くビルド処理を理解して解説できるようにしていこうと思います。