"""Tests for Evidence Agent implementation."""

import pytest
import asyncio
from typing import Dict, Any

# Add Proofreading directory to Python path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Proofreading'))

from agents.evidence_agent import EvidenceAgent
from agents.base_agent import AgentProcessingError


class TestEvidenceAgent:
    """Test cases for EvidenceAgent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = EvidenceAgent()
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        assert self.agent.name == "EvidenceAgent"
        assert self.agent.agent_type == "evidence"
    
    def test_validate_input_valid(self):
        """Test input validation with valid data."""
        valid_input = {
            "content": "This is a test markdown content.",
            "file_metadata": {"path": "test.md", "size": 100}
        }
        assert self.agent.validate_input(valid_input) == True
    
    def test_validate_input_missing_content(self):
        """Test input validation with missing content."""
        invalid_input = {
            "file_metadata": {"path": "test.md", "size": 100}
        }
        assert self.agent.validate_input(invalid_input) == False
    
    def test_validate_input_missing_metadata(self):
        """Test input validation with missing metadata."""
        invalid_input = {
            "content": "This is a test markdown content."
        }
        assert self.agent.validate_input(invalid_input) == False
    
    def test_validate_input_invalid_content_type(self):
        """Test input validation with invalid content type."""
        invalid_input = {
            "content": 123,  # Should be string
            "file_metadata": {"path": "test.md", "size": 100}
        }
        assert self.agent.validate_input(invalid_input) == False
    
    def test_validate_input_invalid_metadata_type(self):
        """Test input validation with invalid metadata type."""
        invalid_input = {
            "content": "This is a test markdown content.",
            "file_metadata": "not_a_dict"  # Should be dict
        }
        assert self.agent.validate_input(invalid_input) == False
    
    @pytest.mark.asyncio
    async def test_process_valid_input(self):
        """Test processing with valid input."""
        input_data = {
            "content": "Python was created in 1991. It is the most popular programming language.",
            "file_metadata": {"path": "test.md", "size": 100}
        }
        
        result = await self.agent.process(input_data)
        
        # Check result structure
        assert "agent_id" in result
        assert "verified_facts" in result
        assert "questionable_claims" in result
        assert "missing_evidence" in result
        assert "recommendations" in result
        assert "confidence_score" in result
        assert "processing_time" in result
        
        # Check types
        assert isinstance(result["verified_facts"], list)
        assert isinstance(result["questionable_claims"], list)
        assert isinstance(result["missing_evidence"], list)
        assert isinstance(result["recommendations"], list)
        assert isinstance(result["confidence_score"], float)
        assert isinstance(result["processing_time"], float)
        
        # Check confidence score range
        assert 0.0 <= result["confidence_score"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_process_invalid_input(self):
        """Test processing with invalid input raises exception."""
        invalid_input = {
            "content": 123,  # Invalid type
            "file_metadata": {"path": "test.md", "size": 100}
        }
        
        with pytest.raises(AgentProcessingError):
            await self.agent.process(invalid_input)
    
    @pytest.mark.asyncio
    async def test_extract_claims(self):
        """Test claim extraction functionality."""
        content = """
        1. Python was created in 1991 by Guido van Rossum.
        2. It is the most popular programming language.
        3. Python is used for web development.
        
        Some other text here.
        """
        
        claims = await self.agent._extract_claims(content)
        
        assert isinstance(claims, list)
        assert len(claims) >= 1
        # Check that claims contain expected content
        claim_text = " ".join(claims)
        assert any("Python" in claim for claim in claims)
    
    @pytest.mark.asyncio
    async def test_verify_facts(self):
        """Test fact verification functionality."""
        claims = ["Python was created in 1991", "Python is used for programming"]
        
        verified_facts = await self.agent._verify_facts(claims, "standard")
        
        assert isinstance(verified_facts, list)
        assert len(verified_facts) == len(claims)
        
        # Check VerifiedFact structure
        for fact in verified_facts:
            assert hasattr(fact, 'claim')
            assert hasattr(fact, 'evidence')
            assert hasattr(fact, 'source')
            assert hasattr(fact, 'confidence')
            assert 0.0 <= fact.confidence <= 1.0
    
    @pytest.mark.asyncio
    async def test_identify_questionable_claims(self):
        """Test questionable claim identification."""
        claims = ["Python is great", "Aliens built the pyramids", "This is normal text"]
        
        questionable = await self.agent._identify_questionable_claims(claims)
        
        assert isinstance(questionable, list)
        # Check QuestionableClaim structure
        for claim in questionable:
            assert hasattr(claim, 'claim')
            assert hasattr(claim, 'reason')
            assert hasattr(claim, 'severity')
    
    @pytest.mark.asyncio
    async def test_find_missing_evidence(self):
        """Test missing evidence identification."""
        claims = ["Python is the best language", "This is a normal statement"]
        
        missing = await self.agent._find_missing_evidence(claims)
        
        assert isinstance(missing, list)
        # Check MissingEvidence structure
        for evidence in missing:
            assert hasattr(evidence, 'claim')
            assert hasattr(evidence, 'required_evidence')
            assert hasattr(evidence, 'suggestion')
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self):
        """Test recommendation generation."""
        from utils.models import VerifiedFact, QuestionableClaim, MissingEvidence
        
        verified_facts = [VerifiedFact("fact1", "evidence1", "source1", 0.9)]
        questionable_claims = [QuestionableClaim("claim1", "reason1", "medium")]
        missing_evidence = [MissingEvidence("claim2", "evidence2", "suggestion2")]
        
        recommendations = await self.agent._generate_recommendations(
            verified_facts, questionable_claims, missing_evidence
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation."""
        from utils.models import VerifiedFact, QuestionableClaim, MissingEvidence
        
        verified_facts = [
            VerifiedFact("fact1", "evidence1", "source1", 0.9),
            VerifiedFact("fact2", "evidence2", "source2", 0.8)
        ]
        questionable_claims = [QuestionableClaim("claim1", "reason1", "medium")]
        missing_evidence = [MissingEvidence("claim2", "evidence2", "suggestion2")]
        
        score = self.agent._calculate_confidence_score(
            verified_facts, questionable_claims, missing_evidence
        )
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    def test_calculate_confidence_score_no_claims(self):
        """Test confidence score calculation with no claims."""
        score = self.agent._calculate_confidence_score([], [], [])
        assert score == 0.8  # Default score for no claims


if __name__ == "__main__":
    pytest.main([__file__])