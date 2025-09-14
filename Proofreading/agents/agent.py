"""Root agent for coordinating the proofreading workflow.

This agent orchestrates the evidence analysis, proofreading, and report generation
workflow by coordinating with specialized sub-agents.
"""

from google.adk.agents import LlmAgent
from agents.evidence_agent import root_agent as evidence_agent
from agents.proofreading_agent import root_agent as proofreading_agent  
from agents.report_agent import root_agent as report_agent


# ADK Root Agent definition with sub-agents
root_agent = LlmAgent(
    name="ProofreadingRootAgent",
    model="gemini-2.0-flash",
    instruction="""You are the root coordinator for a comprehensive proofreading and analysis service.
    
    Your role is to:
    1. Coordinate with specialized sub-agents for evidence analysis, proofreading, and report generation
    2. Orchestrate the complete workflow from content input to final report
    3. Ensure all aspects of content analysis are covered
    4. Provide a unified interface for users
    
    Available sub-agents:
    - EvidenceAgent: Analyzes content for factual accuracy and evidence verification
    - ProofreadingAgent: Performs grammar, style, and content improvement analysis
    - ReportAgent: Generates comprehensive reports consolidating all analysis results
    
    Always coordinate the workflow systematically and provide clear, actionable results.""",
    description="Coordinates evidence analysis, proofreading, and report generation workflow",
    sub_agents=[
        evidence_agent,
        proofreading_agent,
        report_agent
    ]
)
