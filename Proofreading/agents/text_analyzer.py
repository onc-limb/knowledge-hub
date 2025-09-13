"""
Text analysis functionality for proofreading using ADK
"""
from typing import Dict, Any
from utils.mcp_client import MCPClient

class TextAnalyzer:
    """Handles different types of text analysis"""
    
    def __init__(self, textlint_client: MCPClient):
        self.textlint_client = textlint_client
    
    async def check_grammar(self, content: str) -> Dict[str, Any]:
        """Check grammar and linguistic issues"""
        
        # Use textlint MCP for Japanese text checking
        try:
            lint_result = await self.textlint_client.call_tool(
                'lint', {'text': content, 'language': 'ja'}
            )
            
            return {
                'tool_result': lint_result,
                'issues_found': True if 'error' not in lint_result else False
            }
        except Exception as e:
            print(f"Textlint check failed: {str(e)}")
            
            # Fallback to LLM-based grammar check
            # ADK will handle the LLM call automatically
            return {
                'llm_fallback': True,
                'issues_found': True  # Assume issues found when tool fails
            }
    
    async def check_style(self, content: str) -> Dict[str, Any]:
        """Check writing style and consistency"""
        
        # ADK will handle the LLM call automatically based on agent instruction
        return {
            'style_check_performed': True,
            'needs_improvement': True  # Placeholder - ADK will determine this
        }