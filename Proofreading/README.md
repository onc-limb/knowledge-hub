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
uv sync
```

### 2. 環境設定

`.env.template`をコピーして`.env`ファイルを作成し、API キーを設定：

```bash
cp .env.template .env
# .envファイルを編集してAPIキーを設定
```

### 3. 使用方法

#### Markdown Proofreading Service

AI-powered markdown content analysis and improvement system built with coordinated agents.

## Features

- **Evidence Analysis**: Fact-checking and verification of claims
- **Proofreading**: Grammar and style checking
- **Integrated Reports**: Comprehensive analysis with actionable recommendations
- **CLI Interface**: Easy-to-use command-line interface
- **Concurrent Processing**: Parallel analysis for faster results

## Architecture

The system uses a coordinated multi-agent architecture:

- **RootAgent**: Orchestrates the entire workflow
- **EvidenceAgent**: Analyzes factual claims and evidence
- **ProofreadingAgent**: Checks grammar, style, and readability
- **ReportAgent**: Generates integrated reports with priority actions

## Installation

```bash
# Navigate to the Proofreading directory
cd Proofreading

# Install dependencies with uv
uv pip install -r requirements.txt
```

## Usage

### Basic Proofreading

```bash
# Analyze a single markdown file
python cli.py proofread -f path/to/article.md

# Specify output directory and options
python cli.py proofread -f article.md -o reports/ --depth deep --level strict
```

### List Available Files

```bash
# List markdown files in current directory
python cli.py list

# Search in specific directory with pattern
python cli.py list -d articles/ -p "*.md" --recursive
```

### Batch Processing

```bash
# Process multiple files
python cli.py batch -i articles/ -o reports/ --pattern "*.md" -w 3
```

### Advanced Options

- `--verification-depth`: Evidence verification level (basic, standard, deep)
- `--check-level`: Proofreading strictness (basic, standard, strict)
- `--concurrent`: Run analysis in parallel
- `--format`: Output format (text, json, markdown)

## API Usage

```python
from agents.root_agent import RootAgent
from utils.file_manager import FileManager

# Initialize components
root_agent = RootAgent()
file_manager = FileManager()

# Read markdown file
markdown_file = file_manager.read_markdown_file("article.md")

# Prepare input
input_data = {
    "content": markdown_file.content,
    "file_metadata": {
        "path": "article.md",
        "size_bytes": markdown_file.size_bytes,
        "encoding": markdown_file.encoding
    },
    "workflow_options": {
        "verification_depth": "standard",
        "check_level": "standard"
    }
}

# Run analysis
result = await root_agent.process(input_data)

# Access results
print(f"Overall score: {result['integrated_report']['overall_score']}")
```

## Testing

```bash
# Run individual agent tests
python test_evidence_simple.py
python test_proofreading_simple.py
python test_report_simple.py
python test_root_simple.py

# Run CLI tests
python test_cli_simple.py

# Run E2E integration tests
python test_integration_e2e.py
```

## Project Structure

```
Proofreading/
├── agents/
│   ├── base_agent.py          # Abstract base agent
│   ├── evidence_agent.py      # Evidence analysis
│   ├── proofreading_agent.py  # Grammar/style checking
│   ├── report_agent.py        # Report generation
│   └── root_agent.py          # Workflow coordination
├── utils/
│   ├── models.py              # Data models
│   ├── file_manager.py        # File operations
│   ├── progress_tracker.py    # Progress tracking
│   └── agent_config.py        # Configuration
├── config/
│   └── agent_config.py        # Agent configuration
├── cli.py                     # Command-line interface
├── main.py                    # Main entry point
└── test_*.py                  # Test files
```

## Configuration

The system supports various configuration options through the `workflow_options` parameter:

- **verification_depth**: Controls how thoroughly evidence is verified
- **check_level**: Sets the strictness of grammar and style checking
- **concurrent**: Enables parallel processing of evidence and proofreading

## Output Format

Reports include:

- **Executive Summary**: High-level overview of analysis
- **Evidence Analysis**: Fact-checking results with confidence scores
- **Proofreading Results**: Grammar issues, style problems, and suggestions
- **Priority Actions**: Ranked list of recommended improvements
- **Overall Score**: Combined quality assessment

## Development

Built with:

- Python 3.13
- asyncio for concurrent processing
- Click for CLI
- dataclasses for type-safe models
- TDD approach with comprehensive testing

## License

This project follows the specifications defined in `specs/002-markdown-4-rootagent/`.

## アーキテクチャ

### エージェント構成

- **RootAgent**: タスク分散と結果統合
- **EvidenceAgent**: エビデンス調査（MCP 使用）
- **ProofreadingAgent**: 文章校閲（textlint MCP 使用）

### MCP 統合

- Firecrawl: Web サイト調査
- DeepWiki: OSS ライブラリ調査
- AWS Documentation: AWS 情報調査
- textlint: 日本語文章校閲

## 設計原則

- ファイルは 100 行以内
- 独立性の高いモジュール設計
- 非同期処理による効率化
