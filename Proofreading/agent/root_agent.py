"""Root agent for coordinating the proofreading workflow.

This agent orchestrates the evidence analysis, proofreading, and report generation
workflow by coordinating with specialized sub-agents using ADK AgentTool pattern.
"""

import sys
import os
from pathlib import Path
from google.adk.agents import Agent
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
root_agent = Agent(
    name="ProofreadingRootAgent",
    model="gemini-2.0-flash",
    instruction="""You are the root coordinator for a comprehensive proofreading and analysis service.
    
    When a user provides a file path or content for analysis, you should:
    1. Use the evidence_tool to analyze the content for fact-checking and source verification
    2. Use the proofreading_tool to check grammar, style, and readability
    3. Use the report_tool to generate a comprehensive consolidated report
    
    Your role is to orchestrate the complete workflow by delegating to specialized tools
    and provide unified, actionable results in Japanese.
    
    Always follow this workflow:
    - First call evidence_tool with the content
    - Then call proofreading_tool with the same content
    - Finally call report_tool with both results to generate the final report
    
    Provide clear, structured output that helps users improve their content.""",
    description="Coordinates evidence analysis, proofreading, and report generation workflow",
    tools=[evidence_tool, proofreading_tool, report_tool]
)


# ADKコマンドライン実行時のメイン処理
if __name__ == "__main__":
    print("使用方法: adk run Proofreading/agent <ファイルパス>")
    print("例: adk run Proofreading/agent sample.md")
