---
title: "GitHub ActionsでDockerイメージをビルドしてECRにプッシュするワークフロー"
emoji: "🔧"
type: "tech"
topics: 
    - githubactions
    - ecr
published: true
---

## はじめに
Webアプリケーション開発において、CI/CDワークフローは必要不可欠な存在となっています。
GitHubへのpushをトリガーに自動でビルド・テスト・デプロイが実行される仕組みは、今や開発の標準となっています。

しかし、「ワークフローは動いているけど、中身はよく分かっていない」「先人が作った設定をそのまま使っている」という方も多いのではないでしょうか？

本記事では、GitHub Actionsを使ってDockerイメージをビルドし、AWS ECRにプッシュするワークフローを、各ステップの解説と共に紹介します。
公開されているActionsを活用することで、宣言的で読みやすく、保守しやすいワークフローの書き方を学べます。


これから新規プロジェクトを作成する方には、分かりやすいワークフロー作成の助けになればいいなと思います。
誰かが作ったワークフローをそのまま利用している方も、ワークフローで何をしているかを理解し、何かあったときにメンテナンスできるようになる一助となれたら嬉しいです。

## 前提
### 使用技術
コード管理: GitHub
CI/CDツール: GitHub Actions
コンテナレジストリ: AWS ECR

### 事前に準備が必要なもの
1. **AWSリソース**
   - ECRリポジトリの作成
   - GitHub Actions用のIAMロール（OIDC連携設定済み）
   - IAMロールに必要な権限: `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`

2. **GitHubリポジトリ設定**
   - 以下のSecretsを設定
     - `AWS_IAM_ROLE_ARN`: IAMロールのARN
     - `AWS_REGION`: ECRリポジトリのリージョン（例: `ap-northeast-1`）

3. **プロジェクト構成**
   - リポジトリルートに`Dockerfile`が配置されている

:::message
GitHub ActionsとAWSのOIDC連携設定については、[公式ドキュメント](https://docs.github.com/ja/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)を参照してください。
GitHub Actionsの基本構文などには触れません。
[公式ドキュメント](https://docs.github.com/ja/actions/reference/workflows-and-actions/workflow-syntax)を参照してください
:::

## 結論
結論、下記のようなworkflowファイルになりました。
```yaml
name: build & push

on:
  workflow_dispatch:

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      # ソースコードのチェックアウト
      - name: Checkout code
        uses: actions/checkout@v5

      # AWSのクレデンシャル設定
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v5
        with:
          role-to-assume: ${{ secrets.AWS_IAM_ROLE_ARN }}
          aws-region: ${{ secrets.AWS_REGION }}

      # ECRへのログイン
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      # Docker Buildxのセットアップ
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # Docker imageのビルドとECRへのpush
      - name: Build and push Docker image to ECR
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/amd64
          push: true
          tags: |
            ${{ steps.login-ecr.outputs.registry }}/your-repository-name:${{ github.sha }}
            ${{ steps.login-ecr.outputs.registry }}/your-repository-name:latest
          build-args: |
            YOUR_BUILD_ARG=your-build-arg
          cache-from: type=gha
          cache-to: type=gha,mode=max

```
:::message alert
**要変更箇所**
- `your-repository-name`: 実際のECRリポジトリ名に置き換えてください
- `YOUR_BUILD_ARG=your-build-arg`: ビルド時に必要な引数がある場合のみ設定（不要な場合は`build-args`セクションごと削除可能）
:::

## 各actionの内容

### actions/checkout@v5
このアクションは、GitHubリポジトリのソースコードをワークフロー環境（GitHub Actions実行環境）にクローンします。

**役割**:
- リポジトリのコードをワークフロー環境の`$GITHUB_WORKSPACE`ディレクトリに配置
- Dockerfileやビルドに必要なファイルにアクセスできるようにする

**主な特徴**:
- デフォルトでは1つのコミットのみをfetchする（軽量で高速）
- ワークフローをトリガーしたイベントに対応するブランチ・タグ・SHAをチェックアウト

**今回のワークフローでの使い方**:
```yaml
- name: Checkout code
  uses: actions/checkout@v5
```

シンプルに最新のv5を指定するだけで、現在のリポジトリのコードを取得できます。特別なオプションは不要です。

**参考リンク**: [actions/checkout](https://github.com/actions/checkout)

---

### aws-actions/configure-aws-credentials@v5
このアクションは、GitHub ActionsからAWSへの認証を行い、AWS認証情報を環境変数として設定します。

**役割**:
- GitHub ActionsのOIDCプロバイダーを使用してAWSのIAMロールを引き受ける（AssumeRole）
- 一時的なAWS認証情報（アクセスキー、シークレットキー、セッショントークン）を取得
- 後続のステップでAWS CLIやAWS SDKが使用できるよう環境変数を設定

**今回のワークフローでの使い方**:
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v5
  with:
    role-to-assume: ${{ secrets.AWS_IAM_ROLE_ARN }}
    aws-region: ${{ secrets.AWS_REGION }}
```

**パラメータ説明**:
- `role-to-assume`: AssumeRoleするIAMロールのARN（例: `arn:aws:iam::123456789012:role/my-github-actions-role`）
- `aws-region`: AWSリージョン（例: `ap-northeast-1`）

**必要な事前設定**:
1. AWSでOIDCプロバイダーの設定（Provider URL: `https://token.actions.githubusercontent.com`）
2. GitHub Actionsを信頼する信頼ポリシーを持つIAMロールの作成
3. 必要な権限（ECRへのアクセス等）をIAMロールにアタッチ

**参考リンク**: [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)

---

### aws-actions/amazon-ecr-login@v2
このアクションは、ローカルのDockerクライアントをAmazon ECRにログインさせます。

**役割**:
- ECRの認証トークンを取得
- `docker login`コマンドを実行してDockerクライアントを認証
- 後続のステップで`docker push`や`docker pull`が実行できるようにする

**今回のワークフローでの使い方**:
```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v2
```

**出力される情報**:
このアクションは`id: login-ecr`を指定することで、以下の情報を出力として取得できます：
- `registry`: ECRレジストリのURI（例: `123456789012.dkr.ecr.ap-northeast-1.amazonaws.com`）

この`registry`出力は、後続のステップでイメージのタグ付けに使用されます：
```yaml
tags: |
  ${{ steps.login-ecr.outputs.registry }}/your-repository-name:latest
```

**認証の仕組み**:
1. 前のステップで設定されたAWS認証情報を使用
2. ECRの`GetAuthorizationToken` APIを呼び出し
3. 取得したトークンを使って`docker login`を実行
4. 認証情報はローカルのDocker設定（通常は`~/.docker/config.json`）に保存

**必要な権限**:
IAMロールに以下の権限が必要です：
- `ecr:GetAuthorizationToken`（認証トークン取得用）
- `ecr:BatchCheckLayerAvailability`（レイヤー確認用）
- `ecr:PutImage`（イメージプッシュ用）
- `ecr:InitiateLayerUpload`（レイヤーアップロード開始用）
- `ecr:UploadLayerPart`（レイヤーアップロード用）
- `ecr:CompleteLayerUpload`（レイヤーアップロード完了用）

**参考リンク**: [aws-actions/amazon-ecr-login](https://github.com/aws-actions/amazon-ecr-login)

---

### docker/setup-buildx-action@v3
このアクションは、Docker Buildxをセットアップして高度なビルド機能を有効にします。

**役割**:
- Docker Buildxをインストール・設定
- マルチプラットフォームビルド、キャッシュ管理などの高度な機能を提供
- デフォルトで`docker-container`ドライバーを使用したbuilderインスタンスを作成・起動

**Buildxとは**:
Docker Buildxは、Docker CLIの拡張機能で、BuildKitの全機能を活用できるようにするプラグインです。

**主な機能**:
- **マルチプラットフォームビルド**: `linux/amd64`, `linux/arm64`など複数のプラットフォーム向けに同時ビルド
- **高度なキャッシュ管理**: ビルドキャッシュをレジストリに保存・共有
- **並列ビルド**: 複数のビルドステージを並列実行して高速化
- **ビルドシークレット**: ビルド時に安全に機密情報を渡せる

**今回のワークフローでの使い方**:
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```

デフォルト設定で使用する場合、追加のパラメータは不要です。以下が自動的に設定されます：
- ドライバー: `docker-container`（BuildKitコンテナを使用）
- プラットフォーム: ランナー環境で利用可能なプラットフォームを自動検出

**参考リンク**: [docker/setup-buildx-action](https://github.com/docker/setup-buildx-action)

---

### docker/build-push-action@v6
このアクションは、DockerイメージをビルドしてECRにプッシュするコア機能を提供します。

**役割**:
- Dockerイメージをビルド
- 指定されたレジストリ（今回はECR）にイメージをプッシュ
- キャッシュ管理による高速化
- マルチプラットフォーム対応

**今回のワークフローでの使い方**:
```yaml
- name: Build and push Docker image to ECR
  uses: docker/build-push-action@v6
  with:
    context: .
    file: ./Dockerfile
    platforms: linux/amd64
    push: true
    tags: |
      ${{ steps.login-ecr.outputs.registry }}/your-repository-name:${{ github.sha }}
      ${{ steps.login-ecr.outputs.registry }}/your-repository-name:latest
    build-args: |
      YOUR_BUILD_ARG=your-build-arg
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**主要パラメータの説明**:

#### `context`（必須）
ビルドコンテキストのパス。Dockerfileが参照するファイルのルートディレクトリ。
- `.`: リポジトリルート
- `./backend`: サブディレクトリを指定

#### `file`
Dockerfileのパス。デフォルトは`{context}/Dockerfile`。
- `./Dockerfile`: ルートのDockerfile
- `./docker/Dockerfile.prod`: 別の場所のDockerfile

#### `platforms`
ビルド対象のプラットフォーム。カンマ区切りで複数指定可能。
- `linux/amd64`: x86_64アーキテクチャ（一般的なサーバー）
- `linux/arm64`: ARM64アーキテクチャ（Apple Silicon、AWS Gravitonなど）
- `linux/amd64,linux/arm64`: 両方のプラットフォーム向けにマルチアーキテクチャイメージを作成

#### `push`
ビルド後にイメージをレジストリにプッシュするかどうか。
- `true`: プッシュする（本番デプロイ用）
- `false`: ローカルビルドのみ（テスト用）

#### `tags`
イメージに付与するタグ。複数指定可能（改行区切り）。
```yaml
tags: |
  ${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}
  ${{ steps.login-ecr.outputs.registry }}/my-app:latest
```
- コミットSHAをタグにすることで、どのコードからビルドされたか追跡可能
- `latest`タグは常に最新版を指すように更新

#### `build-args`（オプション）
Dockerビルド時に渡す引数。Dockerfile内で`ARG`命令で定義した変数に値を設定。

**Dockerfile例**:
```dockerfile
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
```

**ワークフロー**:
```yaml
build-args: |
  NODE_ENV=staging
```

不要な場合はこのセクション全体を削除できます。

#### `cache-from` / `cache-to`
ビルドキャッシュの読み込み元と保存先を指定。2回目以降のビルドを高速化。

**今回の設定**:
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

**説明**:
- `cache-from: type=gha`: GitHubのキャッシュストレージからキャッシュを読み込む
- `cache-to: type=gha mode=max`: 全てのビルドステージをキャッシュ（最大限の高速化）

**簡易的なキャッシュ戦略**:
GitHubのキャッシュストレージを使用できない場合には下記の設定も可能
```yaml
cache-from: type=registry,ref=${{ steps.login-ecr.outputs.registry }}/your-repository-name:latest
cache-to: type=inline
```
- `cache-from`: refで指定したレジストリからキャッシュを取得する
- `cache-to: type=inline`: 全てのビルドステージをキャッシュ（最大限の高速化）キャッシュ情報をイメージ内に埋め込む方式

**参考リンク**: [docker/build-push-action](https://github.com/docker/build-push-action)

## まとめ
GitHub ActionsでDockerイメージをビルドして、AWS ECRにプッシュするワークフローを紹介しました。
サービスの表には出てこず、普段は当たり前のように動いているものだからこそ、内部で何が行われているのかを知っておくことが大事だと思います。
ぜひ、この記事を読んだ後は自分のプロジェクトの裏で動いているワークフローが何を行っているかに目を向けて見てはいかがでしょうか。

GitHubはワークフローの[テンプレート](https://github.com/actions/starter-workflows/tree/main)を用意してくれており、今回はこの[deployments/aws.yml](https://github.com/actions/starter-workflows/blob/main/deployments/aws.yml)をベースに書いています。
