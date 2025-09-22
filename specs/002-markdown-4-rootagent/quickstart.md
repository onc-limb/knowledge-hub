# Quick Start: Markdown ファイル校正エージェントサービス

**Feature**: 002-markdown-4-rootagent  
**Date**: 2025 年 9 月 14 日

## 概要

このガイドでは、Markdown ファイル校正エージェントサービスの使用方法を段階的に説明します。初回セットアップから実際の使用までを 5 分で体験できます。

## 前提条件

- Python 3.13 以上
- Gemini API キー
- macOS/Linux/Windows（CLI 対応）

## セットアップ

### 1. インストール

```bash
# リポジトリクローン
git clone https://github.com/onc-limb/knowledge-hub.git
cd knowledge-hub

# 仮想環境作成とアクティベート
python3.13 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
uv pip install -e .
```

### 2. API キー設定

```bash
# 環境変数設定
export GEMINI_API_KEY="your-gemini-api-key-here"

# 永続化（bashの場合）
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 動作確認

```bash
# バージョン確認
markdown-proofreading --version

# ヘルプ表示
markdown-proofreading --help
```

## 基本的な使用方法

### 1. サンプルファイル作成

```bash
# テスト用Markdownファイル作成
cat > sample.md << 'EOF'
# AIの活用について

人工知能（AI）は現代社会で重要な役割を果たしています。特に機械学習の分野では、大きな進歩が見られる。

## 主要な技術

- 深層学習
- 自然言語処理
- コンピュータビジョン

これらの技術は様々な業界で応用され、効率性の向上に貢献している。しかし、倫理的な課題も存在するため、慎重な検討が必要である。

## 結論

AI技術の発展は止まることがない。私たちは適切にこの技術を活用し、社会全体の利益を追求すべきだ。
EOF
```

### 2. 基本実行

```bash
# 基本的な校正実行
markdown-proofreading sample.md
```

**期待される出力**:

```
✓ Markdownファイル読み込み完了: sample.md (0.8KB)
⚡ エビデンス調査開始...
⚡ 文章校正開始...
🔍 エビデンス調査完了 (6.2s) - 信頼度: 78%
📝 文章校正完了 (4.8s) - 可読性: 82%
📊 レポート生成中...
✅ レポート生成完了: reports/sample_20250914_143522_proofreading_report.md

総合評価: 80% | 処理時間: 12.4s
```

### 3. レポート確認

```bash
# 生成されたレポートを確認
cat reports/sample_20250914_143522_proofreading_report.md
```

## 詳細設定での実行

### 1. カスタム出力ディレクトリ

```bash
# 出力先を指定
mkdir my-reports
markdown-proofreading -o my-reports sample.md
```

### 2. 詳細ログ付き実行

```bash
# 詳細な進行状況を確認
markdown-proofreading -v sample.md
```

### 3. 高精度設定

```bash
# 深いエビデンス調査と厳密な校正
markdown-proofreading --evidence-depth deep --correction-level strict sample.md
```

### 4. JSON 形式出力

```bash
# 構造化データとして出力
markdown-proofreading -f json sample.md
```

## レポート内容の理解

生成されるレポートには以下のセクションが含まれます：

### 1. エグゼクティブサマリー

- 総合評価スコア
- 主要な改善点
- 推奨アクション

### 2. エビデンス調査結果

- 検証済み事実
- 疑問のある主張
- 根拠不足の項目

### 3. 文章校正結果

- 文法修正提案
- 表現改善案
- 構造改善提案

### 4. 統合改善提案

- 優先度付きアクションリスト
- 実装の難易度評価
- 期待される効果

## トラブルシューティング

### エラー: ファイルが見つからない

```bash
❌ エラー: ファイルが見つかりません: sample.md
```

**解決方法**:

- ファイルパスが正しいか確認
- 相対パスの場合は作業ディレクトリを確認

### エラー: API キーが設定されていない

```bash
❌ エラー: GEMINI_API_KEYが設定されていません
```

**解決方法**:

```bash
export GEMINI_API_KEY="your-api-key"
```

### エラー: タイムアウト

```bash
❌ エラー: 処理がタイムアウトしました (30秒)
```

**解決方法**:

```bash
# タイムアウト時間を延長
markdown-proofreading -t 60 large-file.md
```

### エラー: ファイルサイズ超過

```bash
❌ エラー: ファイルサイズが制限を超えています: large.md (15.2MB > 10MB)
```

**解決方法**:

- ファイルを分割して個別に処理
- 不要なコンテンツを削除

## 高度な使用例

### 1. 設定ファイル使用

```bash
# 設定ファイル例を生成
markdown-proofreading --config-example > config.yaml

# 設定を編集
vim config.yaml

# 設定ファイルで実行
markdown-proofreading --config config.yaml document.md
```

### 2. バッチ処理

```bash
# 複数ファイルの処理
for file in docs/*.md; do
    echo "Processing: $file"
    markdown-proofreading "$file"
done
```

### 3. CI/CD 統合

```bash
# GitHub Actions での使用例
name: Document Quality Check
on: [push]
jobs:
  proofreading:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install markdown-proofreading
      - name: Run proofreading
        run: |
          markdown-proofreading --quiet README.md
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

## 次のステップ

1. **設定ファイルの活用**: 繰り返し使用する設定を設定ファイルに保存
2. **自動化**: CI/CD パイプラインに組み込んで継続的な文書品質チェック
3. **カスタマイズ**: 特定のプロジェクト要件に合わせた設定調整
4. **フィードバック**: 結果を元にした文書作成プロセスの改善

## サポート

- **ドキュメント**: [プロジェクト Wiki](https://github.com/onc-limb/knowledge-hub/wiki)
- **Issue 報告**: [GitHub Issues](https://github.com/onc-limb/knowledge-hub/issues)
- **機能要求**: [Discussions](https://github.com/onc-limb/knowledge-hub/discussions)

## 制限事項

- 最大ファイルサイズ: 10MB
- 同時処理ファイル数: 1（並行エージェント実行は内部で処理）
- サポート言語: 日本語、英語
- 必要なインターネット接続: Gemini API 利用のため

---

これで基本的な使用方法は完了です。詳細な設定や高度な機能については、プロジェクトドキュメントを参照してください。
