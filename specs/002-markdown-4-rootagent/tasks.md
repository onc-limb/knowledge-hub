# Tasks: Markdown ファイル校正エージェントサービス

**Input**: Design documents from `/specs/002-markdown-4-rootagent/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)

```
1. Load plan.md from feature directory
   → Extract: Python 3.13, Google ADK, Gemini 2.0 Flash, CLI architecture
2. Load design documents:
   → data-model.md: 5 entities (MarkdownFile, EvidenceResult, ProofreadingResult, IntegratedReport, TaskAssignment)
   → contracts/: CLI interface, Agent interfaces
   → research.md: ADK framework, asyncio architecture
3. Generate tasks by category:
   → Setup: Python project, ADK dependencies, Proofreading directory setup
   → Tests: CLI contract tests, Agent interface tests, Integration scenarios
   → Core: Data models, Agent implementations, CLI implementation
   → Integration: Async coordination, Progress reporting, File handling
   → Polish: Error handling, Performance tests, Documentation
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
```

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions

- **Implementation Directory**: `/Proofreading` (existing prototype replacement)
- **Source**: `Proofreading/` (agents/, config/, utils/)
- **Tests**: `tests/` at repository root
- Paths assume single project structure

## Phase 3.1: Setup

- [ ] T001 Create Python 3.13 virtual environment and setup uv package manager
- [ ] T002 Initialize Proofreading directory structure (agents/, config/, utils/, reports/)
- [ ] T003 [P] Install Google ADK and configure Gemini 2.0 Flash API dependencies
- [ ] T004 [P] Configure linting (pylint) and formatting (black) tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [ ] T005 [P] CLI interface contract test in tests/contract/cli-interface.test.ts
- [ ] T006 [P] Agent interfaces contract test in tests/contract/agent-interfaces.test.ts
- [ ] T007 [P] Basic CLI command test (markdown-proofreading --help) in tests/integration/basic-cli.test.ts
- [ ] T008 [P] File processing integration test in tests/integration/file-processing.test.ts
- [ ] T009 [P] Multi-agent coordination test in tests/integration/agent-coordination.test.ts
- [ ] T010 [P] Report generation test in tests/integration/report-generation.test.ts

## Phase 3.3: Core Data Models (ONLY after tests are failing)

- [ ] T011 [P] MarkdownFile model in Proofreading/utils/models.py
- [ ] T012 [P] EvidenceResult model in Proofreading/utils/models.py
- [ ] T013 [P] ProofreadingResult model in Proofreading/utils/models.py
- [ ] T014 [P] IntegratedReport model in Proofreading/utils/models.py
- [ ] T015 [P] TaskAssignment model in Proofreading/utils/models.py

## Phase 3.4: Base Agent Infrastructure

- [ ] T016 BaseAgent abstract class in Proofreading/agents/base_agent.py
- [ ] T017 Agent configuration management in Proofreading/config/agent_config.py
- [ ] T018 [P] File manager utilities in Proofreading/utils/file_manager.py
- [ ] T019 [P] Progress tracking utilities in Proofreading/utils/progress_tracker.py

## Phase 3.5: Agent Implementations

- [ ] T020 [P] EvidenceAgent implementation in Proofreading/agents/evidence_agent.py
- [ ] T021 [P] ProofreadingAgent implementation in Proofreading/agents/proofreading_agent.py
- [ ] T022 [P] ReportAgent implementation in Proofreading/agents/report_agent.py
- [ ] T023 RootAgent orchestration in Proofreading/agents/root_agent.py

## Phase 3.6: CLI Implementation

- [ ] T024 CLI argument parsing and validation in Proofreading/cli.py
- [ ] T025 Main CLI service orchestration in Proofreading/cli_service.py
- [ ] T026 CLI error handling and user feedback in Proofreading/cli.py
- [ ] T027 Progress bar and verbose logging in Proofreading/cli.py

## Phase 3.7: Integration & Configuration

- [ ] T028 Async agent coordination in Proofreading/agents/root_agent.py
- [ ] T029 Gemini API client configuration in Proofreading/config/llm_config.py
- [ ] T030 Report file output management in Proofreading/utils/file_manager.py
- [ ] T031 Timeout and retry logic in Proofreading/config/agent_config.py

## Phase 3.8: Polish & Validation

- [ ] T032 [P] Unit tests for data models in tests/unit/test_models.py
- [ ] T033 [P] Unit tests for utilities in tests/unit/test_utils.py
- [ ] T034 [P] Performance tests (<30s processing) in tests/performance/test_performance.py
- [ ] T035 [P] Error handling edge cases in tests/unit/test_error_handling.py
- [ ] T036 [P] Update project README.md with usage examples
- [ ] T037 [P] Create configuration example file in Proofreading/config/example.yaml
- [ ] T038 Run quickstart.md validation scenarios

## Dependencies

- Setup (T001-T004) before tests (T005-T010)
- Tests (T005-T010) before implementation (T011-T037)
- Data models (T011-T015) before agents (T016-T023)
- Base infrastructure (T016-T019) before agent implementations (T020-T023)
- Agent implementations (T020-T023) before CLI (T024-T027)
- CLI (T024-T027) before integration (T028-T031)
- Implementation before polish (T032-T038)

## Parallel Example

```bash
# Launch T005-T010 together (different test files):
Task: "CLI interface contract test in tests/contract/cli-interface.test.ts"
Task: "Agent interfaces contract test in tests/contract/agent-interfaces.test.ts"
Task: "Basic CLI command test in tests/integration/basic-cli.test.ts"
Task: "File processing integration test in tests/integration/file-processing.test.ts"
Task: "Multi-agent coordination test in tests/integration/agent-coordination.test.ts"
Task: "Report generation test in tests/integration/report-generation.test.ts"

# Launch T011-T015 together (data models in same file but independent):
Task: "MarkdownFile model in Proofreading/utils/models.py"
Task: "EvidenceResult model in Proofreading/utils/models.py"
Task: "ProofreadingResult model in Proofreading/utils/models.py"
Task: "IntegratedReport model in Proofreading/utils/models.py"
Task: "TaskAssignment model in Proofreading/utils/models.py"

# Launch T020-T022 together (different agent files):
Task: "EvidenceAgent implementation in Proofreading/agents/evidence_agent.py"
Task: "ProofreadingAgent implementation in Proofreading/agents/proofreading_agent.py"
Task: "ReportAgent implementation in Proofreading/agents/report_agent.py"
```

## Notes

- [P] tasks = different files or independent implementations
- Verify tests fail before implementing features
- Use pytest for all test implementations
- Follow TDD: RED (failing test) → GREEN (minimal implementation) → REFACTOR
- Commit after each major task completion
- CLI uses absolute paths for file handling
- Agent communication follows contract interfaces
- Progress updates every 500ms for user feedback

## Task Generation Rules

- Each contract file → contract test task marked [P]
- Each entity in data-model → model creation task marked [P]
- Each agent → implementation task marked [P] (different files)
- CLI components → sequential implementation (shared files)
- Integration tests → marked [P] (different scenarios)
- Unit tests → marked [P] (different test files)

## Key Features Implementation

- **Multi-agent Architecture**: RootAgent coordinates Evidence/Proofreading/Report agents
- **Async Processing**: Evidence and Proofreading agents run in parallel
- **Progress Tracking**: Real-time progress bars with 500ms updates
- **File Size Limits**: 10MB maximum with appropriate error handling
- **Output Formats**: Markdown (default), JSON, HTML support
- **CLI Configuration**: YAML config file support with examples
- **Error Resilience**: Partial failure tolerance (one agent can fail)
- **Performance Target**: <30 seconds total processing time

## Success Criteria

- All contract tests pass
- CLI processes sample Markdown files successfully
- Agents execute in parallel with proper coordination
- Reports generate in specified formats
- Performance meets <30s requirement
- Error handling covers all edge cases
- Documentation enables immediate usage
