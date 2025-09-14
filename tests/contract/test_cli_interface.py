"""CLI interface contract test for markdown proofreading service.

This test validates the CLI interface specification from 
contracts/cli-interface.md against the actual implementation.
"""

import subprocess
import pytest
import os
import tempfile
from pathlib import Path


class TestCLIInterface:
    """Test CLI interface contract compliance."""

    def test_cli_help_command(self):
        """Test that --help option is available and shows usage."""
        # MUST FAIL initially - CLI not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "markdown-proofreading" in result.stdout
        assert "file_path" in result.stdout

    def test_cli_version_command(self):
        """Test that --version option shows version information."""
        # MUST FAIL initially - CLI not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--version"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "0.1.0" in result.stdout

    def test_cli_basic_options(self):
        """Test that basic CLI options are recognized."""
        # Test that these options don't cause argument errors
        test_cases = [
            ["markdown-proofreading", "--output-dir", "/tmp"],
            ["markdown-proofreading", "--format", "json"],
            ["markdown-proofreading", "--timeout", "60"],
            ["markdown-proofreading", "--verbose"],
            ["markdown-proofreading", "--quiet"],
        ]
        
        for args in test_cases:
            # MUST FAIL initially - options not implemented yet
            result = subprocess.run(
                args + ["--help"],  # Add help to avoid actual execution
                capture_output=True,
                text=True
            )
            # Should not fail due to unrecognized arguments
            assert result.returncode == 0

    def test_cli_missing_file_error(self):
        """Test proper error handling for missing file."""
        result = subprocess.run(
            ["markdown-proofreading", "/nonexistent/file.md"],
            capture_output=True,
            text=True
        )
        
        # Should return exit code 2 for file not found
        assert result.returncode == 2
        assert "ファイルが見つかりません" in result.stderr

    def test_cli_file_size_validation(self):
        """Test file size validation (10MB limit)."""
        # Create a test file larger than 10MB
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            # Write more than 10MB of content
            large_content = "# Large File\n" + "x" * (10 * 1024 * 1024 + 1)
            f.write(large_content)
            large_file_path = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", large_file_path],
                capture_output=True,
                text=True
            )
            
            # Should return exit code 4 for file size exceeded
            assert result.returncode == 4
            assert "ファイルサイズ超過" in result.stderr
        finally:
            os.unlink(large_file_path)

    def test_cli_output_format_options(self):
        """Test output format options (markdown, json, html)."""
        valid_formats = ["markdown", "json", "html"]
        
        for format_type in valid_formats:
            result = subprocess.run(
                ["markdown-proofreading", "--format", format_type, "--help"],
                capture_output=True,
                text=True
            )
            # Should not fail due to invalid format
            assert result.returncode == 0

    def test_cli_timeout_option(self):
        """Test timeout option accepts numeric values."""
        result = subprocess.run(
            ["markdown-proofreading", "--timeout", "30", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_cli_config_file_option(self):
        """Test config file option."""
        result = subprocess.run(
            ["markdown-proofreading", "--config", "config.yaml", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_cli_config_example_command(self):
        """Test config example generation."""
        result = subprocess.run(
            ["markdown-proofreading", "--config-example"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "evidence_depth:" in result.stdout
        assert "correction_level:" in result.stdout

    def test_cli_list_languages_command(self):
        """Test supported languages listing."""
        result = subprocess.run(
            ["markdown-proofreading", "--list-languages"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "ja" in result.stdout
        assert "en" in result.stdout