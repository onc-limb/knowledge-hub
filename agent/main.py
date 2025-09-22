import asyncio
import argparse
from pathlib import Path
import uuid
from dotenv import load_dotenv

from agent.runner import stream_agent_events
from agent.utils.file_manager import FileManager
import os

# .envファイルを読み込む
load_dotenv()

async def main():
    """Main entry point for the agent application."""
    parser = argparse.ArgumentParser(description="Agent application")
    parser.add_argument("--file", required=True, help="File path")
    parser.add_argument("--session", required=False, help="Session ID")
    parser.add_argument("--query", required=False, help="Query string")
    args = parser.parse_args()

    file_path = args.file

    project_root = Path(__file__).resolve().parent.parent
    print(f"Project root directory: {project_root}")
    file_manager = FileManager(project_root)
    query = file_manager.read_markdown_file(file_path)

    session_id = args.session if args.session else str(uuid.uuid4())
    user_id = "default_user"
    async for message in stream_agent_events(query=query, user_id=user_id, session_id=session_id):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())