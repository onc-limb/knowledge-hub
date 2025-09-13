"""
Evidence Research Agent for fact-checking article content
"""
import asyncio
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from agents.claim_extractor import ClaimExtractor
from agents.evidence_researcher import EvidenceResearcher
from utils.mcp_client import MCPClient

class EvidenceAgent(BaseAgent):
    """Agent responsible for researching evidence and fact-checking"""
    
    def __init__(self):
        super().__init__("EvidenceAgent")
        self.mcp_clients = {
            'firecrawl': MCPClient('firecrawl'),
            'deepwiki': MCPClient('deepwiki'),
            'aws_docs': MCPClient('aws-docs')
        }
        self.claim_extractor = ClaimExtractor(self)
        self.researcher = EvidenceResearcher(self.mcp_clients)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process article content for evidence verification"""
        content = input_data.get('content', '')
        path = input_data.get('path', '')
        
        self.log(f"Starting evidence research for: {path}")
        
        # Extract claims and technical statements
        claims = await self.claim_extractor.extract_claims(content)
        
        # Research each claim
        research_results = []
        for claim in claims:
            result = await self.researcher.research_claim(claim)
            research_results.append(result)
        
        # Generate summary and recommendations
        summary = await self.researcher.generate_summary(research_results, self)
        recommendations = await self.researcher.generate_recommendations(research_results)
        
        return {
            'claims_researched': len(claims),
            'research_results': research_results,
            'summary': summary,
            'recommendations': recommendations
        }