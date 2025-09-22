import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from root_agent import root_agent

# runner の定義
APP_NAME = "Proofreading Agent App"
SESSION_SERVICE = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=SESSION_SERVICE,
)

async def stream_agent_events(query: str, user_id: str, session_id: str):
    """Simulate streaming agent events based on the query, user_id, and session_id."""
    # セッションIDが提供されていることを確認
    if not session_id:
        raise ValueError("session_id cannot be None or empty")
    
    session = await SESSION_SERVICE.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session:
        await SESSION_SERVICE.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
  
    # ユーザークエリを所定の形式で格納
    content = types.Content(role='user', parts=[types.Part(text=query)])
  
    # エージェントの実行
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if not event.content:
            continue
        parts = event.content.parts
        if not parts:
            continue
        message = parts[0].text
        if message:
            yield(f"--- Message: {message}")
    return