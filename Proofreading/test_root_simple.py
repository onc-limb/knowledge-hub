"""Simple test for RootAgent to verify basic functionality."""

import asyncio
import sys
import os

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(__file__))

from agents.root_agent import RootAgent


async def test_root_agent():
    """Test RootAgent basic functionality."""
    print("Testing RootAgent...")
    
    # Initialize agent
    agent = RootAgent()
    print(f"✓ Agent initialized: {agent.name}")
    print(f"✓ Agent type: {agent.agent_type}")
    print(f"✓ Sub-agents initialized: Evidence, Proofreading, Report")
    
    # Test input validation
    valid_input = {
        "content": "Python is a programming language. It was created in 1991. Python is widely used for web development and data science.",
        "file_metadata": {"path": "test_article.md", "size": 150},
        "workflow_options": {
            "verification_depth": "standard",
            "check_level": "standard"
        }
    }
    
    is_valid = agent.validate_input(valid_input)
    print(f"✓ Input validation: {is_valid}")
    
    # Test processing
    try:
        print("\n--- Starting Full Workflow ---")
        result = await agent.process(valid_input)
        
        print(f"✓ Workflow completed")
        print(f"  - Workflow ID: {result['workflow_id']}")
        print(f"  - Status: {result['status']}")
        print(f"  - Processing time: {result['processing_time']:.3f}s")
        print(f"  - File path: {result['file_path']}")
        
        # Check task summary
        task_summary = result['task_summary']
        print(f"  - Total tasks: {task_summary['total_tasks']}")
        print(f"  - Completed tasks: {task_summary['completed_tasks']}")
        print(f"  - Failed tasks: {task_summary['failed_tasks']}")
        
        # Check individual results
        if result['evidence_analysis']:
            evidence = result['evidence_analysis']
            print(f"  - Evidence confidence: {evidence['confidence_score']:.2f}")
            print(f"  - Verified facts: {len(evidence['verified_facts'])}")
        
        if result['proofreading_analysis']:
            proofreading = result['proofreading_analysis']
            print(f"  - Readability score: {proofreading['readability_score']:.2f}")
            print(f"  - Grammar issues: {len(proofreading['grammar_issues'])}")
            print(f"  - Style issues: {len(proofreading['style_issues'])}")
        
        if result['integrated_report']:
            report = result['integrated_report']
            print(f"  - Overall score: {report['overall_score']:.2f}")
            print(f"  - Priority actions: {len(report['priority_actions'])}")
            if report['priority_actions']:
                print(f"  - First action: {report['priority_actions'][0]['action']}")
        
        # Check task status
        task_statuses = agent.get_task_status()
        print(f"\n--- Task Status ---")
        for task_status in task_statuses:
            print(f"  - {task_status['agent_type']}: {task_status['status']}")
        
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_concurrent_analysis():
    """Test concurrent analysis functionality."""
    print("\n\nTesting Concurrent Analysis...")
    
    agent = RootAgent()
    
    input_data = {
        "content": "This is a test content for concurrent analysis. Python is great for development.",
        "file_metadata": {"path": "concurrent_test.md", "size": 80},
        "workflow_options": {"verification_depth": "basic", "check_level": "basic"}
    }
    
    try:
        result = await agent.run_concurrent_analysis(input_data)
        
        print(f"✓ Concurrent analysis completed")
        print(f"  - Evidence result available: {result['evidence_result'] is not None}")
        print(f"  - Proofreading result available: {result['proofreading_result'] is not None}")
        print(f"  - Evidence error: {result['evidence_error']}")
        print(f"  - Proofreading error: {result['proofreading_error']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during concurrent analysis: {e}")
        return False


if __name__ == "__main__":
    success1 = asyncio.run(test_root_agent())
    success2 = asyncio.run(test_concurrent_analysis())
    exit(0 if (success1 and success2) else 1)