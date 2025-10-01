
### テーブル構造

#### sessions テーブル
セッションの基本情報を保存します。

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| session_id | TEXT | PRIMARY KEY | セッションの一意識別子 |
| session_type | TEXT | NOT NULL | セッションのタイプ |
| created_at | TEXT | NOT NULL | セッション作成日時 (ISO8601形式) |
| updated_at | TEXT | NOT NULL | セッション更新日時 (ISO8601形式) |

#### agents テーブル
エージェントの状態と会話管理の情報を保存します。

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| agent_id | TEXT | PRIMARY KEY (複合) | エージェントの一意識別子 |
| session_id | TEXT | PRIMARY KEY (複合), FOREIGN KEY | 所属するセッションID |
| state | TEXT | NOT NULL | エージェントの状態 (JSON形式) |
| conversation_manager_state | TEXT | NOT NULL | 会話管理の状態 (JSON形式) |
| created_at | TEXT | NOT NULL | エージェント作成日時 (ISO8601形式) |
| updated_at | TEXT | NOT NULL | エージェント更新日時 (ISO8601形式) |

#### messages テーブル
会話のメッセージを保存します。

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| session_id | TEXT | PRIMARY KEY (複合), FOREIGN KEY | 所属するセッションID |
| agent_id | TEXT | PRIMARY KEY (複合), FOREIGN KEY | 所属するエージェントID |
| message_id | INTEGER | PRIMARY KEY (複合) | メッセージの一意識別子 |
| message | TEXT | NOT NULL | メッセージ内容 (JSON形式) |
| redact_message | TEXT | NULL | 編集済みメッセージ (JSON形式, オプション) |
| created_at | TEXT | NOT NULL | メッセージ作成日時 (ISO8601形式) |
| updated_at | TEXT | NOT NULL | メッセージ更新日時 (ISO8601形式) |
