"""
Base Agent class for all proofreading agents using ADK
"""
from google.adk.agents import LlmAgent
from typing import Dict, Any, List

class BaseAgent(LlmAgent):
    """Base class for all agents in the proofreading system using ADK"""
    
    def __init__(self, name: str, model: str = "gemini-2.0-flash-exp", instruction: str = "", description: str = "", tools: List | None = None):
        super().__init__(
            name=name,
            model=model,
            instruction=instruction or f"You are a {name} agent for proofreading technical articles.",
            description=description or f"Specialized agent for {name.lower()} tasks in proofreading",
            tools=tools or []
        )
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement run method")
    
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