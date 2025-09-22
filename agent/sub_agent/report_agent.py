"""
report agent for refining and clarifying extracted evidence.
This agent proofreads and enhances the clarity of the evidence identified by the Evidence Agent.
"""

from google.adk.agents import LlmAgent
from agent.config.models import GEMINI_2_0_FLASH

report_agent = LlmAgent(
    name="report_agent",
    model=GEMINI_2_0_FLASH,
    instruction="""
    You are a report agent responsible for generating a final report based on proofread content.
    Your role is to:
    1. Compile the proofread evidence into a coherent report
    2. Ensure the report is clear, concise, and professionally formatted
    3. Highlight key findings and conclusions effectively
    Always aim to produce a high-quality report that effectively communicates the information to the intended audience.
    """,
    description="Generates a final report based on proofread content",
)
