"""
Evidence Research Agent for fact-checking article content using ADK
"""
from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from agents.claim_extractor import extract_claims
from agents.evidence_researcher import EvidenceResearcher
from utils.mcp_client import MCPClient

class EvidenceAgent(LlmAgent):
    """Agent responsible for researching evidence and fact-checking using ADK"""
    
    def __init__(self):
        # Define tools for the agent
        tools = [extract_claims]  # Add more tools as needed
        
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
        
        self.mcp_clients = {
            'firecrawl': MCPClient('firecrawl'),
            'deepwiki': MCPClient('deepwiki'),
            'aws_docs': MCPClient('aws-docs')
        }
        self.researcher = EvidenceResearcher(self.mcp_clients)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process article content for evidence verification"""
        content = input_data.get('content', '')
        path = input_data.get('path', '')
        
        print(f"[EvidenceAgent] Starting evidence research for: {path}")
        
        # Extract claims using the tool
        claims = extract_claims(content)
        
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