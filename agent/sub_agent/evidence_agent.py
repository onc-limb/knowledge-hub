"""Evidence analysis agent for fact-checking and verification.

This agent analyzes markdown content to identify claims that need verification
and checks them against available sources.
"""

from google.adk.agents import LlmAgent
from agent.config.models import GEMINI_2_0_FLASH

evidence_agent = LlmAgent(
    name="evidence_agent",
    model=GEMINI_2_0_FLASH,
    instruction="""
    You are an evidence analysis agent responsible for fact-checking and verification.
    Your role is to:
    1. Analyze markdown content for factual claims
    2. Verify claims against available sources
    3. Identify questionable or unsupported statements
    4. Provide confidence ratings for factual assertions
    
    Always provide thorough analysis and clearly distinguish between verified facts,
    questionable claims, and missing evidence.""",
    description="Analyzes markdown content to identify and verify factual claims",
)
