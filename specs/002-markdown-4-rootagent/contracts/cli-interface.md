# CLI Contract: Markdown ファイル校正エージェントサービス

**Feature**: 002-markdown-4-rootagent  
**Date**: 2025 年 9 月 14 日

## CLI Interface Specification

### Command Structure

```bash
markdown-proofreading [OPTIONS] <file_path>
```

### Required Arguments

- `file_path`: 校正対象の Markdown ファイルパス（絶対パスまたは相対パス）

### Options

#### Basic Options

```bash
--output-dir, -o <path>     # レポート出力ディレクトリ（デフォルト: ./reports）
--format, -f <format>       # 出力形式: markdown, json, html（デフォルト: markdown）
--timeout, -t <seconds>     # タイムアウト時間（デフォルト: 30秒）
--verbose, -v               # 詳細ログ出力
--quiet, -q                 # 最小限の出力
```

#### Agent Control Options

```bash
--evidence-depth <level>    # エビデンス調査深度: basic, standard, deep（デフォルト: standard）
--correction-level <level>  # 校正レベル: basic, comprehensive, strict（デフォルト: comprehensive）
--language <lang>          # 言語設定: ja, en（デフォルト: ja）
```

#### Advanced Options

```bash
--config <config_file>      # 設定ファイルパス
--no-progress              # プログレスバー非表示
--parallel-limit <num>     # 並行処理数制限（デフォルト: 2）
--retry-attempts <num>     # 再試行回数（デフォルト: 3）
```

#### Information Options

```bash
--help, -h                 # ヘルプメッセージ表示
--version                  # バージョン情報表示
--list-languages          # サポート言語一覧
--config-example          # 設定ファイル例を表示
```

## Usage Examples

### 基本的な使用法

```bash
# 基本的な校正実行
markdown-proofreading document.md

# 出力ディレクトリ指定
markdown-proofreading -o ./my-reports document.md

# 詳細ログ付き実行
markdown-proofreading -v document.md
```

### 詳細設定

```bash
# 深い調査と厳密な校正
markdown-proofreading --evidence-depth deep --correction-level strict document.md

# タイムアウト延長
markdown-proofreading -t 60 large-document.md

# JSON形式出力
markdown-proofreading -f json document.md
```

### 設定ファイル使用

```bash
# 設定ファイルから実行
markdown-proofreading --config config.yaml document.md

# 設定例表示
markdown-proofreading --config-example > config.yaml
```

## Exit Codes

| Code | Description            |
| ---- | ---------------------- |
| 0    | 正常終了               |
| 1    | 一般的なエラー         |
| 2    | ファイルが見つからない |
| 3    | ファイル読み取りエラー |
| 4    | ファイルサイズ超過     |
| 5    | タイムアウト           |
| 6    | エージェント処理エラー |
| 7    | 設定エラー             |
| 8    | 出力書き込みエラー     |

## Output Format

### Standard Output (成功時)

```
✓ Markdownファイル読み込み完了: document.md (1.2KB)
⚡ エビデンス調査開始...
⚡ 文章校正開始...
🔍 エビデンス調査完了 (8.4s) - 信頼度: 85%
📝 文章校正完了 (6.2s) - 可読性: 78%
📊 レポート生成中...
✅ レポート生成完了: reports/document_20250914_143022_proofreading_report.md

総合評価: 81% | 処理時間: 15.8s
```

### Progress Bar Display

```
エビデンス調査  ████████░░ 80% (8.4s)
文章校正      ██████████ 100% (6.2s)
レポート生成   ███░░░░░░░ 30% (1.2s)
```

### Error Output (stderr)

```
❌ エラー: ファイルが見つかりません: /path/to/missing.md
💡 ヒント: ファイルパスを確認してください

詳細ログは --verbose オプションで確認できます
```

### Verbose Output

```bash
markdown-proofreading -v document.md
```

```
[INFO] 2025-09-14 14:30:22 - CLI starting with args: document.md
[INFO] 2025-09-14 14:30:22 - File validation passed: document.md (1.2KB)
[INFO] 2025-09-14 14:30:22 - RootAgent initialized
[INFO] 2025-09-14 14:30:22 - Starting parallel agent execution
[DEBUG] 2025-09-14 14:30:23 - EvidenceAgent: extracting claims
[DEBUG] 2025-09-14 14:30:25 - ProofreadingAgent: grammar analysis
[INFO] 2025-09-14 14:30:30 - EvidenceAgent completed (confidence: 85%)
[INFO] 2025-09-14 14:30:32 - ProofreadingAgent completed (readability: 78%)
[INFO] 2025-09-14 14:30:33 - ReportAgent: generating integrated report
[INFO] 2025-09-14 14:30:38 - Report saved: reports/document_20250914_143022_proofreading_report.md
```

## Configuration File Format

### YAML Configuration

```yaml
# config.yaml
output:
  directory: "./reports"
  format: "markdown"

agents:
  evidence:
    depth: "standard"
    timeout: 15
  proofreading:
    level: "comprehensive"
    language: "ja"
    timeout: 15
  report:
    template_style: "comprehensive"

processing:
  timeout: 30
  retry_attempts: 3
  parallel_limit: 2

logging:
  level: "INFO"
  show_progress: true

api:
  gemini_api_key: "${GEMINI_API_KEY}"
  rate_limit_per_minute: 60
```

## Environment Variables

```bash
# 必須
export GEMINI_API_KEY="your-api-key"

# オプション
export MARKDOWN_PROOFREADING_CONFIG="/path/to/config.yaml"
export MARKDOWN_PROOFREADING_OUTPUT_DIR="./reports"
export MARKDOWN_PROOFREADING_LOG_LEVEL="INFO"
```

## Input Validation

### File Path Validation

- 存在確認
- 読み取り権限確認
- ファイル拡張子チェック (.md, .markdown)
- ファイルサイズ制限 (10MB)

### Option Validation

- 数値オプションの範囲チェック
- 列挙値オプションの妥当性確認
- パスオプションの存在確認

### Error Messages

```bash
# ファイルエラー
❌ エラー: ファイルが見つかりません: document.md
❌ エラー: ファイルサイズが制限を超えています: document.md (15.2MB > 10MB)
❌ エラー: 読み取り権限がありません: document.md

# オプションエラー
❌ エラー: 無効な形式指定: 'pdf' (利用可能: markdown, json, html)
❌ エラー: タイムアウト値は1-300秒の範囲で指定してください: 500

# 設定エラー
❌ エラー: GEMINI_API_KEYが設定されていません
❌ エラー: 設定ファイルが無効です: config.yaml (line 5: invalid syntax)
```

## Help Messages

### Main Help

```bash
markdown-proofreading --help
```

```
Markdownファイル校正エージェントサービス v0.1.0

USAGE:
    markdown-proofreading [OPTIONS] <file_path>

ARGS:
    <file_path>    校正対象のMarkdownファイルパス

OPTIONS:
    -o, --output-dir <path>       レポート出力ディレクトリ [デフォルト: ./reports]
    -f, --format <format>         出力形式 [デフォルト: markdown] [選択肢: markdown, json, html]
    -t, --timeout <seconds>       タイムアウト時間 [デフォルト: 30]
    -v, --verbose                 詳細ログ出力
    -q, --quiet                   最小限の出力
    --evidence-depth <level>      エビデンス調査深度 [デフォルト: standard]
    --correction-level <level>    校正レベル [デフォルト: comprehensive]
    --language <lang>             言語設定 [デフォルト: ja]
    --config <config_file>        設定ファイルパス
    --no-progress                 プログレスバー非表示
    -h, --help                    このヘルプメッセージを表示
    --version                     バージョン情報を表示

EXAMPLES:
    markdown-proofreading document.md
    markdown-proofreading -o ./reports -f json document.md
    markdown-proofreading --evidence-depth deep --correction-level strict document.md

環境変数 GEMINI_API_KEY の設定が必要です。
詳細: https://github.com/onc-limb/knowledge-hub/tree/main/docs
```
