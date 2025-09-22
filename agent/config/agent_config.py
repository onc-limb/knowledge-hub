"""Agent configuration management.

This module manages configuration settings for all agents in the system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import os
from pathlib import Path
import yaml


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    
    agent_type: str
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    model: str = "gemini-2.0-flash-exp"
    temperature: float = 0.1
    max_tokens: int = 4096
    custom_settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceAgentConfig(AgentConfig):
    """Configuration specific to evidence agents."""
    
    verification_depth: str = "standard"  # basic, standard, deep
    fact_check_sources: int = 3
    confidence_threshold: float = 0.7
    
    def __post_init__(self):
        """Set agent type and validate settings."""
        self.agent_type = "evidence"
        valid_depths = ["basic", "standard", "deep"]
        if self.verification_depth not in valid_depths:
            raise ValueError(f"verification_depth must be one of: {valid_depths}")


@dataclass
class ProofreadingAgentConfig(AgentConfig):
    """Configuration specific to proofreading agents."""
    
    correction_level: str = "comprehensive"  # basic, comprehensive, strict
    check_grammar: bool = True
    check_style: bool = True
    check_structure: bool = True
    language: str = "ja"
    
    def __post_init__(self):
        """Set agent type and validate settings."""
        self.agent_type = "proofreading"
        valid_levels = ["basic", "comprehensive", "strict"]
        if self.correction_level not in valid_levels:
            raise ValueError(f"correction_level must be one of: {valid_levels}")


@dataclass
class ReportAgentConfig(AgentConfig):
    """Configuration specific to report agents."""
    
    output_format: str = "markdown"  # markdown, json, html
    include_scores: bool = True
    include_recommendations: bool = True
    max_priority_actions: int = 10
    
    def __post_init__(self):
        """Set agent type and validate settings."""
        self.agent_type = "report"
        valid_formats = ["markdown", "json", "html"]
        if self.output_format not in valid_formats:
            raise ValueError(f"output_format must be one of: {valid_formats}")


@dataclass
class RootAgentConfig(AgentConfig):
    """Configuration specific to root agent coordination."""
    
    parallel_execution: bool = True
    progress_update_interval: float = 0.5  # seconds
    coordinator_timeout: float = 60.0
    failure_tolerance: bool = True  # Continue if one agent fails
    
    def __post_init__(self):
        """Set agent type."""
        self.agent_type = "root"


class ConfigManager:
    """Manages configuration for all agents."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize config manager.
        
        Args:
            config_file: Path to YAML configuration file.
        """
        self.config_file = config_file
        self._default_configs = self._create_default_configs()
        self._custom_configs = {}
        
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
    
    def _create_default_configs(self) -> Dict[str, AgentConfig]:
        """Create default configurations for all agent types."""
        return {
            "evidence": EvidenceAgentConfig(agent_type="evidence"),
            "proofreading": ProofreadingAgentConfig(agent_type="proofreading"),
            "report": ReportAgentConfig(agent_type="report"),
            "root": RootAgentConfig(agent_type="root")
        }
    
    def get_config(self, agent_type: str) -> AgentConfig:
        """Get configuration for a specific agent type.
        
        Args:
            agent_type: Type of agent (evidence, proofreading, report, root).
            
        Returns:
            Configuration object for the agent type.
            
        Raises:
            ValueError: If agent type is not supported.
        """
        if agent_type in self._custom_configs:
            return self._custom_configs[agent_type]
        
        if agent_type in self._default_configs:
            return self._default_configs[agent_type]
        
        raise ValueError(f"Unsupported agent type: {agent_type}")
    
    def set_config(self, agent_type: str, config: AgentConfig):
        """Set custom configuration for an agent type.
        
        Args:
            agent_type: Type of agent.
            config: Configuration object.
        """
        self._custom_configs[agent_type] = config
    
    def load_from_file(self, config_file: str):
        """Load configuration from YAML file.
        
        Args:
            config_file: Path to YAML configuration file.
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            for agent_type, settings in config_data.items():
                if agent_type == "evidence":
                    config = EvidenceAgentConfig(**settings)
                elif agent_type == "proofreading":
                    config = ProofreadingAgentConfig(**settings)
                elif agent_type == "report":
                    config = ReportAgentConfig(**settings)
                elif agent_type == "root":
                    config = RootAgentConfig(**settings)
                else:
                    continue  # Skip unknown agent types
                
                self._custom_configs[agent_type] = config
                
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_file}: {e}")
    
    def save_to_file(self, config_file: str):
        """Save current configuration to YAML file.
        
        Args:
            config_file: Path to save configuration.
        """
        config_data = {}
        
        for agent_type in ["evidence", "proofreading", "report", "root"]:
            config = self.get_config(agent_type)
            config_data[agent_type] = {
                "timeout": config.timeout,
                "max_retries": config.max_retries,
                "retry_delay": config.retry_delay,
                "model": config.model,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }
            
            # Add agent-specific settings
            if isinstance(config, EvidenceAgentConfig):
                config_data[agent_type].update({
                    "verification_depth": config.verification_depth,
                    "fact_check_sources": config.fact_check_sources,
                    "confidence_threshold": config.confidence_threshold
                })
            elif isinstance(config, ProofreadingAgentConfig):
                config_data[agent_type].update({
                    "correction_level": config.correction_level,
                    "check_grammar": config.check_grammar,
                    "check_style": config.check_style,
                    "check_structure": config.check_structure,
                    "language": config.language
                })
            elif isinstance(config, ReportAgentConfig):
                config_data[agent_type].update({
                    "output_format": config.output_format,
                    "include_scores": config.include_scores,
                    "include_recommendations": config.include_recommendations,
                    "max_priority_actions": config.max_priority_actions
                })
            elif isinstance(config, RootAgentConfig):
                config_data[agent_type].update({
                    "parallel_execution": config.parallel_execution,
                    "progress_update_interval": config.progress_update_interval,
                    "coordinator_timeout": config.coordinator_timeout,
                    "failure_tolerance": config.failure_tolerance
                })
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    
    def get_example_config(self) -> str:
        """Get example configuration as YAML string.
        
        Returns:
            Example configuration in YAML format.
        """
        example_config = {
            "evidence": {
                "timeout": 30.0,
                "verification_depth": "standard",
                "fact_check_sources": 3,
                "confidence_threshold": 0.7,
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.1
            },
            "proofreading": {
                "timeout": 30.0,
                "correction_level": "comprehensive",
                "check_grammar": True,
                "check_style": True,
                "check_structure": True,
                "language": "ja",
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.1
            },
            "report": {
                "timeout": 15.0,
                "output_format": "markdown",
                "include_scores": True,
                "include_recommendations": True,
                "max_priority_actions": 10
            },
            "root": {
                "coordinator_timeout": 60.0,
                "parallel_execution": True,
                "progress_update_interval": 0.5,
                "failure_tolerance": True
            }
        }
        
        return yaml.dump(example_config, default_flow_style=False, allow_unicode=True)