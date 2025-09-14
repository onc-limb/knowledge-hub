"""Report generation integration test.

This test validates the final report generation functionality.
"""

import pytest
import tempfile
import os
import json
from pathlib import Path
from datetime import datetime


class TestReportGeneration:
    """Test report generation functionality."""

    def test_markdown_report_generation(self):
        """Test markdown format report generation."""
        # MUST FAIL initially - report generation not implemented yet
        import subprocess
        
        test_content = """# Test Document

This document contains claims that need verification:
- Python was created in 1991
- The Internet started in 1969

Grammar issues: This sentence have errors. Its important to fix them.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--format", "markdown", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check report file exists
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) > 0
            
            # Validate markdown report structure
            report_file = report_files[-1]
            content = report_file.read_text()
            
            # Check required sections
            assert "# 統合校正レポート" in content or "# Integrated Proofreading Report" in content
            assert "## エビデンス調査結果" in content or "## Evidence Analysis" in content
            assert "## 文章校正結果" in content or "## Proofreading Results" in content
            assert "## 要約" in content or "## Executive Summary" in content
            assert "## 優先対応事項" in content or "## Priority Actions" in content
            assert "## 総合評価" in content or "## Overall Score" in content
            
        finally:
            os.unlink(test_file)

    def test_json_report_generation(self):
        """Test JSON format report generation."""
        import subprocess
        
        test_content = "# Simple Test\nTest document for JSON output."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--format", "json", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check JSON report file exists
            reports_dir = Path("reports")
            json_files = list(reports_dir.glob("*.json"))
            assert len(json_files) > 0
            
            # Validate JSON structure
            json_file = json_files[-1]
            with open(json_file) as f:
                data = json.load(f)
            
            # Required top-level fields
            required_fields = [
                "report_id", "original_file", "evidence_result", 
                "proofreading_result", "executive_summary", 
                "priority_actions", "overall_score", "generated_at"
            ]
            
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
            
            # Validate data types
            assert isinstance(data["report_id"], str)
            assert isinstance(data["overall_score"], (int, float))
            assert 0 <= data["overall_score"] <= 1
            assert isinstance(data["priority_actions"], list)
            assert isinstance(data["executive_summary"], str)
            
            # Validate nested structures
            assert "file_path" in data["original_file"]
            assert "content" in data["original_file"]
            
            assert "agent_id" in data["evidence_result"]
            assert "confidence_score" in data["evidence_result"]
            
            assert "agent_id" in data["proofreading_result"]
            assert "readability_score" in data["proofreading_result"]
            
        finally:
            os.unlink(test_file)

    def test_html_report_generation(self):
        """Test HTML format report generation."""
        import subprocess
        
        test_content = "# HTML Test\nTest document for HTML output."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--format", "html", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check HTML report file exists
            reports_dir = Path("reports")
            html_files = list(reports_dir.glob("*.html"))
            assert len(html_files) > 0
            
            # Validate HTML structure
            html_file = html_files[-1]
            content = html_file.read_text()
            
            # Basic HTML validation
            assert content.startswith("<!DOCTYPE html>") or content.startswith("<html")
            assert "<head>" in content
            assert "<body>" in content
            assert "</html>" in content
            
            # Check for required content sections
            assert "統合校正レポート" in content or "Integrated Report" in content
            assert "エビデンス" in content or "Evidence" in content
            assert "校正" in content or "Proofreading" in content
            
        finally:
            os.unlink(test_file)

    def test_report_filename_format(self):
        """Test report filename follows correct format."""
        import subprocess
        import re
        
        test_content = "# Filename Test\nTest document."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
            base_name = Path(test_file).stem
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check filename format: basename_YYYYMMDD_HHMMSS_proofreading_report.md
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) > 0
            
            latest_report = report_files[-1]
            filename = latest_report.name
            
            # Validate filename pattern
            pattern = r".+_\d{8}_\d{6}_proofreading_report\.md$"
            assert re.match(pattern, filename), f"Invalid filename format: {filename}"
            
        finally:
            os.unlink(test_file)

    def test_report_content_accuracy(self):
        """Test that report content accurately reflects input analysis."""
        import subprocess
        
        test_content = """# Test Document with Known Issues

## Claims Section
1. The moon is made of cheese (needs verification)
2. Python 3.9 was released in 2020 (verifiable fact)

## Grammar Section
This sentence have multiple grammar error. Their going to the store.
You're welcome for the feedback. Its very important.

## Style Section
Very very very repetitive words. The document could be more concise and clear.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--format", "json", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Read generated JSON report
            reports_dir = Path("reports")
            json_files = list(reports_dir.glob("*.json"))
            json_file = json_files[-1]
            
            with open(json_file) as f:
                data = json.load(f)
            
            # Check evidence analysis
            evidence = data["evidence_result"]
            assert len(evidence.get("questionable_claims", [])) > 0  # Should find cheese claim
            
            # Check proofreading results
            proofreading = data["proofreading_result"]
            assert len(proofreading.get("grammar_fixes", [])) > 0  # Should find grammar errors
            
            # Check overall score reflects issues found
            assert data["overall_score"] < 0.9  # Should be lower due to issues
            
            # Check priority actions exist
            assert len(data["priority_actions"]) > 0
            
        finally:
            os.unlink(test_file)

    def test_report_timestamp_accuracy(self):
        """Test that report timestamps are accurate."""
        import subprocess
        from datetime import datetime, timedelta
        
        test_content = "# Timestamp Test\nTest document."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            start_time = datetime.now()
            
            result = subprocess.run(
                ["markdown-proofreading", "--format", "json", test_file],
                capture_output=True,
                text=True
            )
            
            end_time = datetime.now()
            assert result.returncode == 0
            
            # Check timestamp in JSON report
            reports_dir = Path("reports")
            json_files = list(reports_dir.glob("*.json"))
            json_file = json_files[-1]
            
            with open(json_file) as f:
                data = json.load(f)
            
            # Parse generated timestamp
            generated_at = datetime.fromisoformat(data["generated_at"].replace('Z', '+00:00'))
            
            # Timestamp should be within processing window (allowing for timezone differences)
            time_diff = abs((generated_at.replace(tzinfo=None) - start_time).total_seconds())
            assert time_diff < 60  # Within 1 minute
            
        finally:
            os.unlink(test_file)

    def test_report_file_permissions(self):
        """Test that generated reports have correct file permissions."""
        import subprocess
        import stat
        
        test_content = "# Permissions Test\nTest document."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check file permissions
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            report_file = report_files[-1]
            
            file_stat = os.stat(report_file)
            file_mode = stat.filemode(file_stat.st_mode)
            
            # Should be readable and writable by owner
            assert file_stat.st_mode & stat.S_IRUSR  # Owner read
            assert file_stat.st_mode & stat.S_IWUSR  # Owner write
            
        finally:
            os.unlink(test_file)

    def test_concurrent_report_generation(self):
        """Test that multiple concurrent reports don't interfere."""
        import subprocess
        import concurrent.futures
        import threading
        
        def generate_report(content, identifier):
            test_content = f"# Test {identifier}\n{content}"
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(test_content)
                test_file = f.name
            
            try:
                result = subprocess.run(
                    ["markdown-proofreading", test_file],
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0, test_file
            except:
                return False, test_file
        
        # Generate multiple reports concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(generate_report, "Content A", "A"),
                executor.submit(generate_report, "Content B", "B"),
                executor.submit(generate_report, "Content C", "C")
            ]
            
            results = []
            test_files = []
            for future in concurrent.futures.as_completed(futures):
                success, test_file = future.result()
                results.append(success)
                test_files.append(test_file)
        
        try:
            # All should succeed
            assert all(results)
            
            # Check that we have multiple report files
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) >= 3
            
        finally:
            # Cleanup
            for test_file in test_files:
                try:
                    os.unlink(test_file)
                except:
                    pass