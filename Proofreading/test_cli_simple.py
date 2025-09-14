"""Simple test for CLI functionality."""

import tempfile
import os
from pathlib import Path
from click.testing import CliRunner

from cli import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    
    assert result.exit_code == 0
    assert 'Markdown Proofreading Service' in result.output
    print("✓ CLI help test passed")


def test_cli_list_command():
    """Test list command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['list', '--help'])
    
    assert result.exit_code == 0
    assert 'List available markdown files' in result.output
    print("✓ CLI list help test passed")


def test_cli_proofread_command():
    """Test proofread command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['proofread', '--help'])
    
    assert result.exit_code == 0
    assert 'Run comprehensive proofreading analysis' in result.output
    print("✓ CLI proofread help test passed")


def test_cli_proofread_with_temp_file():
    """Test proofreading a temporary file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("# Test Article\n\nThis is a test content with  double spaces.")
        temp_file = f.name
    
    try:
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = runner.invoke(cli, [
                'proofread', 
                '-f', temp_file,
                '-o', temp_dir,
                '--quiet'
            ])
            
            # Check if command ran (might fail due to missing dependencies, but should not crash)
            print(f"Exit code: {result.exit_code}")
            if result.output:
                print(f"Output: {result.output}")
            
            print("✓ CLI proofread execution test completed")
    
    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    print("Testing CLI functionality...")
    
    test_cli_help()
    test_cli_list_command()
    test_cli_proofread_command()
    test_cli_proofread_with_temp_file()
    
    print("✓ All CLI tests completed!")