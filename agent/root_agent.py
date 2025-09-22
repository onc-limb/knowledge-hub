"""Root agent for coordinating the proofreading workflow.

This agent orchestrates the evidence analysis, proofreading, and report generation
workflow by coordinating with specialized sub-agents using ADK AgentTool pattern.
"""

import sys
import os
from pathlib import Path
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import AgentTool
from datetime import datetime

# Import sub-agents as tools
try:
    from .sub_agent.evidence_agent import evidence_agent
    from .sub_agent.proofreading_agent import proofreading_agent
    from .sub_agent.report_agent import report_agent
except ImportError:
    # Fallback for direct execution - add current directory to path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    from sub_agent.evidence_agent import evidence_agent
    from sub_agent.proofreading_agent import proofreading_agent
    from sub_agent.report_agent import report_agent


# Create AgentTool instances for sub-agents
evidence_tool = AgentTool(agent=evidence_agent)
proofreading_tool = AgentTool(agent=proofreading_agent)
report_tool = AgentTool(agent=report_agent)


# ADK Root Agent definition with sub-agents as tools
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
