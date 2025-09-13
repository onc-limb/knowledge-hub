"""
Evidence research functionality
"""
from typing import Dict, Any, List
from utils.mcp_client import MCPClient

class EvidenceResearcher:
    """Handles research of individual claims"""
    
    def __init__(self, mcp_clients: Dict[str, MCPClient]):
        self.mcp_clients = mcp_clients
    
    async def research_claim(self, claim: str) -> Dict[str, Any]:
        """Research a specific claim using MCP clients"""
        print(f"Researching claim: {claim[:50]}...")
        
        # Try different research approaches
        research_attempts = []
        
        # Web search with Firecrawl (mock for now)
        try:
            web_result = await self.mcp_clients['firecrawl'].call_tool(
                'scrape', {'query': claim}
            )
            research_attempts.append({
                'source': 'web',
                'result': web_result,
                'confidence': 'medium'
            })
        except Exception as e:
            print(f"Web research failed: {str(e)}")
        
        return {
            'claim': claim,
            'research_attempts': research_attempts,
            'verified': len(research_attempts) > 0
        }
    
    async def generate_summary(self, research_results: List[Dict], agent) -> str:
        """Generate summary of evidence research"""
        verified_count = sum(1 for r in research_results if r['verified'])
        total_count = len(research_results)
        
        prompt = f"""
        エビデンス調査の結果をまとめてください。
        
        調査した主張の数: {total_count}
        検証できた主張の数: {verified_count}
        
        調査結果の概要を日本語で生成してください。
        """
        
        return await agent.call_llm(prompt)
    
    async def generate_recommendations(self, research_results: List[Dict]) -> List[str]:
        """Generate recommendations based on research results"""
        unverified_claims = [r['claim'] for r in research_results if not r['verified']]
        
        recommendations = []
        if unverified_claims:
            recommendations.append("以下の主張について追加のエビデンスが必要です:")
            recommendations.extend(f"- {claim}" for claim in unverified_claims[:3])
        
        return recommendations