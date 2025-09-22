"""Data models for the markdown proofreading service.

This module contains all core data entities defined in the data model specification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4


@dataclass
class MarkdownFile:
    """Represents a markdown file to be processed."""
    
    file_path: str
    content: str
    size_bytes: int
    encoding: str = "utf-8"
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the markdown file data."""
        if self.size_bytes <= 0:
            raise ValueError("File size must be greater than 0")
        if self.size_bytes > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("File size exceeds 10MB limit")
        if not self.file_path:
            raise ValueError("File path is required")


@dataclass
class VerifiedFact:
    """Represents a verified factual claim."""
    
    claim: str
    evidence: str
    source: str
    confidence: float
    
    def __post_init__(self):
        """Validate confidence score."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")


@dataclass
class QuestionableClaim:
    """Represents a questionable or unverifiable claim."""
    
    claim: str
    reason: str
    severity: str
    
    def __post_init__(self):
        """Validate severity level."""
        valid_severities = ["low", "medium", "high", "critical"]
        if self.severity not in valid_severities:
            raise ValueError(f"Severity must be one of: {valid_severities}")


@dataclass
class MissingEvidence:
    """Represents a claim that lacks sufficient evidence."""
    
    claim: str
    required_evidence: str
    suggestion: str


@dataclass
class EvidenceResult:
    """Result from the evidence analysis agent."""
    
    agent_id: str
    verified_facts: List[VerifiedFact] = field(default_factory=list)
    questionable_claims: List[QuestionableClaim] = field(default_factory=list)
    missing_evidence: List[MissingEvidence] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    processing_time: float = 0.0
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Validate confidence score."""
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")


@dataclass
class GrammarIssue:
    """Represents a grammar issue in the text."""
    
    line: int
    column: int
    message: str
    severity: str
    rule: str
    
    def __post_init__(self):
        """Validate severity level."""
        valid_severities = ["low", "medium", "high"]
        if self.severity not in valid_severities:
            raise ValueError(f"Severity must be one of: {valid_severities}")


@dataclass
class StyleIssue:
    """Represents a style issue in the text."""
    
    line: int
    column: int
    message: str
    severity: str
    category: str
    
    def __post_init__(self):
        """Validate severity level."""
        valid_severities = ["low", "medium", "high"]
        if self.severity not in valid_severities:
            raise ValueError(f"Severity must be one of: {valid_severities}")


@dataclass
class ImprovementSuggestion:
    """Represents an improvement suggestion."""
    
    type: str
    description: str
    original: str
    suggested: str
    confidence: float
    
    def __post_init__(self):
        """Validate confidence."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")


@dataclass
class GrammarFix:
    """Represents a grammar correction."""
    
    line_number: int
    original: str
    corrected: str
    rule: str
    
    def __post_init__(self):
        """Validate line number."""
        if self.line_number < 1:
            raise ValueError("Line number must be positive")


@dataclass
class StyleImprovement:
    """Represents a style improvement suggestion."""
    
    line_number: int
    suggestion: str
    category: str
    priority: str
    
    def __post_init__(self):
        """Validate priority level."""
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")


@dataclass
class StructureSuggestion:
    """Represents a document structure improvement."""
    
    section: str
    improvement: str
    rationale: str


@dataclass
class ProofreadingResult:
    """Result from the proofreading agent."""
    
    agent_id: str
    grammar_issues: List[GrammarIssue] = field(default_factory=list)
    style_issues: List[StyleIssue] = field(default_factory=list)
    style_suggestions: List['StyleSuggestion'] = field(default_factory=list)
    content_improvements: List['ContentImprovement'] = field(default_factory=list)
    suggestions: List[ImprovementSuggestion] = field(default_factory=list)
    readability_score: float = 0.0
    overall_score: float = 0.0
    summary: str = ""
    processing_time: float = 0.0
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Validate readability score."""
        if not 0.0 <= self.readability_score <= 1.0:
            raise ValueError("Readability score must be between 0.0 and 1.0")
        if not 0.0 <= self.overall_score <= 10.0:
            raise ValueError("Overall score must be between 0.0 and 10.0")


@dataclass
class PriorityAction:
    """Represents a priority action item."""
    
    action: str
    category: str
    priority: int
    effort: str
    
    def __post_init__(self):
        """Validate priority and effort."""
        if self.priority < 1:
            raise ValueError("Priority must be positive")
        valid_efforts = ["low", "medium", "high"]
        if self.effort not in valid_efforts:
            raise ValueError(f"Effort must be one of: {valid_efforts}")


@dataclass
class IntegratedReport:
    """Final integrated report combining all analysis results."""
    
    report_id: str = field(default_factory=lambda: str(uuid4()))
    original_file: Optional[MarkdownFile] = None
    evidence_result: Optional[EvidenceResult] = None
    evidence_summary: Dict[str, Any] = field(default_factory=dict)
    proofreading_result: Optional[ProofreadingResult] = None
    proofreading_summary: Dict[str, Any] = field(default_factory=dict)
    sections: List['ReportSection'] = field(default_factory=list)
    executive_summary: str = ""
    priority_actions: List[PriorityAction] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    overall_score: float = 0.0
    overall_quality_score: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)
    file_path: str = ""
    
    def __post_init__(self):
        """Validate overall score."""
        if not 0.0 <= self.overall_score <= 1.0:
            raise ValueError("Overall score must be between 0.0 and 1.0")
        if not 0.0 <= self.overall_quality_score <= 10.0:
            raise ValueError("Overall quality score must be between 0.0 and 10.0")


@dataclass
class TaskAssignment:
    """Represents a task assignment for agent coordination."""
    
    task_id: str = field(default_factory=lambda: str(uuid4()))
    agent_type: str = ""
    status: str = "PENDING"
    input_data: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_details: Optional[str] = None
    
    def __post_init__(self):
        """Validate status."""
        valid_statuses = ["PENDING", "RUNNING", "COMPLETED", "FAILED"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        
        valid_agent_types = ["evidence", "proofreading", "report", "root"]
        if self.agent_type and self.agent_type not in valid_agent_types:
            raise ValueError(f"Agent type must be one of: {valid_agent_types}")


# Export all models for easy importing
__all__ = [
    "MarkdownFile",
    "VerifiedFact", 
    "QuestionableClaim",
    "MissingEvidence",
    "EvidenceResult",
    "GrammarIssue",
    "StyleIssue",
    "ImprovementSuggestion",
    "GrammarFix",
    "StyleImprovement", 
    "StructureSuggestion",
    "ProofreadingResult",
    "PriorityAction",
    "IntegratedReport",
    "TaskAssignment",
    "StyleSuggestion",
    "ContentImprovement",
    "ReportSection"
]


@dataclass
class StyleSuggestion:
    """Represents a style improvement suggestion."""
    
    text: str
    suggestion: str
    reason: str
    category: str
    line_number: int
    column_number: int


@dataclass
class ContentImprovement:
    """Represents a content structure improvement suggestion."""
    
    section: str
    issue: str
    suggestion: str
    impact: str
    priority: str


@dataclass
class ReportSection:
    """Represents a section in the integrated report."""
    
    title: str
    content: str
    order: int

