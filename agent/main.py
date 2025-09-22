import asyncio
import argparse

from agent.runner import stream_agent_events

async def main():
    """Main entry point for the agent application."""
    parser = argparse.ArgumentParser(description="Agent application")
    parser.add_argument("--session", required=False, help="Session ID")
    parser.add_argument("--query", required=True, help="Query string")
    args = parser.parse_args()

    session_id = args.session
    query = args.query
    user_id = "default_user"  # or set as needed
    async for message in stream_agent_events(query=query, user_id=user_id, session_id=session_id):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())