# Quickstart Guide: knowledges ディレクトリメタデータ生成機能

## 概要

このガイドでは、knowledges ディレクトリメタデータ生成機能の基本的な使用方法から、開発者向けの詳細な操作まで順を追って説明します。

## 前提条件

### システム要件

- Node.js 18.0 以上
- npm または yarn
- TypeScript 5.0 以上

### ワークスペース確認

```bash
# 正しいディレクトリにいることを確認
pwd
# /path/to/knowledge-hub が表示されるべき

# 必要なファイルが存在することを確認
ls knowledges/
# ai, aws, css などのディレクトリが表示されるべき
```

## 基本的な使用方法

### 1. メタデータ生成（最も一般的な用途）

```bash
# knowledgesディレクトリをスキャンしてmeta.jsonを更新
npx tsx scripts/generate-metadata.ts

# 実行結果の確認
cat knowledges/meta.json
```

**期待される結果**:

- `knowledges/meta.json` が更新される
- 3 階層構造（categories, subCategories, subSubCategories）でメタデータが生成される
- totalFiles と lastUpdated が自動更新される
- エラーがなければ正常終了（exit code 0）

### 2. 実行結果の確認

```bash
# 生成されたメタデータの内容を確認
cat knowledges/meta.json | jq .

# 出力例:
# 生成されたJSONの整形表示で、3階層構造を確認できる
```

### 3. 既存実装の動作確認

```bash
# 現在のメタデータ生成を実行
npx tsx scripts/generate-metadata.ts

# 生成されたメタデータの構造確認
cat knowledges/meta.json | jq '.categories[0]'
# {
#   "category": "ai",
#   "point": 7,
#   "subCategories": [
#     {
#       "category": "機械学習",
#       "point": 6,
#       "names": ["LightningCLIとは.md", "Lightningのモジュール.md", ...],
#       "subSubCategories": [...]
#     }
#   ]
# }
```

## 高度な使用方法

### 4. 出力結果の分析

```bash
# 総ファイル数の確認
cat knowledges/meta.json | jq '.totalFiles'

# 最終更新日時の確認
cat knowledges/meta.json | jq '.lastUpdated'

# カテゴリ別ファイル数の確認
cat knowledges/meta.json | jq '.categories[] | {category: .category, point: .point}'
```

### 5. メタデータの定期更新

```bash
# cronまたは定期実行スクリプトでの利用例
npx tsx scripts/generate-metadata.ts
git add knowledges/meta.json
git commit -m "chore: update knowledges metadata"
```

## 実際の作業フロー例

### シナリオ 1: 新しい記事を追加した後

```bash
# 1. 新しいMarkdownファイルを作成
echo "# 新しい記事" > knowledges/typescript/新しい記事.md

# 2. メタデータを更新
npx tsx scripts/generate-metadata.ts

# 3. 変更を確認
git diff knowledges/meta.json
```

### シナリオ 2: カテゴリ構造を変更した後

```bash
# 1. 現在の状態を確認
cat knowledges/meta.json | jq '.categories | length'

# 2. メタデータを更新
npx tsx scripts/generate-metadata.ts

# 3. 変更内容の検証
cat knowledges/meta.json | jq '.categories[] | .category'
```

### シナリオ 3: 統計情報の確認

```bash
# 1. 現在の統計を確認
cat knowledges/meta.json | jq '{totalFiles: .totalFiles, lastUpdated: .lastUpdated}'

# 2. カテゴリ別のファイル数を取得
cat knowledges/meta.json | jq '.categories[] | {category: .category, point: .point}'
```

## トラブルシューティング

### よくある問題と解決方法

#### 問題 1: TypeScript 実行エラー

```bash
Error: Could not resolve TypeScript module
```

**解決方法**:

**解決方法**:

```bash
# tsxまたはts-nodeがインストールされているか確認
npm list tsx ts-node

# 必要に応じてインストール
npm install -g tsx
# または
npm install -g ts-node

# プロジェクトローカルでの実行
npx tsx scripts/generate-metadata.ts
```

#### 問題 2: knowledges ディレクトリが見つからない

```bash
Error: Directory not found: knowledges
```

**解決方法**:

```bash
# 現在の場所を確認
pwd

# knowledgesディレクトリの存在確認
ls -la | grep knowledges

# 正しいディレクトリに移動
cd /path/to/knowledge-hub
```

#### 問題 3: メタデータファイルの書き込みエラー

```bash
Error: Cannot write to output file: knowledges/meta.json
```

**解決方法**:

```bash
# ファイルの権限を確認
ls -la knowledges/meta.json

# 必要に応じて権限を修正
chmod 644 knowledges/meta.json

# ディレクトリの権限も確認
chmod 755 knowledges/
```

### 詳細なログの取得

```bash
# TypeScript実行環境でのデバッグ
npx tsx scripts/generate-metadata.ts

# ログファイルに出力
npx tsx scripts/generate-metadata.ts 2>&1 | tee metadata-generation.log
```

## 検証方法

### 生成されたメタデータの妥当性確認

```bash
# JSON形式の妥当性チェック
cat knowledges/meta.json | jq empty && echo "Valid JSON" || echo "Invalid JSON"

# スキーマ検証（jqを使用）
cat knowledges/meta.json | jq '.categories | type'  # "array"が出力されるべき
cat knowledges/meta.json | jq '.totalFiles | type'  # "number"が出力されるべき
cat knowledges/meta.json | jq '.lastUpdated | type'  # "string"が出力されるべき

# 3階層構造の確認
cat knowledges/meta.json | jq '.categories[0].subCategories[0].subSubCategories | type'
```

### パフォーマンス測定

```bash
# 実行時間の測定
time npx tsx scripts/generate-metadata.ts

# ファイル数の確認
find knowledges -type f | wc -l
# この数値とmeta.jsonのtotalFilesが一致するべき
```

## 次のステップ

1. **テスト追加**: 既存実装用のテストスイート構築
2. **ドキュメント**: 契約仕様書の完成
3. **監視**: ファイル変更の監視と自動実行

### package.json スクリプト化

```json
{
  "scripts": {
    "generate-metadata": "tsx scripts/generate-metadata.ts",
    "metadata:check": "jq empty knowledges/meta.json"
  }
}
```

### CI 統合例

```yaml
# .github/workflows/update-metadata.yml
name: Update Metadata
on:
  push:
    paths: ["knowledges/**"]
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npx tsx scripts/generate-metadata.ts
      - run: git add knowledges/meta.json
      - run: git commit -m "chore: update knowledges metadata" || exit 0
      - run: git push
```

この quickstart ガイドに従うことで、既存のメタデータ生成機能を効果的に活用できるようになります。
