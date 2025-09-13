"""
Text analysis functionality for proofreading
"""
from typing import Dict, Any
from utils.mcp_client import MCPClient

class TextAnalyzer:
    """Handles different types of text analysis"""
    
    def __init__(self, textlint_client: MCPClient):
        self.textlint_client = textlint_client
    
    async def check_grammar(self, content: str, agent) -> Dict[str, Any]:
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
            prompt = f"""
            以下の日本語技術文書の文法や表現をチェックしてください。
            特に以下の点に注意してください:
            - 誤字脱字
            - 助詞の使い方
            - 文体の統一
            - 技術用語の適切な使用
            
            文書内容:
            {content[:800]}...
            
            問題のある箇所があれば指摘してください:
            """
            
            response = await agent.call_llm(prompt)
            return {
                'llm_result': response,
                'issues_found': '問題' in response or '指摘' in response
            }
    
    async def check_style(self, content: str, agent) -> Dict[str, Any]:
        """Check writing style and consistency"""
        
        prompt = f"""
        以下の技術文書のスタイルと一貫性をチェックしてください:
        
        チェック項目:
        1. 文体の統一（です・ます調 vs である調）
        2. 技術用語の表記統一
        3. 見出しの階層構造
        4. 段落の構成
        5. コードブロックの記述方法
        
        文書内容:
        {content[:800]}...
        
        スタイルの改善点があれば具体的に指摘してください:
        """
        
        response = await agent.call_llm(prompt)
        return {
            'style_feedback': response,
            'needs_improvement': '改善' in response or '統一' in response
        }