# Implementation Plan: Markdown ファイル校正エージェントサービス

**Branch**: `002-markdown-4-rootagent` | **Date**: 2025 年 9 月 14 日 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-markdown-4-rootagent/spec.md`

## Execution Flow (/plan command scope)

```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:

- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

Markdown ファイルの内容に対してエビデンス調査と文章校正を並行実行する 4 エージェントシステム。RootAgent がタスクを調整し、Evidence/ProofreadingAgent が専門処理を実行し、ReportAgent が統合レポートを生成して reports ディレクトリに保存する。

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: Google ADK (Agent Development Kit), google-generativeai (gemini-2.0-flash)  
**Storage**: ファイルシステム (Markdown ファイル読み込み、reports ディレクトリ出力)  
**Testing**: pytest (TDD 原則に従った実装)  
**Target Platform**: ローカル PC CLI 環境 (macOS/Linux/Windows 対応) - web アプリケーション公開は対象外
**Project Type**: single - ローカル CLI ツール構造  
**Performance Goals**: 小〜中規模 Markdown ファイル (<10MB) の処理、レスポンス時間 <30 秒  
**Constraints**: プログレスバー表示必須、並行エージェント実行、エラーハンドリング完備  
**Scale/Scope**: 個人/小チーム向けローカルツール、同時実行 3-4 エージェント、1 ファイル単位処理
**Implementation Directory**: /Proofreading (既存プロトタイプの置き換え)

**User Technical Context**: 使用言語 python 3.13, agent サービス Google ADK, 使用する LLM gemini-2.0-flash, 入力は markdown ファイルのパス、出力は markdown 形式, 処理の実行は cli 上から行う。本サービスはローカル PC で cli を通じて実行されることを想定し、web application として公開することは考慮していない。

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

**Simplicity**:

- Projects: 1 (CLI tool with library structure) ✅
- Using framework directly? Google ADK 直接使用、ラッパークラス最小限 ✅
- Single data model? MarkdownFile, EvidenceResult, ProofreadingResult, IntegratedReport ✅
- Avoiding patterns? Repository/UoW 不使用、直接ファイル I/O ✅

**Architecture**:

- EVERY feature as library? MarkdownProofreading ライブラリ + ローカル CLI ✅
- Libraries listed:
  - markdown-proofreading-lib (/Proofreading 内: 4 エージェント + オーケストレーション)
- CLI per library: --input, --output, --help, --version, --format ✅
- Library docs: llms.txt format planned? ✅

**Testing (NON-NEGOTIABLE)**:

- RED-GREEN-Refactor cycle enforced? ✅ 計画済み
- Git commits show tests before implementation? ✅ コミット戦略含む
- Order: Contract→Integration→E2E→Unit strictly followed? ✅
- Real dependencies used? 実際のファイルシステム、実際の Gemini API ✅
- Integration tests for: 新ライブラリ、エージェント間通信、レポート生成 ✅
- FORBIDDEN: Implementation before test, skipping RED phase ✅

**Observability**:

- Structured logging included? ✅ エージェント処理状況、エラー詳細
- CLI output unified? ローカル CLI 出力 + プログレスバー ✅
- Error context sufficient? ファイルパス、エージェント名、処理段階 ✅

**Versioning**:

- Version number assigned? 0.1.0 (MAJOR.MINOR.BUILD) ✅
- BUILD increments on every change? ✅
- Breaking changes handled? ✅ 初回実装のため該当なし

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)

```
### Source Code (/Proofreading directory)
```

# ローカル CLI ツール構造 (/Proofreading 内に実装)

Proofreading/
├── agents/
│ ├── **init**.py
│ ├── base_agent.py
│ ├── root_agent.py
│ ├── evidence_agent.py
│ ├── proofreading_agent.py
│ └── report_agent.py
├── models/
│ ├── **init**.py
│ ├── markdown_file.py
│ ├── evidence_result.py
│ ├── proofreading_result.py
│ ├── integrated_report.py
│ └── task_assignment.py
├── cli/
│ ├── **init**.py
│ ├── main.py
│ └── cli_service.py
├── utils/
│ ├── **init**.py
│ ├── file_manager.py
│ ├── progress_tracker.py
│ └── error_handler.py
├── config/
│ ├── **init**.py
│ └── settings.py
├── tests/
│ ├── contract/
│ ├── integration/
│ ├── unit/
│ └── fixtures/
├── reports/
├── pyproject.toml
├── README.md
└── main.py

```

**Structure Decision**: /Proofreading内のローカルCLIツール構造（既存プロトタイプ置き換え）
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:

   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts

_Prerequisites: research.md complete_

1. **Extract entities from feature spec** → `data-model.md`:

   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:

   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:

   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:

   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/bash/update-agent-context.sh copilot` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/\*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach

_This section describes what the /tasks command will do - DO NOT execute during /plan_

**Task Generation Strategy**:

- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data-model, quickstart)
- Each contract → contract test task [P] (RootAgent, EvidenceAgent, ProofreadingAgent, ReportAgent)
- Each entity → model creation task [P] (MarkdownFile, EvidenceResult, ProofreadingResult, IntegratedReport, TaskAssignment)
- Each user story → integration test task (File reading, Parallel processing, Report generation)
- Implementation tasks to make tests pass following TDD principles

**Ordering Strategy**:

- TDD order: Tests before implementation (RED-GREEN-Refactor cycle)
- Dependency order: Models → Agents → CLI → Integration
- Infrastructure first: Error handling, Logging, Configuration
- Mark [P] for parallel execution (independent files)

**Task Categories**:

1. **Project Setup** (4 tasks): pyproject.toml, directory structure, dependencies, config
2. **Data Models** (5 tasks): Entity classes with validation
3. **Agent Contracts** (4 tasks): Abstract base classes and interfaces
4. **Agent Implementation** (4 tasks): Concrete agent classes
5. **CLI Interface** (3 tasks): Command parsing, argument validation, main execution
6. **Testing** (12 tasks): Contract tests, integration tests, E2E tests
7. **Documentation** (3 tasks): API docs, user guide, deployment guide

**Estimated Output**: 35-40 numbered, ordered tasks in tasks.md with clear dependencies

**Quality Gates**:

- Each task must include acceptance criteria
- Tests written before implementation (constitutional requirement)
- Parallel tasks clearly marked for efficiency
- Integration points explicitly defined

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation

_These phases are beyond the scope of the /plan command_

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking

_Fill ONLY if Constitution Check has violations that must be justified_

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |

## Progress Tracking

_This checklist is updated during execution flow_

**Phase Status**:

- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:

- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---

_Based on Constitution v2.1.1 - See `/memory/constitution.md`_
