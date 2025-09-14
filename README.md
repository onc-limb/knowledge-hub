# knowledge-hub

onc-limb のナレッジベースリポジトリ

## 概要

自分の技術知識、経験をナレッジや記事として蓄え、公開するサービス
markdown 形式で記載したドキュメントの保管を主としている。

機能として、下記の二つを持っている

- ナレッジが更新された時、ナレッジファイルの数やタイトルをスキャンしてメタデータファイルを更新する。（**拡張版で無制限階層対応済み**）
- 記述したドキュメントに対して、エビデンスや文章構成などを添削、指摘するエージェント機能。

## 仕様

### /articles

zenn(https://zenn.dev/)とホームページ(https://www.onc-limb.com/)に記事を公開するためのディレクトリ

- .md ファイルの published プロパティが true の場合、zenn とホームページに公開する。
- .md ファイルの published プロパティが false の場合、ホームページにのみ公開する。

### /book

zenn に書籍を公開するためのディレクトリ

- 現在は未使用

### /knowledges

技術分野のメモや記録を残しておくためのディレクトリ

- ホームページに公開する。

### /scripts

/knowledges 配下にある.md ファイルをスキャンして、メタデータを生成するスクリプト

#### メタデータ生成機能

- **従来版**: `npm run generate-metadata` - 3 階層制限、全ファイル対象
- **拡張版**: `npm run generate-metadata-enhanced` - 無制限階層、カスタムフィルタ、CLI オプション

#### 主な新機能（拡張版）

- 🚀 **無制限階層スキャン**: 3 階層を超える深いディレクトリ構造に対応
- 📝 **マークダウンフィルタ**: `--md-only`でマークダウンファイルのみ対象
- ⚙️ **カスタマイズ可能**: `--max-depth`、`--format`、`--verbose`等のオプション
- 🔄 **完全な下位互換性**: 従来の動作を`--legacy`モードで維持
- 📊 **複数出力形式**: JSON（従来）とテキスト形式をサポート

#### 使用例

```bash
# 基本使用（無制限階層）
npm run generate-metadata-enhanced

# マークダウンのみ、最大3階層
npm run generate-metadata-enhanced -- --md-only --max-depth 3

# テキスト形式で出力
npm run generate-metadata-enhanced -- --format text --output structure.txt

# ヘルプ確認
npm run generate-metadata-enhanced -- --help
```

### /Proofreading

記事やメモの内容を添削するエージェントサービス

### /tests

メタデータ生成機能のテストスイート

- Contract tests: 既存機能の動作確認
- Integration tests: 階層処理とファイルスキャンの統合テスト
- Enhanced tests: 新機能のテスト
- Performance tests: パフォーマンス比較
