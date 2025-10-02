"""uv run python -m strands_agents_hands_on.examples.06_multi_agents.swarm_example"""

from strands import Agent
from strands.multiagent import Swarm

researcher = Agent(
    name="researcher",
    system_prompt="""
あなたはリサーチ担当のエージェントです。
技術的な要件や背景情報を調査し、必要に応じてcoderエージェントにハンドオフしてください。
    """.strip(),
)

coder = Agent(
    name="coder",
    system_prompt="""
あなたはコード実装担当のエージェントです。
要件に基づいてコードを実装し、完成したらreviewerエージェントにハンドオフしてください。
    """.strip(),
)

reviewer = Agent(
    name="reviewer",
    system_prompt="""
あなたはコードレビュー担当のエージェントです。
実装されたコードをレビューし、問題があればcoderにフィードバックを返し、
問題なければ最終レポートを作成してください。
    """.strip(),
)

# Swarmを作成
swarm = Swarm(
    [researcher, coder, reviewer],
    entry_point=researcher,  # 最初のエージェント
    max_handoffs=20,  # 最大ハンドオフ回数
    max_iterations=20,  # 最大反復回数
    execution_timeout=900,  # 合計タイムアウト (秒)
    node_timeout=300,  # 各エージェントのタイムアウト (秒)
    repetitive_handoff_detection_window=0,  # ピンポン動作検出の履歴ウィンドウサイズ(0だと無効)
    repetitive_handoff_min_unique_agents=0,  # ピンポン検出に必要な最小ユニークエージェント数(0だと無効)
)

# 実行
print("=" * 80)
print("Swarm パターンの実行")
print("=" * 80)
print("タスク: シンプルな計算機APIの設計と実装")
print("=" * 80)

result = swarm(
    """
シンプルな計算機のREST APIを設計して実装してください。
- 加算、減算、乗算、除算の4つの操作をサポート
- Pythonで実装
- エラーハンドリングを含める
"""
)
