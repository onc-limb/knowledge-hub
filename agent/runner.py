import asyncio
import os
from datetime import datetime
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

def create_log_file(user_id: str, session_id: str) -> str:
    """Create a unique log file path for agent output."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"agent_{user_id}_{session_id}_{timestamp}.log"
    
    return os.path.join(logs_dir, filename)

def write_to_log(log_file_path: str, message: str):
    """Write message to log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

async def stream_agent_events(query: str, user_id: str, session_id: str):
    """Simulate streaming agent events based on the query, user_id, and session_id."""
    # セッションIDが提供されていることを確認
    if not session_id:
        raise ValueError("session_id cannot be None or empty")
    
    # ログファイルを作成
    log_file_path = create_log_file(user_id, session_id)
    
    # ログ開始の記録
    write_to_log(log_file_path, f"=== Agent Session Started ===")
    write_to_log(log_file_path, f"User ID: {user_id}")
    write_to_log(log_file_path, f"Session ID: {session_id}")
    write_to_log(log_file_path, f"Query: {query}")
    write_to_log(log_file_path, f"Log File: {log_file_path}")
    write_to_log(log_file_path, "=" * 40)
    
    session = await SESSION_SERVICE.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session:
        await SESSION_SERVICE.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        write_to_log(log_file_path, "New session created")
    else:
        write_to_log(log_file_path, "Using existing session")
  
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
            # ログファイルに出力
            write_to_log(log_file_path, f"Agent Response: {message}")
            # 従来通りのストリーミング出力
            yield(f"--- Message: {message}")
    
    # ログ終了の記録
    write_to_log(log_file_path, "=" * 40)
    write_to_log(log_file_path, "=== Agent Session Completed ===")
    
    return