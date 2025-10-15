# Agent Contracts: Markdown ファイル校正エージェントサービス

**Feature**: 002-markdown-4-rootagent  
**Date**: 2025 年 9 月 14 日

## 概要

エージェント間の契約は、Python の抽象基底クラス（ABC）とプロトコルで定義されます。各エージェントは標準化されたインターフェースを実装し、型安全性を保証します。

## Base Agent Contract

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class BaseAgent(ABC):
    """全エージェントの基底クラス"""

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        メイン処理メソッド

        Args:
            input_data: エージェント固有の入力データ

        Returns:
            処理結果辞書

        Raises:
            AgentProcessingError: 処理中のエラー
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """入力データのバリデーション"""
        pass

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """エージェントタイプ識別子"""
        pass
```

## 1. Root Agent Contract

**Purpose**: タスク調整とオーケストレーション

### Input Interface

```python
class RootAgentInput:
    file_path: str          # Markdownファイルパス
    output_dir: str         # レポート出力ディレクトリ
    timeout: int = 30       # タイムアウト（秒）
    progress_callback: Optional[callable] = None
```

### Output Interface

```python
class RootAgentOutput:
    success: bool           # 処理成功フラグ
    report_path: str        # 生成レポートパス
    processing_time: float  # 総処理時間
    agent_results: Dict[str, Any]  # 各エージェント結果
    error_message: Optional[str] = None
```

### Methods

```python
class RootAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    async def coordinate_agents(self, markdown_file: MarkdownFile) -> Tuple[EvidenceResult, ProofreadingResult]
    async def generate_final_report(self, evidence: EvidenceResult, proofreading: ProofreadingResult) -> IntegratedReport
```

## 2. Evidence Agent Contract

**Purpose**: エビデンス調査と事実確認

### Input Interface

```python
class EvidenceAgentInput:
    content: str            # Markdownファイル内容
    file_metadata: Dict[str, Any]  # ファイルメタデータ
    verification_depth: str = "standard"  # 検証深度
```

### Output Interface

```python
class EvidenceAgentOutput:
    agent_id: str
    verified_facts: List[Dict[str, Any]]
    questionable_claims: List[Dict[str, Any]]
    missing_evidence: List[Dict[str, Any]]
    recommendations: List[str]
    confidence_score: float
    processing_time: float
    error_message: Optional[str] = None
```

### Methods

```python
class EvidenceAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    async def extract_claims(self, content: str) -> List[str]
    async def verify_facts(self, claims: List[str]) -> List[VerifiedFact]
    async def identify_questionable_claims(self, claims: List[str]) -> List[QuestionableClaim]
```

## 3. Proofreading Agent Contract

**Purpose**: 文章校正と改善提案

### Input Interface

```python
class ProofreadingAgentInput:
    content: str            # Markdownファイル内容
    file_metadata: Dict[str, Any]  # ファイルメタデータ
    correction_level: str = "comprehensive"  # 校正レベル
    language: str = "ja"    # 言語設定
```

### Output Interface

```python
class ProofreadingAgentOutput:
    agent_id: str
    grammar_fixes: List[Dict[str, Any]]
    style_improvements: List[Dict[str, Any]]
    structure_suggestions: List[Dict[str, Any]]
    readability_score: float
    processing_time: float
    error_message: Optional[str] = None
```

### Methods

```python
class ProofreadingAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    async def check_grammar(self, content: str) -> List[GrammarFix]
    async def suggest_style_improvements(self, content: str) -> List[StyleImprovement]
    async def analyze_structure(self, content: str) -> List[StructureSuggestion]
    def calculate_readability_score(self, content: str) -> float
```

## 4. Report Agent Contract

**Purpose**: 統合レポート生成

### Input Interface

```python
class ReportAgentInput:
    original_file: MarkdownFile
    evidence_result: EvidenceResult
    proofreading_result: ProofreadingResult
    output_path: str
    template_style: str = "comprehensive"
```

### Output Interface

```python
class ReportAgentOutput:
    report_id: str
    file_path: str
    executive_summary: str
    overall_score: float
    generation_time: float
    error_message: Optional[str] = None
```

### Methods

```python
class ReportAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    def generate_executive_summary(self, evidence: EvidenceResult, proofreading: ProofreadingResult) -> str
    def calculate_overall_score(self, evidence: EvidenceResult, proofreading: ProofreadingResult) -> float
    def format_markdown_report(self, report: IntegratedReport) -> str
    def save_report(self, content: str, file_path: str) -> bool
```

## Error Handling Contract

### Exception Hierarchy

```python
class AgentError(Exception):
    """基底エラークラス"""
    pass

class AgentProcessingError(AgentError):
    """処理中エラー"""
    pass

class AgentInputValidationError(AgentError):
    """入力検証エラー"""
    pass

class AgentTimeoutError(AgentError):
    """タイムアウトエラー"""
    pass

class AgentCommunicationError(AgentError):
    """エージェント間通信エラー"""
    pass
```

### Error Response Format

```python
class ErrorResponse:
    error_type: str         # エラータイプ
    error_message: str      # エラーメッセージ
    error_code: str         # エラーコード
    timestamp: datetime     # 発生時刻
    agent_id: str          # エラー発生エージェント
    context: Dict[str, Any] # エラーコンテキスト
```

## Progress Reporting Contract

### Progress Event

```python
class ProgressEvent:
    agent_id: str           # 進捗報告エージェント
    stage: str             # 処理段階
    progress: float        # 0.0-1.0の進捗率
    message: str           # 進捗メッセージ
    timestamp: datetime    # 報告時刻
```

### Progress Callback

```python
ProgressCallback = Callable[[ProgressEvent], None]
```

## Configuration Contract

### Agent Configuration

```python
class AgentConfig:
    gemini_api_key: str
    timeout_seconds: int = 30
    max_file_size_mb: int = 10
    output_directory: str = "./reports"
    log_level: str = "INFO"
    retry_attempts: int = 3
```

## Testing Contracts

### Mock Agent Interface

```python
class MockAgent(BaseAgent):
    """テスト用モックエージェント"""

    def __init__(self, agent_type: str, mock_response: Dict[str, Any]):
        self._agent_type = agent_type
        self._mock_response = mock_response

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._mock_response

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return True

    @property
    def agent_type(self) -> str:
        return self._agent_type
```
