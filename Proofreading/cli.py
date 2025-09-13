"""
Command-line interface for the proofreading agent system
"""
import asyncio
import click
import os
from pathlib import Path
from cli_service import ProofreadingService

@click.command()
@click.option('--file-path', '-f', required=True, 
              help='Path to the article file to proofread (relative to repository root)')
@click.option('--output', '-o', default=None,
              help='Output file for the proofreading report')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def proofread(file_path: str, output: str, verbose: bool):
    """
    記事の校閲を実行するコマンドラインツール
    
    使用例:
    python cli.py -f articles/my-article.md
    python cli.py -f knowledges/python/Logging.md -o report.txt
    """
    
    # Check if .env file exists
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        click.echo("❌ .envファイルが見つかりません。")
        click.echo("📝 .env.templateを参考に.envファイルを作成してください。")
        return
    
    # Run the proofreading process
    service = ProofreadingService()
    asyncio.run(service.run_proofreading(file_path, output, verbose))

@click.command()
@click.option('--pattern', '-p', default='',
              help='Search pattern for finding markdown files')
def list_files(pattern: str):
    """
    校閲可能なマークダウンファイルを一覧表示
    
    使用例:
    python cli.py list-files
    python cli.py list-files -p "articles"
    """
    
    service = ProofreadingService()
    service.list_files(pattern)

@click.group()
def cli():
    """記事校閲エージェントシステム"""
    pass

# Add commands to the group
cli.add_command(proofread)
cli.add_command(list_files)

if __name__ == '__main__':
    cli()