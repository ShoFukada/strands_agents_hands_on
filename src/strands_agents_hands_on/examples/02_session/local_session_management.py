"""Usage example for session management.

Usage:
    # 1回目の実行: 情報を伝える
    uv run python -m strands_agents_hands_on.examples.02_session.local_session_management user-123

    # 2回目の実行: セッションが保存されているか確認
    uv run python -m strands_agents_hands_on.examples.02_session.local_session_management user-123 second
"""

import sys

from strands import Agent
from strands.session.file_session_manager import FileSessionManager

MIN_ARGS = 2
SECOND_ARG_INDEX = 2

if len(sys.argv) < MIN_ARGS:
    print("Error: session_id が必要です")
    print("Usage: python -m strands_agents_hands_on.examples.02_session.local_session_management <session_id> [second]")
    sys.exit(1)

session_id = sys.argv[1]

session_manager = FileSessionManager(
    session_id=session_id,
    storage_dir="./data/sessions",
)

agent = Agent(session_manager=session_manager)

if len(sys.argv) > SECOND_ARG_INDEX and sys.argv[SECOND_ARG_INDEX] == "second":
    print(f"=== 2回目の実行 (session_id: {session_id}) ===")
    response = agent("さっき私が教えた数字は何でしたか?")
else:
    # 1回目の実行: 情報を伝える
    print(f"=== 1回目の実行 (session_id: {session_id}) ===")
    response = agent("私の好きな数字は42です。覚えておいてください。")
    print("\n次に 'second' 引数をつけて実行してセッション永続化をテストしてください:")
    print(f"uv run python -m strands_agents_hands_on.examples.02_session.local_session_management {session_id} second")
