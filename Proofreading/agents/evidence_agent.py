"""Evidence analysis agent for fact-checking and verification.

This agent analyzes markdown content to identify claims that need verification
and checks them against available sources.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from google.adk.agents import Agent
from utils.models import EvidenceResult, VerifiedFact, QuestionableClaim, MissingEvidence


async def analyze_evidence(content: str, sources: Optional[List[str]] = None) -> Dict[str, Any]:
    """Tool function for evidence analysis and fact-checking.
    
    Args:
        content: Markdown content to analyze for factual claims
        sources: Optional list of source URLs/references to verify against
        
    Returns:
        Dictionary containing evidence analysis results
    """
    # Simulate evidence analysis processing
    await asyncio.sleep(0.1)
    
    # Mock analysis results - create objects with correct parameters
    verified_facts = [
        {
            "claim": "Python is a programming language",
            "evidence": "Python official website and documentation",
            "source": sources[0] if sources else "https://python.org",
            "confidence": 0.95
        }
    ]
    
    questionable_claims = [
        {
            "claim": "This framework is the fastest",
            "reason": "No comparative benchmarks provided",
            "severity": "medium"
        }
    ]
    
    missing_evidence = [
        {
            "claim": "Usage statistics mentioned",
            "required_evidence": "Specific metrics and data sources",
            "suggestion": "Provide benchmarks and usage data"
        }
    ]
    
    result = {
        "agent_id": "evidence_agent",
        "verified_facts": verified_facts,
        "questionable_claims": questionable_claims,
        "missing_evidence": missing_evidence,
        "confidence_score": 0.75
    }
    
    return result


# ADK Agent definition
root_agent = Agent(
    name="EvidenceAgent",
    model="gemini-2.0-flash",
    instruction="""You are an evidence analysis agent responsible for fact-checking and verification.
    Your role is to:
    1. Analyze markdown content for factual claims
    2. Verify claims against available sources
    3. Identify questionable or unsupported statements
    4. Provide confidence ratings for factual assertions
    
    Always provide thorough analysis and clearly distinguish between verified facts,
    questionable claims, and missing evidence.""",
    description="Analyzes markdown content to identify and verify factual claims",
    tools=[analyze_evidence]
)
