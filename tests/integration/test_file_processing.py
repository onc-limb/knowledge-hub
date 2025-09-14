"""File processing integration test.

This test validates end-to-end file processing functionality.
"""

import pytest
import tempfile
import os
import subprocess
import json
from pathlib import Path


class TestFileProcessing:
    """Test file processing integration."""

    def test_process_simple_markdown_file(self):
        """Test processing a simple valid markdown file."""
        # MUST FAIL initially - processing not implemented yet
        test_content = """# Sample Document

This is a sample markdown document for testing.

## Introduction

The purpose of this document is to test the markdown proofreading service.
It contains some claims that may need evidence verification.

## Claims to Verify

1. Python is the most popular programming language in 2024.
2. Markdown was created by John Gruber in 2004.
3. The speed of light is approximately 300,000 km/s.

## Grammar Test

This sentence have a grammar error. The weather is nice today, it's sunny.
Their going to the store. Your welcome for the help.

## Conclusion

This document should generate a comprehensive report with evidence 
verification and grammar corrections.
"""
        
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
            
            # Check that report was generated
            reports_dir = Path("reports")
            assert reports_dir.exists()
            
            # Find the generated report file
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) > 0
            
            # Verify report content
            report_file = report_files[-1]  # Get the latest report
            report_content = report_file.read_text()
            
            assert "# 統合校正レポート" in report_content or "Integrated Report" in report_content
            assert "エビデンス調査結果" in report_content or "Evidence" in report_content
            assert "文章校正結果" in report_content or "Proofreading" in report_content
            
        finally:
            os.unlink(test_file)

    def test_process_file_with_custom_output_dir(self):
        """Test processing with custom output directory."""
        test_content = "# Test\nSimple test document."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                result = subprocess.run(
                    ["markdown-proofreading", "--output-dir", temp_dir, test_file],
                    capture_output=True,
                    text=True
                )
                
                assert result.returncode == 0
                
                # Check that report was generated in custom directory
                output_dir = Path(temp_dir)
                report_files = list(output_dir.glob("*_proofreading_report.md"))
                assert len(report_files) > 0
                
            finally:
                os.unlink(test_file)

    def test_process_file_json_output_format(self):
        """Test processing with JSON output format."""
        test_content = "# Test\nSimple test document."
        
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
            
            # Check that JSON report was generated
            reports_dir = Path("reports")
            json_files = list(reports_dir.glob("*.json"))
            assert len(json_files) > 0
            
            # Verify JSON structure
            json_file = json_files[-1]
            with open(json_file) as f:
                report_data = json.load(f)
            
            required_keys = ["report_id", "original_file", "evidence_result", 
                           "proofreading_result", "executive_summary", "overall_score"]
            for key in required_keys:
                assert key in report_data
                
        finally:
            os.unlink(test_file)

    def test_process_file_with_timeout(self):
        """Test processing with custom timeout."""
        test_content = "# Test\nSimple test document."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            # Test with reasonable timeout
            result = subprocess.run(
                ["markdown-proofreading", "--timeout", "60", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
        finally:
            os.unlink(test_file)

    def test_process_empty_file(self):
        """Test processing an empty markdown file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("")  # Empty file
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", test_file],
                capture_output=True,
                text=True
            )
            
            # Should handle empty files gracefully
            assert result.returncode == 0
            
            # Should still generate a report
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) > 0
            
        finally:
            os.unlink(test_file)

    def test_process_large_file_within_limit(self):
        """Test processing a file close to but within size limit."""
        # Create ~5MB file (within 10MB limit)
        large_content = "# Large Document\n" + ("Test content. " * 200000)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(large_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--timeout", "90", test_file],
                capture_output=True,
                text=True
            )
            
            # Should process successfully
            assert result.returncode == 0
            
        finally:
            os.unlink(test_file)

    def test_process_file_with_special_characters(self):
        """Test processing file with unicode and special characters."""
        test_content = """# テストドキュメント

これは日本語のテストです。

## 特殊文字テスト

- Émojis: 🚀 📝 ✅
- Unicode: αβγδε
- Mathematical: ∑∫∆√
- Quotes: "smart quotes" 'apostrophes'

## 混合言語

This document contains both English and 日本語 text.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", test_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            
            # Check that report handles unicode correctly
            reports_dir = Path("reports")
            report_files = list(reports_dir.glob("*_proofreading_report.md"))
            assert len(report_files) > 0
            
            # Verify report can be read as UTF-8
            report_file = report_files[-1]
            report_content = report_file.read_text(encoding='utf-8')
            assert len(report_content) > 0
            
        finally:
            os.unlink(test_file)

    def test_progress_bar_display(self):
        """Test that progress bar is displayed during processing."""
        test_content = "# Test\n" + ("Content for progress testing. " * 1000)
        
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
            
            # Check for progress indicators in output
            output = result.stdout + result.stderr
            progress_indicators = ["⚡", "🔍", "📝", "📊", "✅", "%"]
            assert any(indicator in output for indicator in progress_indicators)
            
        finally:
            os.unlink(test_file)

    def test_processing_time_within_limits(self):
        """Test that processing completes within time limits."""
        test_content = "# Test\nSimple test for timing."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            import time
            start_time = time.time()
            
            result = subprocess.run(
                ["markdown-proofreading", test_file],
                capture_output=True,
                text=True
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            assert result.returncode == 0
            # Should complete within 30 seconds for small file
            assert processing_time < 30
            
        finally:
            os.unlink(test_file)