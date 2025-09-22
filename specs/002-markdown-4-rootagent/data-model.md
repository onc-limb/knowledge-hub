# Data Model: Markdown ファイル校正エージェントサービス

**Feature**: 002-markdown-4-rootagent  
**Date**: 2025 年 9 月 14 日

## エンティティ概要

システムは 4 つのコアエンティティで構成され、エージェント間でデータを交換しながら処理を進めます。

## Core Entities

### 1. MarkdownFile

**Purpose**: 校正対象の Markdown ファイルを表現

**Attributes**:

- `file_path: str` - ファイルパス（絶対パス）
- `content: str` - ファイル内容（UTF-8）
- `size_bytes: int` - ファイルサイズ
- `created_at: datetime` - 処理開始時刻
- `encoding: str` - 文字エンコーディング（デフォルト: UTF-8）

**Validation Rules**:

- file_path: 存在するファイル、読み取り権限あり
- size_bytes: 0 < size <= 10MB
- content: 空文字列も許可（空ファイル処理）

**State Transitions**:

```
PENDING → LOADED → PROCESSING → COMPLETED | FAILED
```

### 2. EvidenceResult

**Purpose**: エビデンス調査エージェントの結果

**Attributes**:

- `agent_id: str` - エージェント識別子
- `verified_facts: List[VerifiedFact]` - 検証済み事実
- `questionable_claims: List[QuestionableClaim]` - 疑問のある主張
- `missing_evidence: List[MissingEvidence]` - 根拠不足項目
- `recommendations: List[str]` - 改善推奨事項
- `confidence_score: float` - 0.0-1.0 の信頼度
- `processing_time: float` - 処理時間（秒）
- `error_message: Optional[str]` - エラー詳細

**Related Entities**:

- **VerifiedFact**: `claim: str, evidence: str, source: str, confidence: float`
- **QuestionableClaim**: `claim: str, reason: str, severity: str`
- **MissingEvidence**: `claim: str, required_evidence: str, suggestion: str`

### 3. ProofreadingResult

**Purpose**: 文章校正エージェントの結果

**Attributes**:

- `agent_id: str` - エージェント識別子
- `grammar_fixes: List[GrammarFix]` - 文法修正
- `style_improvements: List[StyleImprovement]` - 表現改善
- `structure_suggestions: List[StructureSuggestion]` - 構造改善
- `readability_score: float` - 0.0-1.0 の可読性スコア
- `processing_time: float` - 処理時間（秒）
- `error_message: Optional[str]` - エラー詳細

**Related Entities**:

- **GrammarFix**: `line_number: int, original: str, corrected: str, rule: str`
- **StyleImprovement**: `line_number: int, suggestion: str, category: str, priority: str`
- **StructureSuggestion**: `section: str, improvement: str, rationale: str`

### 4. IntegratedReport

**Purpose**: 最終的な統合レポート

**Attributes**:

- `report_id: str` - レポート一意識別子（UUID）
- `original_file: MarkdownFile` - 元ファイル情報
- `evidence_result: EvidenceResult` - エビデンス調査結果
- `proofreading_result: ProofreadingResult` - 校正結果
- `executive_summary: str` - 要約
- `priority_actions: List[PriorityAction]` - 優先対応事項
- `overall_score: float` - 0.0-1.0 の総合評価
- `generated_at: datetime` - レポート生成時刻
- `file_path: str` - 保存先パス

**Related Entities**:

- **PriorityAction**: `action: str, category: str, priority: int, effort: str`

### 5. TaskAssignment

**Purpose**: エージェント間のタスク管理

**Attributes**:

- `task_id: str` - タスク一意識別子
- `agent_type: str` - エージェント種別（evidence/proofreading/report）
- `status: str` - PENDING/RUNNING/COMPLETED/FAILED
- `input_data: dict` - エージェントへの入力データ
- `result: Optional[dict]` - 処理結果
- `started_at: Optional[datetime]` - 開始時刻
- `completed_at: Optional[datetime]` - 完了時刻
- `error_details: Optional[str]` - エラー詳細

## データフロー

```
1. MarkdownFile ──→ RootAgent
                    ├─→ TaskAssignment(evidence) ──→ EvidenceResult
                    └─→ TaskAssignment(proofreading) ──→ ProofreadingResult

2. EvidenceResult + ProofreadingResult ──→ TaskAssignment(report) ──→ IntegratedReport

3. IntegratedReport ──→ File System (reports/)
```

## バリデーション制約

### ファイルサイズ制限

- 最大 10MB
- エラー時の適切なメッセージ

### 文字エンコーディング

- UTF-8 優先
- 自動検出機能

### 並行処理制約

- EvidenceAgent と ProofreadingAgent は同時実行
- ReportAgent は両者完了後に実行

### エラーハンドリング

- 部分的失敗許容（片方のエージェントが失敗してもレポート生成）
- 構造化エラー情報

## パフォーマンス要件

### メモリ使用量

- ファイル内容: 最大 10MB
- 結果データ: 最大 5MB
- 総計 15MB 以下

### 処理時間

- 全体処理: 30 秒以内
- プログレス更新: 500ms 間隔

## セキュリティ考慮事項

### ファイルアクセス

- 読み取り専用操作
- パストラバーサル防止
- 権限チェック

### データ保護

- 一時的メモリ保持
- 機密情報ログ出力禁止
