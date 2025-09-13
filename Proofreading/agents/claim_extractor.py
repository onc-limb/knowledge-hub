"""
Evidence claim extraction functionality
"""
from typing import List
from agents.base_agent import BaseAgent

class ClaimExtractor:
    """Extracts factual claims from article content"""
    
    def __init__(self, agent: BaseAgent):
        self.agent = agent
    
    async def extract_claims(self, content: str) -> List[str]:
        """Extract factual claims from the article content"""
        prompt = f"""
        以下の技術記事から、事実確認が必要な技術的な主張や情報を抽出してください。
        特に以下の観点で抽出してください:
        - API仕様や使用方法
        - ライブラリやフレームワークの機能
        - AWSなどのクラウドサービスの仕様
        - 技術的な手順や設定方法
        
        記事内容:
        {content[:1000]}...
        
        抽出した主張を箇条書きで返してください:
        """
        
        response = await self.agent.call_llm(prompt)
        
        # Parse the response into individual claims
        claims = [line.strip().lstrip('- ').lstrip('・') 
                 for line in response.split('\n') 
                 if line.strip() and (line.strip().startswith('-') or line.strip().startswith('・'))]
        
        return claims[:5]  # Limit to top 5 claims to avoid excessive API calls