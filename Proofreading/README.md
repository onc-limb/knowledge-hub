# 記事校閲エージェントシステム

技術記事の校閲を自動化するマルチエージェントシステムです。

## 機能

- **エビデンス調査**: 記事内の技術的主張の事実確認
- **文章校閲**: 日本語文章の文法・スタイル・読みやすさのチェック
- **多角的分析**: 複数のエージェントによる包括的な校閲

## セットアップ

### 1. 依存関係のインストール

```bash
cd Proofreading
pip install -r requirements.txt
```

### 2. 環境設定

`.env.template`をコピーして`.env`ファイルを作成し、APIキーを設定：

```bash
cp .env.template .env
# .envファイルを編集してAPIキーを設定
```

### 3. 使用方法

#### 記事の校閲実行

```bash
# 基本的な校閲
python main.py proofread -f articles/my-article.md

# 詳細出力とレポート保存
python main.py proofread -f knowledges/python/Logging.md -o report.txt -v
```

#### ファイル一覧表示

```bash
# 全マークダウンファイル表示
python main.py list-files

# パターン検索
python main.py list-files -p "articles"
```

## アーキテクチャ

### エージェント構成

- **RootAgent**: タスク分散と結果統合
- **EvidenceAgent**: エビデンス調査（MCP使用）
- **ProofreadingAgent**: 文章校閲（textlint MCP使用）

### MCP統合

- Firecrawl: Webサイト調査
- DeepWiki: OSSライブラリ調査  
- AWS Documentation: AWS情報調査
- textlint: 日本語文章校閲

## 設計原則

- ファイルは100行以内
- 独立性の高いモジュール設計
- 非同期処理による効率化