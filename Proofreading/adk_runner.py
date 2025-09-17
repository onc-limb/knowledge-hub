#!/usr/bin/env python3
"""
ADK Runner - ADKコマンドを使用してエージェントを実行するためのヘルパー
"""

import asyncio
import subprocess
import tempfile
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ADKRunner:
    """ADKコマンドを使用してエージェントを実行するためのクラス"""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self.temp_dir = Path(tempfile.gettempdir()) / "adk_runner"
        self.temp_dir.mkdir(exist_ok=True)
    
    async def run_agent_with_file(self, agent_name: str, file_path: str, timeout: int = 60) -> Dict[str, Any]:
        """
        ADKコマンドを使用してエージェントを実行し、ファイルを分析する
        
        Args:
            agent_name: エージェント名 (evidence_agent, proofreading_agent など)
            file_path: 分析対象のファイルパス
            timeout: タイムアウト時間（秒）
            
        Returns:
            エージェントの実行結果
        """
        try:
            # エージェントディレクトリのパスを確認
            agent_path = self.agents_dir / agent_name
            if not agent_path.exists():
                return {
                    "error": f"Agent directory not found: {agent_path}",
                    "agent_name": agent_name
                }
            
            # 一時的なプロンプトファイルを作成
            prompt_file = self.temp_dir / f"{agent_name}_prompt.txt"
            
            # エージェントに送るプロンプトを作成
            if agent_name == "evidence_agent":
                prompt = f"""ファイル '{file_path}' のMarkdownコンテンツについて、エビデンス分析を行ってください。

以下の項目について詳細に分析してください：
1. 事実主張の検証と根拠の確認
2. 疑問のある主張や不正確な可能性がある内容の特定
3. 不足しているエビデンスや追加すべき情報源の指摘
4. 全体的な信頼性スコアの算出

分析結果を詳細なレポート形式で返してください。"""
            
            elif agent_name == "proofreading_agent":
                prompt = f"""ファイル '{file_path}' のMarkdownコンテンツについて、校正分析を行ってください。

以下の項目について詳細に分析してください：
1. 文法エラーや誤字脱字の検出
2. 文体やスタイルの改善提案
3. 文章構造や論理的流れの改善案
4. 読みやすさと理解しやすさの評価

分析結果を詳細なレポート形式で返してください。"""
            
            else:
                prompt = f"ファイル '{file_path}' の内容を分析してください。詳細なレポートを提供してください。"
            
            # プロンプトファイルに書き込み
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # ADKコマンドを構築
            cmd = [
                "adk", "run", str(agent_path),
                "--input", str(prompt_file)
            ]
            
            # ADKエージェントを実行
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            
            # 標準出力から結果を取得
            if process.returncode == 0:
                output = stdout.decode('utf-8') if stdout else ""
                return {
                    "success": True,
                    "agent_name": agent_name,
                    "output": output.strip(),
                    "analysis_type": "evidence" if "evidence" in agent_name else "proofreading"
                }
            else:
                error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
                return {
                    "error": f"ADK command failed with return code {process.returncode}",
                    "agent_name": agent_name,
                    "stderr": error_msg,
                    "stdout": stdout.decode('utf-8') if stdout else ""
                }
            
        except asyncio.TimeoutError:
            return {
                "error": f"ADK command timeout after {timeout} seconds",
                "agent_name": agent_name
            }
        except FileNotFoundError:
            return {
                "error": "ADK command not found. Please ensure ADK is installed and available in PATH.",
                "agent_name": agent_name
            }
        except Exception as e:
            return {
                "error": f"Execution error: {str(e)}",
                "agent_name": agent_name
            }
        finally:
            # 一時ファイルをクリーンアップ
            if prompt_file.exists():
                prompt_file.unlink()
    
    async def run_evidence_agent(self, file_path: str) -> Dict[str, Any]:
        """Evidence Agentを実行してファイルを分析"""
        return await self.run_agent_with_file("evidence_agent", file_path)
    
    async def run_proofreading_agent(self, file_path: str) -> Dict[str, Any]:
        """Proofreading Agentを実行してファイルを分析"""
        return await self.run_agent_with_file("proofreading_agent", file_path)
    
    async def check_adk_availability(self) -> bool:
        """ADKコマンドが利用可能かチェック"""
        try:
            process = await asyncio.create_subprocess_exec(
                "adk", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False
        except Exception:
            return False


# モジュールレベルの便利関数
_runner = None

def get_adk_runner() -> ADKRunner:
    """ADKRunnerのシングルトンインスタンスを取得"""
    global _runner
    if _runner is None:
        _runner = ADKRunner()
    return _runner


async def run_evidence_analysis(file_path: str) -> Dict[str, Any]:
    """Evidence Agentでファイル分析を実行する便利関数"""
    runner = get_adk_runner()
    return await runner.run_evidence_agent(file_path)


async def run_proofreading_analysis(file_path: str) -> Dict[str, Any]:
    """Proofreading Agentでファイル分析を実行する便利関数"""
    runner = get_adk_runner()
    return await runner.run_proofreading_agent(file_path)


async def check_adk_available() -> bool:
    """ADKコマンドが利用可能かチェックする便利関数"""
    runner = get_adk_runner()
    return await runner.check_adk_availability()