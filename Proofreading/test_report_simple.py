"""Simple test for ReportAgent to verify basic functionality."""

import asyncio
import sys
import os

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(__file__))

from agents.report_agent import ReportAgent


async def test_report_agent():
    """Test ReportAgent basic functionality."""
    print("Testing ReportAgent...")
    
    # Initialize agent
    agent = ReportAgent()
    print(f"✓ Agent initialized: {agent.name}")
    print(f"✓ Agent type: {agent.agent_type}")
    
    # Test input validation
    valid_input = {
        "file_metadata": {"path": "test.md", "size": 100},
        "evidence_result": {
            "agent_id": "evidence-test",
            "confidence_score": 0.85,
            "processing_time": 0.1,
            "verified_facts": [],
            "questionable_claims": [],
            "missing_evidence": [],
            "recommendations": []
        },
        "proofreading_result": {
            "agent_id": "proofreading-test",
            "readability_score": 0.75,
            "processing_time": 0.05,
            "summary": "Found 2 grammar issues",
            "grammar_issues": [],
            "style_issues": [],
            "suggestions": []
        },
        "original_content": "This is a test markdown content."
    }
    
    is_valid = agent.validate_input(valid_input)
    print(f"✓ Input validation: {is_valid}")
    
    # Test processing
    try:
        result = await agent.process(valid_input)
        print(f"✓ Processing completed")
        print(f"  - Report ID: {result['report_id']}")
        print(f"  - Executive summary: {result['executive_summary'][:50]}...")
        print(f"  - Priority actions: {len(result['priority_actions'])}")
        print(f"  - Overall score: {result['overall_score']:.2f}")
        print(f"  - File path: {result['file_path']}")
        print(f"  - Processing time: {result['processing_time']:.3f}s")
        
        if result['priority_actions']:
            print(f"  - First action: {result['priority_actions'][0]['action']}")
        
        if result['evidence_summary']:
            print(f"  - Evidence summary: {result['evidence_summary']}")
        
        if result['proofreading_summary']:
            print(f"  - Proofreading summary: {result['proofreading_summary']}")
        
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_report_agent_minimal():
    """Test ReportAgent with minimal input."""
    print("\nTesting ReportAgent with minimal input...")
    
    agent = ReportAgent()
    
    # Test with only file metadata and one result
    minimal_input = {
        "file_metadata": {"path": "minimal.md", "size": 50},
        "evidence_result": {
            "agent_id": "evidence-minimal",
            "confidence_score": 0.6,
            "processing_time": 0.05
        }
    }
    
    try:
        result = await agent.process(minimal_input)
        print(f"✓ Minimal processing completed")
        print(f"  - Overall score: {result['overall_score']:.2f}")
        print(f"  - Priority actions: {len(result['priority_actions'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during minimal processing: {e}")
        return False


if __name__ == "__main__":
    success1 = asyncio.run(test_report_agent())
    success2 = asyncio.run(test_report_agent_minimal())
    exit(0 if (success1 and success2) else 1)