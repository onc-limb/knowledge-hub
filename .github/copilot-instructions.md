## 使用ツール

Agent tool: Agent Development Kit (ADK)

- [ADK GitHub](https://github.com/google/adk-python/)

Python packages manager: uv

- [uv GitHub](https://github.com/astral-sh/uv)

## 現在の開発コンテキスト

### アクティブな機能開発

**Feature**: knowledges ディレクトリメタデータ生成機能 (001-knowledges-markdown)
**Tech Stack**: TypeScript/Node.js, fs/path modules
**Purpose**: knowledges 配下の Markdown ファイルを再帰的にスキャンし、階層的なメタデータを meta.json に生成

### プロジェクト構造

```
knowledge-hub/
├── knowledges/           # メタデータ生成対象ディレクトリ
│   ├── meta.json        # 出力ファイル（既存形式維持）
│   ├── ai/              # カテゴリディレクトリ
│   └── aws/             # サブカテゴリ対応
├── scripts/             # CLIツール
│   └── generate-metadata.ts
└── specs/001-knowledges-markdown/  # 設計文書
    ├── plan.md
    ├── data-model.md
    └── contracts/
```

### 開発方針

- **テスト駆動開発**: RED-GREEN-Refactor サイクル厳守
- **シンプル設計**: Node.js 標準ライブラリのみ使用
- **互換性維持**: 既存 meta.json 形式の完全継承
- **再帰構造**: 任意の深度のディレクトリ階層対応
