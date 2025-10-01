"""Usage example for custom SQLite session repository.

Usage:
    # 1回目の実行: 情報を伝える
    uv run python -m strands_agents_hands_on.examples.02_session.custom_session_management user-123

    # 2回目の実行: セッションが保存されているか確認
    uv run python -m strands_agents_hands_on.examples.02_session.custom_session_management user-123 second
"""

import json
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from strands import Agent
from strands.session.repository_session_manager import RepositorySessionManager
from strands.session.session_repository import SessionRepository
from strands.types.content import Message
from strands.types.session import Session, SessionAgent, SessionMessage, SessionType


class SQLiteSessionRepository(SessionRepository):
    """SQLite-based session repository implementation."""

    def __init__(self, db_path: str = "sessions.db") -> None:
        """Initialize SQLite session repository.

        Args:
            db_path: Path to the SQLite database file

        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    session_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Agents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    agent_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    conversation_manager_state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (session_id, agent_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            """)

            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    session_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    message_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    redact_message TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (session_id, agent_id, message_id),
                    FOREIGN KEY (session_id, agent_id) REFERENCES agents (session_id, agent_id)
                )
            """)

            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session_agent
                ON messages (session_id, agent_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_agents_session_id
                ON agents (session_id)
            """)

            conn.commit()

    # Session methods
    def create_session(self, session: Session, **_kwargs: Any) -> Session:
        """Create a new session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sessions (session_id, session_type, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session.session_id,
                    session.session_type.value,
                    session.created_at or datetime.now(UTC).isoformat(),
                    session.updated_at or datetime.now(UTC).isoformat(),
                ),
            )
            conn.commit()
        return session

    def read_session(self, session_id: str, **_kwargs: Any) -> Session | None:
        """Read a session by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT session_id, session_type, created_at, updated_at
                FROM sessions
                WHERE session_id = ?
                """,
                (session_id,),
            )
            row = cursor.fetchone()

            if row:
                return Session(
                    session_id=row[0],
                    session_type=SessionType(row[1]),
                    created_at=row[2],
                    updated_at=row[3],
                )
            return None

    # Agent methods
    def create_agent(self, session_id: str, session_agent: SessionAgent, **_kwargs: Any) -> None:
        """Create a new agent."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO agents (agent_id, session_id, state, conversation_manager_state, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session_agent.agent_id,
                    session_id,
                    json.dumps(session_agent.state),
                    json.dumps(session_agent.conversation_manager_state),
                    session_agent.created_at or datetime.now(UTC).isoformat(),
                    session_agent.updated_at or datetime.now(UTC).isoformat(),
                ),
            )
            conn.commit()

    def read_agent(self, session_id: str, agent_id: str, **_kwargs: Any) -> SessionAgent | None:
        """Read an agent by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT agent_id, state, conversation_manager_state, created_at, updated_at
                FROM agents
                WHERE session_id = ? AND agent_id = ?
                """,
                (session_id, agent_id),
            )
            row = cursor.fetchone()

            if row:
                return SessionAgent(
                    agent_id=row[0],
                    state=json.loads(row[1]),
                    conversation_manager_state=json.loads(row[2]),
                    created_at=row[3],
                    updated_at=row[4],
                )
            return None

    def update_agent(self, session_id: str, session_agent: SessionAgent, **_kwargs: Any) -> None:
        """Update an existing agent."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE agents
                SET state = ?, conversation_manager_state = ?, updated_at = ?
                WHERE session_id = ? AND agent_id = ?
                """,
                (
                    json.dumps(session_agent.state),
                    json.dumps(session_agent.conversation_manager_state),
                    datetime.now(UTC).isoformat(),
                    session_id,
                    session_agent.agent_id,
                ),
            )
            conn.commit()

    # Message methods
    def create_message(self, session_id: str, agent_id: str, session_message: SessionMessage, **_kwargs: Any) -> None:
        """Create a new message."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO messages (session_id, agent_id, message_id, message, redact_message, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    agent_id,
                    session_message.message_id,
                    json.dumps(dict(session_message.message)),
                    json.dumps(dict(session_message.redact_message)) if session_message.redact_message else None,
                    session_message.created_at or datetime.now(UTC).isoformat(),
                    session_message.updated_at or datetime.now(UTC).isoformat(),
                ),
            )
            conn.commit()

    def read_message(self, session_id: str, agent_id: str, message_id: int, **_kwargs: Any) -> SessionMessage | None:
        """Read a message by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT message_id, message, redact_message, created_at, updated_at
                FROM messages
                WHERE session_id = ? AND agent_id = ? AND message_id = ?
                """,
                (session_id, agent_id, message_id),
            )
            row = cursor.fetchone()

            if row:
                return SessionMessage(
                    message_id=row[0],
                    message=Message(**json.loads(row[1])),
                    redact_message=Message(**json.loads(row[2])) if row[2] else None,
                    created_at=row[3],
                    updated_at=row[4],
                )
            return None

    def update_message(self, session_id: str, agent_id: str, session_message: SessionMessage, **_kwargs: Any) -> None:
        """Update an existing message."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE messages
                SET message = ?, redact_message = ?, updated_at = ?
                WHERE session_id = ? AND agent_id = ? AND message_id = ?
                """,
                (
                    json.dumps(dict(session_message.message)),
                    json.dumps(dict(session_message.redact_message)) if session_message.redact_message else None,
                    datetime.now(UTC).isoformat(),
                    session_id,
                    agent_id,
                    session_message.message_id,
                ),
            )
            conn.commit()

    def list_messages(
        self,
        session_id: str,
        agent_id: str,
        limit: int | None = None,
        offset: int = 0,
        **_kwargs: Any,
    ) -> list[SessionMessage]:
        """List messages for a session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = """
                SELECT message_id, message, redact_message, created_at, updated_at
                FROM messages
                WHERE session_id = ? AND agent_id = ?
                ORDER BY message_id ASC
                LIMIT ? OFFSET ?
            """

            # SQLite requires explicit limit, use -1 for no limit
            actual_limit = limit if limit is not None else -1
            cursor.execute(query, (session_id, agent_id, actual_limit, offset))
            rows = cursor.fetchall()

            return [
                SessionMessage(
                    message_id=row[0],
                    message=Message(**json.loads(row[1])),
                    redact_message=Message(**json.loads(row[2])) if row[2] else None,
                    created_at=row[3],
                    updated_at=row[4],
                )
                for row in rows
            ]


if __name__ == "__main__":
    MIN_ARGS = 2
    SECOND_ARG_INDEX = 2

    if len(sys.argv) < MIN_ARGS:
        print("Error: session_id が必要です")
        print(
            "Usage: python -m strands_agents_hands_on.examples.02_session."
            "custom_session_management <session_id> [second]"
        )
        sys.exit(1)

    session_id = sys.argv[1]

    # SQLiteセッションリポジトリを作成
    db_path = "data/sessions.db"
    Path("data").mkdir(exist_ok=True)
    sqlite_repo = SQLiteSessionRepository(db_path=db_path)

    # カスタムリポジトリを使ってセッションマネージャーを作成
    session_manager = RepositorySessionManager(
        session_id=session_id,
        session_repository=sqlite_repo,
    )

    # エージェントを作成
    agent = Agent(session_manager=session_manager)

    # 1回目と2回目の実行を切り替え
    if len(sys.argv) > SECOND_ARG_INDEX and sys.argv[SECOND_ARG_INDEX] == "second":
        # 2回目の実行: 会話履歴を参照する質問
        print(f"=== 2回目の実行 (session_id: {session_id}) ===")
        response = agent("さっき私が教えた数字は何でしたか?")
    else:
        # 1回目の実行: 情報を伝える
        print(f"=== 1回目の実行 (session_id: {session_id}) ===")
        response = agent("私の好きな数字は42です。覚えておいてください。")
        print("\n次に 'second' 引数をつけて実行してセッション永続化をテストしてください:")
        print(
            "uv run python -m strands_agents_hands_on.examples.02_session."
            f"custom_session_management {session_id} second"
        )
        print(f"\nセッションデータの保存先: {db_path}")
        print("データベースの確認: sqlite3 data/sessions.db")
