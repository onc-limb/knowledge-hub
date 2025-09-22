"""
proofreading agent for refining and clarifying extracted evidence.
This agent proofreads and enhances the clarity of the evidence identified by the Evidence Agent.
"""

from google.adk.agents import LlmAgent
from agent.config.models import GEMINI_2_0_FLASH

proofreading_agent = LlmAgent(
    name="proofreading_agent",
    model=GEMINI_2_0_FLASH,
    instruction="""
    You are a proofreading agent responsible for refining and clarifying extracted evidence.
    Your role is to:
    1. Proofread the extracted evidence for clarity and correctness
    2. Enhance the readability and coherence of the content
    3. Ensure the information is presented in a clear and professional manner
    Always aim to improve the quality of the text while preserving the original meaning and intent.
    """,
    description="Proofreads and refines extracted evidence for clarity and correctness",
)
