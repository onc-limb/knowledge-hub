"""
Proofreading Agent for text improvement and style checking using ADK
"""
from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from agents.text_analyzer import TextAnalyzer
from agents.suggestion_generator import SuggestionGenerator
from utils.mcp_client import MCPClient

class ProofreadingAgent(LlmAgent):
    """Agent responsible for proofreading and style improvement using ADK"""
    
    def __init__(self):
        super().__init__(
            name="ProofreadingAgent",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are a Proofreading Agent responsible for improving technical articles.
            Your tasks include:
            1. Check grammar and linguistic issues
            2. Analyze writing style and consistency
            3. Assess readability and comprehensibility
            4. Generate improvement suggestions
            5. Provide detailed proofreading summary
            
            Focus on technical accuracy, clarity, and professional presentation.
            """,
            description="Specialized agent for proofreading and style improvement",
            tools=[]
        )
        
        self.textlint_client = MCPClient('textlint')
        self.analyzer = TextAnalyzer(self.textlint_client)
        self.suggestion_generator = SuggestionGenerator()
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process article content for proofreading"""
        content = input_data.get('content', '')
        path = input_data.get('path', '')
        
        print(f"[ProofreadingAgent] Starting proofreading for: {path}")
        
        # Perform different types of proofreading
        grammar_check = await self.analyzer.check_grammar(content, self)
        style_check = await self.analyzer.check_style(content, self)
        readability_check = await self.suggestion_generator.check_readability(content, self)
        
        # Generate improvement suggestions
        suggestions = await self.suggestion_generator.generate_suggestions(
            content, grammar_check, style_check, readability_check, self
        )
        
        # Generate summary
        summary = await self.suggestion_generator.generate_summary(suggestions, self)
        
        return {
            'grammar_issues': grammar_check,
            'style_issues': style_check,
            'readability_score': readability_check,
            'suggestions': suggestions,
            'summary': summary
        }