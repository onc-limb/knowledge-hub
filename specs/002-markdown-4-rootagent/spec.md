# Feature Specification: Markdown ファイル校正エージェントサービス

**Feature Branch**: `002-markdown-4-rootagent`  
**Created**: 2025 年 9 月 14 日  
**Status**: Draft  
**Input**: User description: "指定したパスの markdown ファイルの内容を読み取り、エビデンス調査と文章校正を行うエージェントサービス。エージェントは 4 つ、タスクを割り振る RootAgent, エビデンス調査をする evidence_agent, 文章の校正をする proofreading_agent,そしてエビデンス調査と文章校正の結果を下にレポートを作成する report_agent です。パスを受け取ったら、ルートエージェントはそのパスの示すファイルのコンテンツを取得して、evidence_agent と proofreading_agent にそれぞれのタスクを割り振ります。二つのエージェントのタスクが完了したら、その結果を元に report_agent にタスクを振ります。report_agent のタスク結果を reports ディレクトリ配下に格納して完了。"

## Execution Flow (main)

```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identified: 4-agent system (root, evidence, proofreading, report), markdown file processing, task orchestration
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → Clear user flow: file path → content extraction → parallel processing → report generation
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines

- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing

### Primary User Story

ユーザーは Markdown ファイルの品質向上を求めています。指定したファイルパスの Markdown ファイルに対して、内容の事実確認（エビデンス調査）と文章の校正を同時に実行し、包括的な改善レポートを受け取りたいと考えています。

### Acceptance Scenarios

1. **Given** 有効な Markdown ファイルパス, **When** ユーザーがサービスを実行, **Then** ファイル内容が読み取られ、エビデンス調査と文章校正が並行実行される
2. **Given** エビデンス調査と文章校正が完了, **When** 両方の結果が利用可能, **Then** 統合レポートが生成され reports ディレクトリに保存される
3. **Given** 存在しないファイルパス, **When** ユーザーがサービス実行を試行, **Then** 適切なエラーメッセージが表示される
4. **Given** 空の Markdown ファイル, **When** サービスが実行される, **Then** 空ファイルに対する適切なレポートが生成される

### Edge Cases

- 非常に大きな Markdown ファイル（数 MB）が指定された場合の処理
- ファイル読み取り権限がない場合のエラーハンドリング
- エビデンス調査またはプルーフリーディングエージェントのいずれかが失敗した場合の処理
- reports ディレクトリが存在しない場合の自動作成

## Requirements

### Functional Requirements

- **FR-001**: システムは Markdown ファイルパスを入力として受け取り、ファイル内容を読み取る必要がある
- **FR-002**: システムはルートエージェントを通じてタスクを他のエージェントに適切に振り分ける必要がある
- **FR-003**: システムはエビデンス調査エージェントとプルーフリーディングエージェントを並行実行する必要がある
- **FR-004**: エビデンス調査エージェントは文章内の事実や主張に対する根拠の確認を実行する必要がある
- **FR-005**: プルーフリーディングエージェントは文法、表現、構造の改善提案を実行する必要がある
- **FR-006**: システムは両エージェントの結果を統合したレポートを生成する必要がある
- **FR-007**: 生成されたレポートは reports ディレクトリに一意のファイル名で保存される必要がある
- **FR-008**: システムは無効なファイルパスに対して適切なエラーメッセージを提供する必要がある
- **FR-009**: システムは処理の進行状況をプログレスバーでユーザーに通知する必要がある

### Key Entities

- **MarkdownFile**: 校正対象となる Markdown ファイル、ファイルパス、内容、メタデータを含む
- **EvidenceResult**: エビデンス調査の結果、検証された事実、疑問点、推奨事項を含む
- **ProofreadingResult**: 文章校正の結果、文法修正、表現改善、構造改善提案を含む
- **IntegratedReport**: 統合レポート、両エージェントの結果、総合的な改善提案、優先度付けされた推奨事項を含む
- **TaskAssignment**: エージェントへのタスク割り当て、担当エージェント、処理状況、結果を含む

---

## Review & Acceptance Checklist

### Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
