#!/usr/bin/env python3
"""
Proofreading Agent System
記事校閲エージェントシステム

使用方法:
    python main.py proofread -f path/to/article.md
    python main.py list-files -p "*.md"
    
環境設定:
    1. uv sync
    2. .env.templateを参考に.envファイルを作成
    3. 必要なAPIキーを.envファイルに設定
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from cli import cli

if __name__ == '__main__':
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8以上が必要です")
        sys.exit(1)
    
    # Check if running from correct directory
    if not (current_dir / 'pyproject.toml').exists():
        print("❌ Proofreadingディレクトリから実行してください")
        sys.exit(1)
    
    # Run CLI
    try:
        cli()
    except KeyboardInterrupt:
        print("\n❌ ユーザーによって中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラー: {str(e)}")
        sys.exit(1)