import asyncio
import argparse
import uuid
from dotenv import load_dotenv

from agent.runner import stream_agent_events

# .envファイルを読み込む
load_dotenv()

async def main():
    """Main entry point for the agent application."""
    parser = argparse.ArgumentParser(description="Agent application")
    parser.add_argument("--session", required=False, help="Session ID")
    parser.add_argument("--query", required=True, help="Query string")
    args = parser.parse_args()

    session_id = args.session if args.session else str(uuid.uuid4())
    query = args.query
    user_id = "default_user"  # or set as needed
    async for message in stream_agent_events(query=query, user_id=user_id, session_id=session_id):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())