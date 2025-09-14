"""Basic CLI command integration test.

This test validates basic CLI functionality like help and version commands.
"""

import subprocess
import pytest
import sys
import os
from pathlib import Path


class TestBasicCLI:
    """Test basic CLI command functionality."""

    def test_cli_executable_exists(self):
        """Test that markdown-proofreading command is available."""
        # MUST FAIL initially - CLI executable not installed yet
        result = subprocess.run(
            ["which", "markdown-proofreading"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "markdown-proofreading" in result.stdout

    def test_cli_help_displays_usage(self):
        """Test help command shows proper usage information."""
        # MUST FAIL initially - CLI not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        help_output = result.stdout
        
        # Check for required help content
        assert "usage:" in help_output.lower()
        assert "file_path" in help_output
        assert "options:" in help_output.lower()
        assert "--output-dir" in help_output
        assert "--format" in help_output
        assert "--timeout" in help_output
        assert "--verbose" in help_output

    def test_cli_version_shows_correct_version(self):
        """Test version command shows correct version."""
        # MUST FAIL initially - CLI not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--version"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "0.1.0" in result.stdout

    def test_cli_no_arguments_shows_help(self):
        """Test that running without arguments shows help."""
        result = subprocess.run(
            ["markdown-proofreading"],
            capture_output=True,
            text=True
        )
        
        # Should show help and exit with error
        assert result.returncode != 0
        assert "usage:" in result.stderr.lower() or "usage:" in result.stdout.lower()

    def test_cli_invalid_option_shows_error(self):
        """Test that invalid options show proper error."""
        result = subprocess.run(
            ["markdown-proofreading", "--invalid-option"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "invalid" in result.stderr.lower() or "unrecognized" in result.stderr.lower()

    def test_cli_list_languages_command(self):
        """Test list languages command."""
        # MUST FAIL initially - not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--list-languages"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        output = result.stdout
        assert "ja" in output
        assert "en" in output

    def test_cli_config_example_command(self):
        """Test config example command."""
        # MUST FAIL initially - not implemented yet
        result = subprocess.run(
            ["markdown-proofreading", "--config-example"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        output = result.stdout
        
        # Should output valid YAML config
        assert "evidence_depth:" in output
        assert "correction_level:" in output
        assert "output_dir:" in output
        assert "format:" in output

    def test_cli_python_module_execution(self):
        """Test CLI can be executed as Python module."""
        # Alternative way to run if executable not available
        result = subprocess.run(
            [sys.executable, "-m", "Proofreading.cli", "--help"],
            capture_output=True,
            text=True,
            cwd="/Users/ongasatoshi/Documents/development/onc-limb/knowledge-hub"
        )
        
        # Should work even if global executable not installed
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()

    def test_cli_error_codes(self):
        """Test CLI returns correct error codes."""
        test_cases = [
            # (command_args, expected_exit_code, description)
            (["markdown-proofreading", "/nonexistent/file.md"], 2, "file not found"),
            (["markdown-proofreading", "--timeout", "-1", "file.md"], 7, "invalid config"),
            (["markdown-proofreading", "--format", "invalid", "file.md"], 7, "invalid format"),
        ]
        
        for args, expected_code, description in test_cases:
            result = subprocess.run(args, capture_output=True, text=True)
            assert result.returncode == expected_code, f"Failed for {description}"

    def test_cli_verbose_mode(self):
        """Test verbose mode produces detailed output."""
        # Create a temporary test file
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\nThis is a test.")
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--verbose", test_file],
                capture_output=True,
                text=True
            )
            
            # In verbose mode, should see detailed logging
            output = result.stderr + result.stdout
            assert "[INFO]" in output or "[DEBUG]" in output
        finally:
            os.unlink(test_file)

    def test_cli_quiet_mode(self):
        """Test quiet mode produces minimal output."""
        # Create a temporary test file
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\nThis is a test.")
            test_file = f.name
        
        try:
            result = subprocess.run(
                ["markdown-proofreading", "--quiet", test_file],
                capture_output=True,
                text=True
            )
            
            # In quiet mode, should have minimal output
            output = result.stdout
            # Should only show essential information, no progress bars
            assert "✓" not in output or len(output.split('\n')) <= 3
        finally:
            os.unlink(test_file)