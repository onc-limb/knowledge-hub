#!/usr/bin/env python3
"""
Test script to run the root agent using ADK Runner directly
"""

import asyncio
from google.adk.runners import InMemoryRunner
from agent.root_agent import root_agent


async def main():
    """Test the root agent with a simple message"""
    
    # Create an in-memory runner with the agent
    runner = InMemoryRunner(app_name="ProofreadingTest", agent=root_agent)
    
    # Test message
    message = "テストファイルの内容を分析してください。以下はサンプルMarkdownファイルです:\n\n# テスト記事\n\nこれはテストの記事です。AIについて書かれています。機械学習は重要な技術です。"
    
    print("=== ADK Root Agent テスト開始 ===")
    print(f"メッセージ: {message}")
    print("\n=== 実行開始 ===")
    
    try:
        # Run the agent
        result = await runner.run(message)
        
        print("\n=== 実行結果 ===")
        print(result)
        
    except Exception as e:
        print(f"\n=== エラーが発生しました ===")
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())