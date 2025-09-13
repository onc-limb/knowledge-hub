"""
Evidence Research Agent for fact-checking article content using ADK
"""
from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from agents.evidence_researcher import EvidenceResearcher
from utils.mcp_client import MCPClient

class EvidenceAgent(LlmAgent):
    """Agent responsible for researching evidence and fact-checking using ADK"""
    
    def __init__(self):
        # Define tools for the agent - temporarily empty to resolve errors
        tools = []  # Will add proper tools later
        
        super().__init__(
            name="EvidenceAgent",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are an Evidence Research Agent responsible for fact-checking technical articles.
            Your tasks include:
            1. Extract factual claims from article content
            2. Research each claim using available tools
            3. Generate summaries and recommendations
            4. Verify technical accuracy
            
            Use the available tools to gather evidence and provide thorough analysis.
            """,
            description="Specialized agent for evidence research and fact-checking",
            tools=tools
        )
        
        # Initialize MCP clients and researcher after super().__init__
        self._init_resources()
    
    def _init_resources(self):
        """Initialize MCP clients and researcher resources"""
        self._mcp_clients = {
            'firecrawl': MCPClient('firecrawl'),
            'deepwiki': MCPClient('deepwiki'),
            'aws_docs': MCPClient('aws-docs')
        }
        self._researcher = EvidenceResearcher(self._mcp_clients)
    
    def _extract_claims_simple(self, content: str) -> List[str]:
        """Simple claim extraction as fallback"""
        # Basic implementation - extract sentences that contain factual statements
        import re
        sentences = re.split(r'[.!?]+', content)
        claims = []
        
        # Look for sentences that might contain claims
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in 
                ['は', 'です', 'である', 'できる', 'する', '機能', '方法', '技術']):
                claims.append(sentence)
        
        return claims[:5]  # Limit to first 5 claims
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process article content for evidence verification"""
        content = input_data.get('content', '')
        path = input_data.get('path', '')
        
        print(f"[EvidenceAgent] Starting evidence research for: {path}")
        
        # Extract claims using the tool - for now use a simple method
        claims = self._extract_claims_simple(content)
        
        # Research each claim
        research_results = []
        for claim in claims:
            result = await self._researcher.research_claim(claim)
            research_results.append(result)
        
        # Generate summary and recommendations
        summary = await self._researcher.generate_summary(research_results)
        recommendations = await self._researcher.generate_recommendations(research_results)
        
        return {
            'claims_researched': len(claims),
            'research_results': research_results,
            'summary': summary,
            'recommendations': recommendations
        }