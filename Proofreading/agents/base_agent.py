"""
Base Agent class for all proofreading agents
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from config.llm_config import LLMConfig

class BaseAgent(ABC):
    """Base class for all agents in the proofreading system"""
    
    def __init__(self, name: str):
        self.name = name
        self.llm_config = LLMConfig()
        self.model = self.llm_config.get_model()
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    def generate_prompt(self, template: str, **kwargs) -> str:
        """Generate prompt from template with given parameters"""
        return template.format(**kwargs)
    
    async def call_llm(self, prompt: str) -> str:
        """Call the LLM with the given prompt"""
        try:
            return self.llm_config.generate_response(prompt)
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def log(self, message: str):
        """Log a message"""
        print(f"[{self.name}] {message}")

class AgentTask:
    """Represents a task that can be processed by an agent"""
    
    def __init__(self, task_type: str, data: Dict[str, Any]):
        self.task_type = task_type
        self.data = data
        self.results = {}
        self.status = "pending"
    
    def mark_completed(self, results: Dict[str, Any]):
        """Mark the task as completed with results"""
        self.results = results
        self.status = "completed"
    
    def mark_failed(self, error: str):
        """Mark the task as failed with error message"""
        self.results = {"error": error}
        self.status = "failed"