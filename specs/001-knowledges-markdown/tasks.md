# Tasks: knowledges ディレクトリメタデータ生成機能（既存実装の改良）

**Input**: Design documents from `/specs/001-knowledges-markdown/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/
**Note**: 既存の `/scripts/generate-metadata.ts` の機能改良タスク

## Execution Flow (main)

```
1. Load plan.md from feature directory ✓
   → Tech stack: TypeScript/Node.js, fs/path modules
   → Structure: Single project (既存プロジェクトに統合)
2. Load optional design documents: ✓
   → data-model.md: Category/SubCategory/MetadataCollection entities
   → contracts/: CLI interface, Library API contracts
   → research.md: Node.js標準ライブラリ、同期処理選択
3. Analyze existing implementation: ✓
   → Current: 固定3階層制限 (subSubCategories) - 無制限階層への改良が必要
   → Current: All files included (not just .md)
   → Current: totalFiles, lastUpdated metadata
4. Generate improvement tasks: ✓
   → Setup: Testing環境、型定義改良
   → Tests: 既存機能のテスト追加
   → Enhancement: 無制限階層対応、.mdフィルタ、CLIオプション
   → Refactoring: コード整理、エラーハンドリング改善
   → Polish: パフォーマンス、ドキュメント
5. Apply task rules: ✓
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
6. Number tasks sequentially (T001, T002...) ✓
7. Generate dependency graph ✓
8. Create parallel execution examples ✓
9. Return: SUCCESS (tasks ready for execution) ✓
```

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below are based on plan.md structure decision

## Phase 3.1: Setup & Analysis

- [ ] T001 Analyze existing implementation in scripts/generate-metadata.ts
- [ ] T002 Create test directory structure for existing functionality
- [ ] T003 [P] Setup TypeScript testing configuration for the existing script

## Phase 3.2: Tests for Existing Functionality (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests cover existing behavior and MUST PASS with current implementation**

- [ ] T004 [P] Contract test for current CLI usage: `node scripts/generate-metadata.ts`
- [ ] T005 [P] Integration test for unlimited depth hierarchy (categories→subCategories 無制限再帰)
- [ ] T006 [P] Integration test for current file counting behavior (all files, not just .md)
- [ ] T007 [P] Integration test for totalFiles and lastUpdated metadata fields
- [ ] T008 [P] Integration test for hierarchy console output display
- [ ] T009 [P] Unit test for existing scanDirectory function behavior
- [ ] T010 [P] Unit test for countFilesRecursively function

## Phase 3.3: Enhancement Implementation (ONLY after tests are passing)

- [ ] T011 Add CLI argument parsing (--help, --version, --format options)
- [ ] T012 Add markdown-only filtering option (--md-only flag)
- [ ] T013 Implement unlimited depth hierarchy (remove any depth limits)
- [ ] T014 [P] Add proper TypeScript type definitions for existing interfaces
- [ ] T015 [P] Add error handling improvements to scanDirectory function
- [ ] T016 [P] Add validation for input directory and file permissions
- [ ] T017 Add backward compatibility mode (--legacy for fixed depth hierarchy)

## Phase 3.4: Integration & Enhancement

- [ ] T018 Integrate new CLI options with existing generateMetadata function
- [ ] T019 Add structured logging to existing console output
- [ ] T020 Implement backward-compatible JSON output format
- [ ] T021 Add performance monitoring to existing file counting operations

## Phase 3.5: Polish & Documentation

- [ ] T022 [P] Unit tests for new CLI option parsing
- [ ] T023 [P] Unit tests for markdown filtering functionality
- [ ] T024 [P] Unit tests for unlimited depth scanning
- [ ] T025 Performance tests (compare unlimited depth with existing implementation performance)
- [ ] T026 [P] Update quickstart.md with new CLI options
- [ ] T027 [P] Create documentation for backward compatibility options
- [ ] T028 Refactor existing code for better maintainability
- [ ] T029 Manual validation using existing knowledges directory structure

## Dependencies

```
Setup (T001-T003) → Tests for Current (T004-T010) → Enhancements (T011-T017) → Integration (T018-T021) → Polish (T022-T029)

Specific dependencies:
- T001 (analysis) blocks all other tasks - must understand existing implementation first
- T004-T010 (existing functionality tests) must PASS before enhancements
- T011-T017 can run in parallel where marked [P]
- T013 (unlimited depth) requires T005 (unlimited depth test) to pass first
- T012 (markdown filtering) is independent enhancement
- Performance tests (T025) require existing and new implementations for comparison
```

## Parallel Example

```
# Phase 3.2 - Test existing functionality:
Task: "Contract test for current CLI usage: node scripts/generate-metadata.ts"
Task: "Integration test for 3-level hierarchy structure"
Task: "Integration test for all-files counting behavior"
Task: "Unit test for scanDirectory function behavior"

# Phase 3.3 - Enhancement implementation:
Task: "Add proper TypeScript type definitions"
Task: "Add error handling improvements"
Task: "Add validation for input directory"

# Phase 3.5 - Polish tasks:
Task: "Unit tests for CLI option parsing"
Task: "Unit tests for markdown filtering"
Task: "Update quickstart.md with new options"
Task: "Create backward compatibility documentation"
```

```
Setup (T001-T003) → Tests (T004-T011) → Implementation (T012-T022) → Polish (T023-T030)

Specific dependencies:
- T012 (types) blocks T013, T014, T016, T017
- T013 (scanner) blocks T014, T015
- T014 (core logic) blocks T015, T019
- T015 (CLI) blocks T019
- Tests (T004-T011) must fail before implementation starts
- Integration (T019-T022) before polish (T023-T030)
```

## Parallel Example

```
# Phase 3.2 - Launch contract tests together:
Task: "Contract test CLI interface basic usage in tests/contract/cli-interface.test.ts"
Task: "Contract test CLI options in tests/contract/cli-options.test.ts"
Task: "Contract test library API scanDirectorySync in tests/contract/library-api.test.ts"
Task: "Contract test library API generateMetadata in tests/contract/library-api-metadata.test.ts"

# Phase 3.2 - Launch integration tests together:
Task: "Integration test unlimited depth hierarchy scanning in tests/integration/unlimited-depth.test.ts"
Task: "Integration test recursive directory processing in tests/integration/recursive-scan.test.ts"
Task: "Integration test metadata generation in tests/integration/metadata-generation.test.ts"
Task: "Integration test existing meta.json compatibility in tests/integration/compatibility.test.ts"

# Phase 3.3 - Launch core implementation together:
Task: "Type definitions in src/metadata-generator/types.ts"
Task: "Directory scanner implementation in src/metadata-generator/scanner.ts"
Task: "Metadata generator core logic in src/metadata-generator/index.ts"

# Phase 3.5 - Launch unit tests together:
Task: "Unit tests for scanner utilities in tests/unit/scanner-utils.test.ts"
Task: "Unit tests for validation rules in tests/unit/validation.test.ts"
Task: "Unit tests for calculations in tests/unit/calculations.test.ts"
```

## Notes

- [P] tasks = different files, no dependencies
- **CRITICAL**: First understand existing implementation before making changes
- Tests for existing functionality must PASS (not fail) - we're testing current behavior
- New enhancements should be additive and backward compatible
- Preserve existing meta.json output format (add fields, don't remove)
- Keep 3-level hierarchy as default, add unlimited depth as option
- Focus on improving existing code rather than complete rewrite

## Task Generation Rules Applied

1. **From Existing Implementation**:

   - Current CLI usage → T004 (contract test)
   - 3-level hierarchy → T005, T013 (test current, enhance with unlimited)
   - All file types → T006, T012 (test current, add markdown filtering)

2. **From Data Model** (enhanced to match existing):

   - CategoryMetadata interface → T014 (improve type definitions)
   - subSubCategories field → T005 (test existing structure)
   - totalFiles/lastUpdated → T007 (test existing metadata)

3. **From Contracts** (adapted to existing):

   - CLI interface → T011 (add options to existing script)
   - Library API → T018-T021 (integrate with existing functions)

4. **From User Stories** (backward compatible):
   - Enhanced functionality → T012, T013 (additive improvements)
   - Existing behavior preservation → T004-T010 (regression prevention)

## Validation Checklist

_GATE: Checked before task execution_

- [x] Existing implementation analyzed (T001)
- [x] Current behavior tests come before enhancements (T004-T010 → T011-T017)
- [x] Backward compatibility preserved throughout
- [x] Parallel tasks truly independent (different files/functions)
- [x] Each task specifies exact file path or function
- [x] No task breaks existing functionality
- [x] Enhancements are additive, not replacements
- [x] Performance comparison with existing implementation planned (T025)
