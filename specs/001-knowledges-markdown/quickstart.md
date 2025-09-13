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
# デフォルトでknowledgesディレクトリをスキャンしてmeta.jsonを更新
node scripts/generate-metadata.ts

# 実行結果の確認
cat knowledges/meta.json
```

**期待される結果**:

- `knowledges/meta.json` が更新される
- コンソールに処理状況が表示される
- エラーがなければ正常終了（exit code 0）

### 2. 詳細ログ付きで実行

```bash
# 処理内容を詳しく確認したい場合
node scripts/generate-metadata.ts --verbose

# 出力例:
# Scanning directory: knowledges
# Found category: ai (7 files, 1 subcategory)
# Found category: aws (3 files, 3 subcategories)
# Generated metadata for 8 categories
# Written to: knowledges/meta.json
```

### 3. 変更前の確認（ドライラン）

```bash
# 実際にファイルを変更せずに結果を確認
node scripts/generate-metadata.ts --dry-run

# 出力例:
# Would scan directory: knowledges
# Would generate metadata for:
#   - ai (7 points)
#   - aws (3 points)
# Would write to: knowledges/meta.json
# No files were modified.
```

## 高度な使用方法

### 4. 出力形式の変更

```bash
# 見やすい形式で標準出力に表示
node scripts/generate-metadata.ts --format pretty

# JSON形式で標準出力（他のツールとの連携用）
node scripts/generate-metadata.ts --format json
```

### 5. カスタム出力ファイル

```bash
# 別の場所にメタデータファイルを生成
node scripts/generate-metadata.ts --output backup/meta.json

# 一時的なメタデータ生成
node scripts/generate-metadata.ts --output /tmp/temp-meta.json
```

### 6. 異なるディレクトリのスキャン

```bash
# 別のディレクトリをスキャン（テスト用途など）
node scripts/generate-metadata.ts ./test-knowledges --output test-meta.json
```

## 実際の作業フロー例

### シナリオ 1: 新しい記事を追加した後

```bash
# 1. 新しいMarkdownファイルを作成
echo "# 新しい記事" > knowledges/typescript/新しい記事.md

# 2. メタデータを更新
node scripts/generate-metadata.ts --verbose

# 3. 変更を確認
git diff knowledges/meta.json
```

### シナリオ 2: カテゴリ構造を大幅に変更した後

```bash
# 1. 現在の状態を確認
node scripts/generate-metadata.ts --dry-run

# 2. 実際に更新
node scripts/generate-metadata.ts

# 3. 変更内容の検証
node scripts/generate-metadata.ts --format pretty
```

### シナリオ 3: 統計情報の確認

```bash
# 1. 現在の統計を確認
node scripts/generate-metadata.ts --format pretty

# 2. カテゴリ別のファイル数を取得
jq '.categories[] | {category: .category, point: .point}' knowledges/meta.json
```

## トラブルシューティング

### よくある問題と解決方法

#### 問題 1: Permission denied エラー

```bash
Error: Permission denied accessing directory: knowledges
```

**解決方法**:

```bash
# ディレクトリの権限を確認
ls -la knowledges/

# 必要に応じて権限を修正
chmod 755 knowledges/
```

#### 問題 2: Directory not found エラー

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

#### 問題 3: JSON 書き込みエラー

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
# デバッグモードで実行
DEBUG=metadata-generator node scripts/generate-metadata.ts --verbose

# ログファイルに出力
node scripts/generate-metadata.ts --verbose 2>&1 | tee metadata-generation.log
```

## 検証方法

### 生成されたメタデータの妥当性確認

```bash
# JSON形式の妥当性チェック
jq empty knowledges/meta.json && echo "Valid JSON" || echo "Invalid JSON"

# スキーマ検証（jqを使用）
jq '.categories | type' knowledges/meta.json  # "array"が出力されるべき

# ファイル数の手動確認
find knowledges -name "*.md" | wc -l
# この数値とmeta.jsonの全pointの合計が一致するべき
```

### パフォーマンス測定

```bash
# 実行時間の測定
time node scripts/generate-metadata.ts

# メモリ使用量の確認（Node.js）
node --max-old-space-size=100 scripts/generate-metadata.ts
```

## 次のステップ

1. **自動化**: CI パイプラインでの自動メタデータ更新
2. **監視**: ファイル変更の監視と自動実行
3. **拡張**: カスタムフィルタやフォーマットの追加

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
      - run: node scripts/generate-metadata.ts
      - run: git add knowledges/meta.json
      - run: git commit -m "Update metadata" || exit 0
      - run: git push
```

この quickstart ガイドに従うことで、メタデータ生成機能を効果的に活用できるようになります。
