"""
CLI command handlers
"""
import asyncio
import click
from pathlib import Path

from agents.root_agent import RootAgent
from agents.evidence_agent import EvidenceAgent
from agents.proofreading_agent import ProofreadingAgent
from utils.file_manager import FileManager

class ProofreadingService:
    """Main service for handling proofreading operations"""
    
    async def run_proofreading(self, file_path: str, output_file: str, verbose: bool):
        """Main proofreading process"""
        
        try:
            # Initialize file manager and read article
            file_manager = FileManager()
            
            click.echo(f"📖 記事を読み込み中: {file_path}")
            content = file_manager.read_file(file_path)
            article_info = file_manager.parse_markdown(content)
            
            if verbose:
                click.echo(f"📊 記事情報:")
                click.echo(f"   タイトル: {article_info['title']}")
                click.echo(f"   行数: {article_info['line_count']}")
                click.echo(f"   単語数: {article_info['word_count']}")
            
            # Initialize and run agents
            click.echo("🤖 エージェントを初期化中...")
            root_agent = RootAgent()
            evidence_agent = EvidenceAgent()
            proofreading_agent = ProofreadingAgent()
            
            root_agent.set_agents(evidence_agent, proofreading_agent)
            
            click.echo("⚡ 校閲プロセスを開始...")
            
            input_data = {
                'content': content,
                'path': file_path,
                'metadata': article_info
            }
            
            result = await root_agent.process(input_data)
            
            # Display and save results
            await self._display_results(result)
            
            if output_file:
                await self._save_report(result, output_file, file_path)
                click.echo(f"\n💾 レポートを保存しました: {output_file}")
            
            click.echo("\n✅ 校閲プロセスが完了しました！")
            
        except FileNotFoundError as e:
            click.echo(f"❌ ファイルエラー: {str(e)}")
        except Exception as e:
            click.echo(f"❌ エラーが発生しました: {str(e)}")
            if verbose:
                import traceback
                click.echo(traceback.format_exc())
    
    async def _display_results(self, result: dict):
        """Display proofreading results"""
        click.echo("\n" + "="*50)
        click.echo("📋 校閲結果レポート")
        click.echo("="*50)
        
        # Overall summary
        click.echo("\n🔍 総合評価:")
        click.echo(result.get('overall_summary', '評価を生成できませんでした'))
        
        # Evidence findings
        evidence = result.get('evidence_findings', {})
        click.echo(f"\n🔬 エビデンス調査結果:")
        click.echo(f"   調査完了: {evidence.get('claims_researched', 0)}件")
        click.echo(f"   概要: {evidence.get('summary', 'なし')}")
        
        # Proofreading suggestions
        proofreading = result.get('proofreading_suggestions', {})
        click.echo(f"\n✏️  文章校閲結果:")
        click.echo(f"   概要: {proofreading.get('summary', 'なし')}")
        
        if proofreading.get('suggestions'):
            click.echo("   改善提案:")
            for suggestion in proofreading['suggestions'][:5]:
                click.echo(f"   • {suggestion}")
    
    async def _save_report(self, result: dict, output_file: str, file_path: str):
        """Save the proofreading report to a file"""
        
        report_content = f"""校閲レポート
===================
対象ファイル: {file_path}
生成日時: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

総合評価:
{result.get('overall_summary', '評価なし')}

エビデンス調査結果:
{result.get('evidence_findings', {}).get('summary', 'なし')}

文章校閲結果:
{result.get('proofreading_suggestions', {}).get('summary', 'なし')}

改善提案:
"""
        
        suggestions = result.get('proofreading_suggestions', {}).get('suggestions', [])
        for i, suggestion in enumerate(suggestions, 1):
            report_content += f"{i}. {suggestion}\n"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
        except Exception as e:
            click.echo(f"⚠️  レポート保存に失敗しました: {str(e)}")
    
    def list_files(self, pattern: str):
        """List available markdown files for proofreading"""
        try:
            file_manager = FileManager()
            markdown_files = file_manager.find_markdown_files(pattern)
            
            # Filter files to only include those in articles/, books/, knowledges/
            target_dirs = ['articles/', 'books/', 'knowledges/']
            filtered_files = [f for f in markdown_files if any(f.startswith(d) for d in target_dirs)]
            
            click.echo(f"📄 発見されたマークダウンファイル ({len(filtered_files)}件):")
            
            for file_path in filtered_files:
                click.echo(f"   • {file_path}")
            
            if not filtered_files:
                click.echo("   マークダウンファイルが見つかりませんでした。")
            
        except Exception as e:
            click.echo(f"❌ エラーが発生しました: {str(e)}")