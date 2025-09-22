# Research: Markdown ファイル校正エージェントサービス

**Feature**: 002-markdown-4-rootagent  
**Date**: 2025 年 9 月 14 日

## 技術決定事項

### 1. Agent Framework 選択

**Decision**: Google ADK (Agent Development Kit)を使用  
**Rationale**:

- Python 3.13 との互換性が良好
- マルチエージェント管理機能が充実
- 並行処理サポート
- Gemini API 統合が容易

**Alternatives considered**:

- LangChain: 過度に複雑、憲法原則（シンプルさ）に反する
- CrewAI: 実行時依存関係が重い
- カスタム実装: 車輪の再発明、開発時間増大

### 2. LLM API 選択

**Decision**: Gemini 2.0 Flash API 使用  
**Rationale**:

- 高速レスポンス（30 秒以内要件に対応）
- 日本語処理能力が高い
- コスト効率が良好
- マルチモーダル対応（将来拡張性）

**Alternatives considered**:

- GPT-4: コスト高、API 制限
- Claude: レスポンス時間が長い
- ローカル LLM: 品質不安定、リソース要件大

### 3. 並行処理アーキテクチャ

**Decision**: asyncio + concurrent.futures 使用  
**Rationale**:

- Evidence Agent と Proofreading Agent の真の並行実行
- プログレスバー更新との両立
- エラーハンドリング統合容易

**Alternatives considered**:

- multiprocessing: オーバーヘッド大、Agent 状態共有困難
- threading: GIL 制約、I/O バウンドタスクには適用可能だが複雑

### 4. プログレスバー実装

**Decision**: rich.progress 使用  
**Rationale**:

- 美麗な CLI 表示
- 並行タスク進捗の視覚化
- エラー状態の表示サポート

**Alternatives considered**:

- tqdm: 機能不足、並行表示困難
- 自作進捗表示: 開発時間増大、品質不安定

### 5. ファイル構造と依存関係管理

**Decision**:

- pyproject.toml + uv 使用
- src/markdown_proofreading/構造
- CLI: src/markdown_proofreading/cli.py

**Rationale**:

- Python 3.13 対応
- 高速パッケージ管理
- モダン Python プロジェクト標準

**Alternatives considered**:

- poetry: 依存解決が遅い
- pip + requirements.txt: 依存管理機能不足

### 6. エラーハンドリング戦略

**Decision**:

- 構造化例外 hierarchy
- エージェント別エラー分類
- 復旧可能エラーの再試行機能

**Rationale**:

- 観測可能性要件対応
- ユーザーフレンドリなエラーメッセージ
- デバッグ容易性

### 7. 出力形式設計

**Decision**:

- Markdown 形式統合レポート
- 構造化セクション（エビデンス/校正/統合提案）
- タイムスタンプ付きファイル名

**Rationale**:

- ユーザー要件（Markdown 出力）
- 可読性最優先
- バージョン管理対応

## 実装方針

### アーキテクチャパターン

- Command Pattern: CLI → RootAgent
- Observer Pattern: プログレス通知
- Strategy Pattern: エージェント交換可能性

### テスト戦略

1. Contract Tests: エージェント間インターフェース
2. Integration Tests: 実ファイル使用
3. E2E Tests: CLI 全体フロー
4. Unit Tests: 個別エージェント機能

### パフォーマンス考慮事項

- ファイルサイズ制限: 10MB
- タイムアウト設定: 30 秒
- メモリ使用量監視
- 並行処理最適化

## リスク分析

### 高リスク

- Gemini API レート制限
- 大容量ファイル処理

### 中リスク

- エージェント間通信失敗
- プログレスバー表示崩れ

### 低リスク

- 依存関係競合
- CLI 引数解析

## 次フェーズへの推奨事項

1. data-model.md でエンティティ関係明確化
2. contracts/でエージェント間 API 定義
3. quickstart.md でユーザー体験検証
4. TDD 原則に従った段階的実装
