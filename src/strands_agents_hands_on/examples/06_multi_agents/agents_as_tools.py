"""uv run python -m strands_agents_hands_on.examples.06_multi_agents.agents_as_tools"""

from strands import Agent, tool


@tool
def research_destination(query: str) -> str:
    """旅行先をリサーチするツール。

    Args:
        query: リサーチクエリ (場所、テーマなど)

    Returns:
        リサーチ結果

    """
    research_agent = Agent(
        system_prompt="""
あなたは旅行先のリサーチを専門とするアシスタントです。
指定された場所について、気候、観光スポット、文化、注意事項などを調査して報告してください。
    """.strip(),
    )
    return str(research_agent(query))


@tool
def recommend_product(requirements: str) -> str:
    """商品を推薦するツール。

    Args:
        requirements: 商品要件 (用途、条件など)

    Returns:
        商品推薦結果

    """
    product_agent = Agent(
        system_prompt="""
あなたは商品推薦を専門とするアシスタントです。
ユーザーの要件に基づいて、最適な商品を推薦してください。
具体的な商品名、特徴、価格帯、おすすめポイントを含めてください。
    """.strip(),
    )
    return str(product_agent(requirements))


orchestrator = Agent(
    system_prompt="""
あなたはユーザーの要求を理解し、適切な専門エージェントに作業を委譲するオーケストレーターです。
ユーザーの要求に応じて適切なツールを使用し、結果を統合して回答してください。
    """.strip(),
    tools=[research_destination, recommend_product],
)

print("=" * 80)
print("Agents as Tools パターンの実行")
print("=" * 80)

result = orchestrator("パタゴニア旅行に適したハイキングブーツを探しています")
