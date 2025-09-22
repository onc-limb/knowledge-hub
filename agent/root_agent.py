"""Root agent for coordinating the proofreading workflow.

This agent orchestrates the evidence analysis, proofreading, and report generation
workflow by coordinating with specialized sub-agents using ADK AgentTool pattern.
"""

from google.adk.agents import SequentialAgent

from sub_agent import evidence_agent, proofreading_agent, report_agent

root_agent = SequentialAgent(
    name="proofreading_root_agent",
    sub_agents=[evidence_agent, proofreading_agent, report_agent],
    description=
    """
    This agent coordinates the workflow for analyzing and proofreading documents.
    It uses the following specialized sub-agents:
    1. Evidence Agent: Analyzes the provided document and extracts key evidence.
    2. Proofreading Agent: Proofreads the extracted evidence for clarity and correctness.
    3. Report Agent: Generates a final report based on the proofread content.
    """,
)
