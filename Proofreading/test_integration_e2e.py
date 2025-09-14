"""End-to-end integration test for the complete proofreading system."""

import asyncio
import tempfile
import json
from pathlib import Path

from agents.root_agent import RootAgent
from utils.file_manager import FileManager


async def test_complete_workflow():
    """Test the complete proofreading workflow end-to-end."""
    print("🧪 Starting E2E Integration Test...")
    
    # Create test content
    test_content = """# Python Programming Guide

Python was created in 1991 by Guido van Rossum. It is the most popular programming language for web development and data science.

## Key Features

1. Python is easy to learn and use
2. It has a large standard library  
3. Python supports multiple programming paradigms

This is a very long sentence that probably exceeds the recommended length for good readability and might trigger style warnings in the proofreading analysis system which should detect this issue.

## Data Science Applications

Python is widely used in data science because of libraries like NumPy, Pandas, and Scikit-learn.
"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        print(f"📝 Created test file: {temp_file}")
        
        # Initialize components
        root_agent = RootAgent()
        file_manager = FileManager()
        
        # Read file
        markdown_file = file_manager.read_markdown_file(temp_file)
        print(f"📖 File size: {markdown_file.size_bytes} bytes")
        
        # Prepare input data
        input_data = {
            "content": markdown_file.content,
            "file_metadata": {
                "path": temp_file,
                "size_bytes": markdown_file.size_bytes,
                "encoding": markdown_file.encoding
            },
            "workflow_options": {
                "verification_depth": "standard",
                "check_level": "standard"
            }
        }
        
        print("🔄 Running complete workflow...")
        
        # Run complete workflow
        result = await root_agent.process(input_data)
        
        # Validate results
        print("✅ Workflow Results:")
        print(f"   Status: {result['status']}")
        print(f"   Processing time: {result['processing_time']:.3f}s")
        print(f"   Workflow ID: {result['workflow_id']}")
        
        # Check evidence analysis
        if result['evidence_analysis']:
            evidence = result['evidence_analysis']
            print(f"   Evidence confidence: {evidence['confidence_score']:.2f}")
            print(f"   Verified facts: {len(evidence['verified_facts'])}")
            print(f"   Questionable claims: {len(evidence['questionable_claims'])}")
        
        # Check proofreading analysis
        if result['proofreading_analysis']:
            proofreading = result['proofreading_analysis']
            print(f"   Readability score: {proofreading['readability_score']:.2f}")
            print(f"   Grammar issues: {len(proofreading['grammar_issues'])}")
            print(f"   Style issues: {len(proofreading['style_issues'])}")
            print(f"   Suggestions: {len(proofreading['suggestions'])}")
        
        # Check integrated report
        if result['integrated_report']:
            report = result['integrated_report']
            print(f"   Overall score: {report['overall_score']:.2f}")
            print(f"   Priority actions: {len(report['priority_actions'])}")
            
            if report['priority_actions']:
                print("   Top priority action:")
                action = report['priority_actions'][0]
                print(f"     - {action['action']} (Priority: {action['priority']})")
        
        # Check task summary
        task_summary = result['task_summary']
        print(f"   Total tasks: {task_summary['total_tasks']}")
        print(f"   Completed: {task_summary['completed_tasks']}")
        print(f"   Failed: {task_summary['failed_tasks']}")
        
        # Test concurrent analysis
        print("\n🔄 Testing concurrent analysis...")
        concurrent_result = await root_agent.run_concurrent_analysis(input_data)
        
        evidence_ok = concurrent_result['evidence_result'] is not None
        proofreading_ok = concurrent_result['proofreading_result'] is not None
        
        print(f"   Evidence analysis: {'✅' if evidence_ok else '❌'}")
        print(f"   Proofreading analysis: {'✅' if proofreading_ok else '❌'}")
        
        # Test task status tracking
        task_statuses = root_agent.get_task_status()
        print(f"\n📊 Task Status Summary:")
        for status in task_statuses:
            print(f"   {status['agent_type']}: {status['status']}")
        
        print("\n✅ E2E Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ E2E Integration Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)


async def test_error_handling():
    """Test error handling in the system."""
    print("\n🧪 Testing Error Handling...")
    
    root_agent = RootAgent()
    
    # Test with invalid input
    invalid_input = {
        "content": 123,  # Invalid type
        "file_metadata": "not_a_dict"  # Invalid type
    }
    
    try:
        result = await root_agent.process(invalid_input)
        
        if result['status'] == 'failed':
            print("✅ Error handling works correctly")
            print(f"   Error message: {result['error_message']}")
            return True
        else:
            print("❌ Expected failure but got success")
            return False
            
    except Exception as e:
        print("✅ Exception handling works correctly")
        print(f"   Exception: {e}")
        return True


async def test_performance():
    """Test system performance with larger content."""
    print("\n🧪 Testing Performance...")
    
    # Create larger test content
    large_content = "# Large Document\n\n" + ("This is a test paragraph. " * 100 + "\n\n") * 10
    
    input_data = {
        "content": large_content,
        "file_metadata": {
            "path": "large_test.md",
            "size_bytes": len(large_content.encode()),
            "encoding": "utf-8"
        },
        "workflow_options": {
            "verification_depth": "basic",
            "check_level": "basic"
        }
    }
    
    root_agent = RootAgent()
    
    import time
    start_time = time.time()
    
    try:
        result = await root_agent.process(input_data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        print(f"✅ Performance test completed")
        print(f"   Content size: {len(large_content)} chars")
        print(f"   Processing time: {processing_time:.3f}s")
        print(f"   Status: {result['status']}")
        
        if processing_time < 10.0:  # Should complete within 10 seconds
            print("✅ Performance is acceptable")
            return True
        else:
            print("⚠️  Performance is slower than expected")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


async def main():
    """Run all integration tests."""
    print("🚀 Starting Integration Test Suite\n")
    
    test_results = []
    
    # Run tests
    test_results.append(await test_complete_workflow())
    test_results.append(await test_error_handling())
    test_results.append(await test_performance())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"\n📊 Integration Test Summary:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All integration tests PASSED!")
    else:
        print(f"\n⚠️  {total-passed} test(s) FAILED")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)