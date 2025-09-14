"""Multi-agent coordination integration test.

This test validates the coordination between RootAgent, EvidenceAgent, 
ProofreadingAgent, and ReportAgent.
"""

import pytest
import asyncio
import tempfile
import json
from unittest.mock import Mock, patch
from pathlib import Path


class TestMultiAgentCoordination:
    """Test multi-agent coordination functionality."""

    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self):
        """Test that Evidence and Proofreading agents run in parallel."""
        # MUST FAIL initially - agents not implemented yet
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import MarkdownFile
        
        root_agent = RootAgent()
        
        # Create test markdown file
        test_content = """# Test Document

This is a test document with some claims:
1. The Earth is round.
2. Python was created by Guido van Rossum.

There are also some grammar error here. The sentence structure needs improvement.
"""
        
        markdown_file = MarkdownFile(
            file_path="/tmp/test.md",
            content=test_content,
            size_bytes=len(test_content.encode()),
            encoding="utf-8"
        )
        
        # Mock to track execution timing
        evidence_start_time = None
        proofreading_start_time = None
        evidence_end_time = None
        proofreading_end_time = None
        
        async def mock_evidence_process(input_data):
            nonlocal evidence_start_time, evidence_end_time
            import time
            evidence_start_time = time.time()
            await asyncio.sleep(0.1)  # Simulate processing time
            evidence_end_time = time.time()
            return {
                "agent_id": "evidence-001",
                "verified_facts": [],
                "confidence_score": 0.85,
                "processing_time": 0.1
            }
        
        async def mock_proofreading_process(input_data):
            nonlocal proofreading_start_time, proofreading_end_time
            import time
            proofreading_start_time = time.time()
            await asyncio.sleep(0.1)  # Simulate processing time
            proofreading_end_time = time.time()
            return {
                "agent_id": "proofreading-001",
                "grammar_fixes": [],
                "readability_score": 0.78,
                "processing_time": 0.1
            }
        
        with patch('Proofreading.agents.evidence_agent.EvidenceAgent.process', 
                   side_effect=mock_evidence_process), \
             patch('Proofreading.agents.proofreading_agent.ProofreadingAgent.process', 
                   side_effect=mock_proofreading_process):
            
            evidence_result, proofreading_result = await root_agent.coordinate_agents(markdown_file)
            
            # Verify parallel execution (overlapping time windows)
            assert evidence_start_time is not None
            assert proofreading_start_time is not None
            
            # Check that they started roughly at the same time (within 50ms)
            time_diff = abs(evidence_start_time - proofreading_start_time)
            assert time_diff < 0.05  # Should start within 50ms of each other

    @pytest.mark.asyncio
    async def test_agent_result_aggregation(self):
        """Test that RootAgent properly aggregates results from all agents."""
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import EvidenceResult, ProofreadingResult
        
        root_agent = RootAgent()
        
        # Create mock results
        evidence_result = EvidenceResult(
            agent_id="evidence-001",
            verified_facts=[{"claim": "Test claim", "confidence": 0.9}],
            questionable_claims=[],
            missing_evidence=[],
            recommendations=["Add more sources"],
            confidence_score=0.85,
            processing_time=5.2
        )
        
        proofreading_result = ProofreadingResult(
            agent_id="proofreading-001",
            grammar_fixes=[{"line": 1, "original": "error", "corrected": "errors"}],
            style_improvements=[],
            structure_suggestions=[],
            readability_score=0.78,
            processing_time=4.8
        )
        
        # Test report generation
        integrated_report = await root_agent.generate_final_report(
            evidence_result, proofreading_result
        )
        
        assert integrated_report.evidence_result == evidence_result
        assert integrated_report.proofreading_result == proofreading_result
        assert integrated_report.overall_score > 0
        assert len(integrated_report.executive_summary) > 0
        assert len(integrated_report.priority_actions) > 0

    @pytest.mark.asyncio
    async def test_agent_error_handling_isolation(self):
        """Test that if one agent fails, the other can still complete."""
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import MarkdownFile
        
        root_agent = RootAgent()
        
        markdown_file = MarkdownFile(
            file_path="/tmp/test.md",
            content="# Test",
            size_bytes=6,
            encoding="utf-8"
        )
        
        async def mock_evidence_failure(input_data):
            raise Exception("Evidence service unavailable")
        
        async def mock_proofreading_success(input_data):
            return {
                "agent_id": "proofreading-001",
                "grammar_fixes": [],
                "readability_score": 0.78,
                "processing_time": 2.1
            }
        
        with patch('Proofreading.agents.evidence_agent.EvidenceAgent.process', 
                   side_effect=mock_evidence_failure), \
             patch('Proofreading.agents.proofreading_agent.ProofreadingAgent.process', 
                   side_effect=mock_proofreading_success):
            
            # Should not raise exception, but handle partial failure
            evidence_result, proofreading_result = await root_agent.coordinate_agents(markdown_file)
            
            # Evidence should indicate failure
            assert evidence_result.error_message is not None
            # Proofreading should succeed
            assert proofreading_result.error_message is None
            assert proofreading_result.readability_score == 0.78

    @pytest.mark.asyncio
    async def test_task_assignment_tracking(self):
        """Test task assignment and status tracking."""
        from Proofreading.utils.models import TaskAssignment
        from datetime import datetime
        
        # Test task creation
        task = TaskAssignment(
            task_id="task-001",
            agent_type="evidence",
            status="PENDING",
            input_data={"content": "test"},
            result=None,
            started_at=None,
            completed_at=None,
            error_details=None
        )
        
        assert task.status == "PENDING"
        assert task.result is None
        
        # Test task status progression
        task.status = "RUNNING"
        task.started_at = datetime.now()
        
        assert task.status == "RUNNING"
        assert task.started_at is not None
        
        # Test task completion
        task.status = "COMPLETED"
        task.completed_at = datetime.now()
        task.result = {"confidence_score": 0.85}
        
        assert task.status == "COMPLETED"
        assert task.result["confidence_score"] == 0.85

    @pytest.mark.asyncio
    async def test_progress_callback_updates(self):
        """Test that progress callbacks are properly triggered."""
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import MarkdownFile
        
        root_agent = RootAgent()
        progress_updates = []
        
        def progress_callback(stage, percentage, message):
            progress_updates.append({
                "stage": stage,
                "percentage": percentage,
                "message": message
            })
        
        markdown_file = MarkdownFile(
            file_path="/tmp/test.md",
            content="# Test document",
            size_bytes=15,
            encoding="utf-8"
        )
        
        # Mock agent processes to simulate progress
        async def mock_evidence_process(input_data):
            progress_callback("evidence", 50, "Analyzing claims")
            await asyncio.sleep(0.05)
            progress_callback("evidence", 100, "Evidence analysis complete")
            return {"agent_id": "evidence-001", "confidence_score": 0.85}
        
        async def mock_proofreading_process(input_data):
            progress_callback("proofreading", 50, "Checking grammar")
            await asyncio.sleep(0.05)
            progress_callback("proofreading", 100, "Proofreading complete")
            return {"agent_id": "proofreading-001", "readability_score": 0.78}
        
        with patch('Proofreading.agents.evidence_agent.EvidenceAgent.process', 
                   side_effect=mock_evidence_process), \
             patch('Proofreading.agents.proofreading_agent.ProofreadingAgent.process', 
                   side_effect=mock_proofreading_process):
            
            # Set progress callback
            root_agent.progress_callback = progress_callback
            
            await root_agent.coordinate_agents(markdown_file)
            
            # Verify progress updates were called
            assert len(progress_updates) >= 4  # At least 2 updates per agent
            
            # Check that we got updates for both agents
            evidence_updates = [u for u in progress_updates if u["stage"] == "evidence"]
            proofreading_updates = [u for u in progress_updates if u["stage"] == "proofreading"]
            
            assert len(evidence_updates) >= 2
            assert len(proofreading_updates) >= 2

    @pytest.mark.asyncio
    async def test_timeout_handling_in_coordination(self):
        """Test timeout handling in agent coordination."""
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import MarkdownFile
        
        root_agent = RootAgent()
        
        markdown_file = MarkdownFile(
            file_path="/tmp/test.md",
            content="# Test",
            size_bytes=6,
            encoding="utf-8"
        )
        
        async def slow_evidence_process(input_data):
            await asyncio.sleep(2)  # Takes too long
            return {"agent_id": "evidence-001", "confidence_score": 0.85}
        
        async def fast_proofreading_process(input_data):
            await asyncio.sleep(0.1)  # Completes quickly
            return {"agent_id": "proofreading-001", "readability_score": 0.78}
        
        with patch('Proofreading.agents.evidence_agent.EvidenceAgent.process', 
                   side_effect=slow_evidence_process), \
             patch('Proofreading.agents.proofreading_agent.ProofreadingAgent.process', 
                   side_effect=fast_proofreading_process):
            
            # Set short timeout
            root_agent.timeout = 1.0  # 1 second timeout
            
            evidence_result, proofreading_result = await root_agent.coordinate_agents(markdown_file)
            
            # Evidence should timeout and have error
            assert evidence_result.error_message is not None
            # Proofreading should complete successfully
            assert proofreading_result.error_message is None

    @pytest.mark.asyncio
    async def test_concurrent_agent_resource_management(self):
        """Test that concurrent agents don't interfere with each other's resources."""
        from Proofreading.agents.root_agent import RootAgent
        from Proofreading.utils.models import MarkdownFile
        
        root_agent = RootAgent()
        
        markdown_file = MarkdownFile(
            file_path="/tmp/test.md",
            content="# Test document with multiple claims and grammar issues.",
            size_bytes=56,
            encoding="utf-8"
        )
        
        # Track resource usage
        evidence_resource_calls = []
        proofreading_resource_calls = []
        
        async def mock_evidence_process(input_data):
            # Simulate API calls
            evidence_resource_calls.append("api_call_1")
            await asyncio.sleep(0.1)
            evidence_resource_calls.append("api_call_2")
            return {"agent_id": "evidence-001", "confidence_score": 0.85}
        
        async def mock_proofreading_process(input_data):
            # Simulate different API calls
            proofreading_resource_calls.append("grammar_api_1")
            await asyncio.sleep(0.1)
            proofreading_resource_calls.append("grammar_api_2")
            return {"agent_id": "proofreading-001", "readability_score": 0.78}
        
        with patch('Proofreading.agents.evidence_agent.EvidenceAgent.process', 
                   side_effect=mock_evidence_process), \
             patch('Proofreading.agents.proofreading_agent.ProofreadingAgent.process', 
                   side_effect=mock_proofreading_process):
            
            await root_agent.coordinate_agents(markdown_file)
            
            # Verify both agents used their resources without interference
            assert len(evidence_resource_calls) == 2
            assert len(proofreading_resource_calls) == 2
            assert "api_call_1" in evidence_resource_calls
            assert "grammar_api_1" in proofreading_resource_calls