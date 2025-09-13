# Implementation Plan: knowledges ディレクトリメタデータ生成機能

**Branch**: `001-knowledges-markdown` | **Date**: 2025 年 9 月 14 日 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-knowledges-markdown/spec.md`

## Execution Flow (/plan command scope)

```
1. Load feature spec from Input path ✓
   → Feature spec loaded successfully
2. Fill Technical Context (scan for NEEDS CLARIFICATION) ✓
   → Detect Project Type: single (Node.js/TypeScript utility)
   → Set Structure Decision: Option 1 (single project)
3. Evaluate Constitution Check section below ✓
   → No violations detected in initial constitution check
   → Update Progress Tracking: Initial Constitution Check ✓
4. Execute Phase 0 → research.md ✓
   → All technical aspects are clear from existing codebase
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file ✓
6. Re-evaluate Constitution Check section ✓
   → No new violations detected
   → Update Progress Tracking: Post-Design Constitution Check ✓
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md) ✓
8. STOP - Ready for /tasks command ✓
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:

- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

knowledges 配下の Markdown ファイルを再帰的にスキャンし、カテゴリ・サブカテゴリ・ファイル統計を含む階層的なメタデータを meta.json に生成する機能。TypeScript による Node.js CLI ツールとして実装し、既存の scripts/generate-metadata.ts を拡張して深い階層構造に対応する。

## Technical Context

**Language/Version**: TypeScript/Node.js (既存プロジェクトに合わせて)  
**Primary Dependencies**: Node.js fs/path modules, TypeScript  
**Storage**: /knowledges/meta.json (JSON ファイル出力)  
**Testing**: Node.js built-in test runner または Jest  
**Target Platform**: Node.js 環境 (開発者のローカル環境)
**Project Type**: single (既存の knowledge-hub プロジェクトに統合)  
**Performance Goals**: 1000 ファイル未満のスキャンを 1 秒以内  
**Constraints**: 既存の meta.json 形式との互換性維持が必須  
**Scale/Scope**: knowledges 配下の全 Markdown ファイル (現在約 20 ファイル、将来的に数百ファイル程度)

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

**Simplicity**:

- Projects: 1 (既存プロジェクトに統合)
- Using framework directly? ✓ (Node.js 標準ライブラリ使用)
- Single data model? ✓ (Category/SubCategory 構造のみ)
- Avoiding patterns? ✓ (シンプルなファイルスキャン処理)

**Architecture**:

- EVERY feature as library? ✓ (metadata-generator ライブラリとして実装)
- Libraries listed: metadata-generator (Markdown ファイルスキャンとメタデータ生成)
- CLI per library: ✓ (generate-metadata --help/--version/--format)
- Library docs: llms.txt format planned? ✓

**Testing (NON-NEGOTIABLE)**:

- RED-GREEN-Refactor cycle enforced? ✓ (テスト先行開発)
- Git commits show tests before implementation? ✓
- Order: Contract→Integration→E2E→Unit strictly followed? ✓
- Real dependencies used? ✓ (実際のファイルシステム使用)
- Integration tests for: 新ライブラリ、実ファイル操作
- FORBIDDEN: Implementation before test, skipping RED phase ✓

**Observability**:

- Structured logging included? ✓ (処理状況とエラー詳細)
- Frontend logs → backend? N/A (CLI ツール)
- Error context sufficient? ✓

**Versioning**:

- Version number assigned? 1.0.0 (新機能)
- BUILD increments on every change? ✓
- Breaking changes handled? ✓ (既存形式維持で後方互換性保証)
- Using framework directly? (no wrapper classes)
- Single data model? (no DTOs unless serialization differs)
- Avoiding patterns? (no Repository/UoW without proven need)

**Architecture**:

- EVERY feature as library? (no direct app code)
- Libraries listed: [name + purpose for each]
- CLI per library: [commands with --help/--version/--format]
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:

- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Git commits show tests before implementation?
- Order: Contract→Integration→E2E→Unit strictly followed?
- Real dependencies used? (actual DBs, not mocks)
- Integration tests for: new libraries, contract changes, shared schemas?
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:

- Structured logging included?
- Frontend logs → backend? (unified stream)
- Error context sufficient?

**Versioning**:

- Version number assigned? (MAJOR.MINOR.BUILD)
- BUILD increments on every change?
- Breaking changes handled? (parallel tests, migration plan)

## Project Structure

### Documentation (this feature)

```
specs/001-knowledges-markdown/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)

```
# Option 1: Single project (DEFAULT)
src/
├── metadata-generator/  # 新ライブラリ
│   ├── index.ts
│   ├── scanner.ts
│   └── types.ts
├── cli/
│   └── generate-metadata.ts  # 既存スクリプト拡張
└── lib/

tests/
├── contract/
├── integration/
│   └── metadata-generator.test.ts
└── unit/
    └── scanner.test.ts
```

**Structure Decision**: Option 1 (既存の knowledge-hub プロジェクトに統合)
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)

backend/
├── src/
│ ├── models/
│ ├── services/
│ └── api/
└── tests/

frontend/
├── src/
│ ├── components/
│ ├── pages/
│ └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)

api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]

```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research
既存のプロジェクト構造とscripts/generate-metadata.tsを分析済み。技術的な不明点はなく、以下の技術選択が明確:

1. **TypeScript/Node.js**: 既存プロジェクトとの整合性
2. **ファイルシステムAPI**: Node.js標準のfs/pathモジュール
3. **既存形式**: categories配列構造の維持
4. **再帰処理**: ディレクトリ階層の深度制限なし

**Output**: research.md (技術調査結果)

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Category, SubCategory エンティティ
   - ファイル統計とメタデータ構造
   - 階層関係とポイント計算ルール

2. **Generate API contracts** from functional requirements:
   - CLIインターフェース仕様
   - 入力: knowledgesディレクトリパス
   - 出力: meta.json更新

3. **Generate contract tests** from contracts:
   - CLI実行テスト
   - JSON出力形式検証
   - エラーハンドリングテスト

4. **Extract test scenarios** from user stories:
   - ファイル追加/削除シナリオ
   - 深い階層構造テスト
   - 既存形式互換性テスト

5. **Update agent file incrementally**:
   - GitHub Copilot instructions更新
   - 新技術スタック情報追加

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, .github/copilot-instructions.md

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

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P]
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order: Types → Scanner → CLI → Integration
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*No constitution violations detected - this section intentionally left empty*

## Progress Tracking
*This checklist is updated during execution flow*

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
- [x] Complexity deviations documented (none)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
```
