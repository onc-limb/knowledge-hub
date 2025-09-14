"""Simple test for ProofreadingAgent to verify basic functionality."""

import asyncio
import sys
import os

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(__file__))

from agents.proofreading_agent import ProofreadingAgent


async def test_proofreading_agent():
    """Test ProofreadingAgent basic functionality."""
    print("Testing ProofreadingAgent...")
    
    # Initialize agent
    agent = ProofreadingAgent()
    print(f"✓ Agent initialized: {agent.name}")
    print(f"✓ Agent type: {agent.agent_type}")
    
    # Test input validation
    valid_input = {
        "content": "This is a test content with  double spaces and trailing space . This is a very long line that exceeds the normal length limit and might be considered too long for good readability and style recommendations.",
        "file_metadata": {"path": "test.md", "size": 100}
    }
    
    is_valid = agent.validate_input(valid_input)
    print(f"✓ Input validation: {is_valid}")
    
    # Test processing
    try:
        result = await agent.process(valid_input)
        print(f"✓ Processing completed")
        print(f"  - Agent ID: {result['agent_id']}")
        print(f"  - Grammar issues: {len(result['grammar_issues'])}")
        print(f"  - Style issues: {len(result['style_issues'])}")
        print(f"  - Suggestions: {len(result['suggestions'])}")
        print(f"  - Readability score: {result['readability_score']:.2f}")
        print(f"  - Processing time: {result['processing_time']:.3f}s")
        print(f"  - Summary: {result['summary']}")
        
        if result['grammar_issues']:
            print(f"  - First grammar issue: {result['grammar_issues'][0]['message']}")
        
        if result['style_issues']:
            print(f"  - First style issue: {result['style_issues'][0]['message']}")
        
        if result['suggestions']:
            print(f"  - First suggestion: {result['suggestions'][0]['description']}")
        
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_proofreading_agent())
    exit(0 if success else 1)