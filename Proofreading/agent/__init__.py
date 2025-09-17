"""ADK Agent Module

This module contains the root agent and sub-agents for the proofreading workflow.
"""

from .root_agent import root_agent

# Export the main agent for ADK discovery
__all__ = ["root_agent"]
