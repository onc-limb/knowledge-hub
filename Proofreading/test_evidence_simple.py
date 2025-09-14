"""Simple test for EvidenceAgent to verify basic functionality."""

import asyncio
import sys
import os

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(__file__))

from agents.evidence_agent import EvidenceAgent


async def test_evidence_agent():
    """Test EvidenceAgent basic functionality."""
    print("Testing EvidenceAgent...")
    
    # Initialize agent
    agent = EvidenceAgent()
    print(f"✓ Agent initialized: {agent.name}")
    print(f"✓ Agent type: {agent.agent_type}")
    
    # Test input validation
    valid_input = {
        "content": "Python was created in 1991. It is a popular programming language.",
        "file_metadata": {"path": "test.md", "size": 100}
    }
    
    is_valid = agent.validate_input(valid_input)
    print(f"✓ Input validation: {is_valid}")
    
    # Test processing
    try:
        result = await agent.process(valid_input)
        print(f"✓ Processing completed")
        print(f"  - Agent ID: {result['agent_id']}")
        print(f"  - Verified facts: {len(result['verified_facts'])}")
        print(f"  - Questionable claims: {len(result['questionable_claims'])}")
        print(f"  - Missing evidence: {len(result['missing_evidence'])}")
        print(f"  - Recommendations: {len(result['recommendations'])}")
        print(f"  - Confidence score: {result['confidence_score']:.2f}")
        print(f"  - Processing time: {result['processing_time']:.3f}s")
        
        if result['verified_facts']:
            print(f"  - First verified fact: {result['verified_facts'][0]['claim']}")
        
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_evidence_agent())
    exit(0 if success else 1)