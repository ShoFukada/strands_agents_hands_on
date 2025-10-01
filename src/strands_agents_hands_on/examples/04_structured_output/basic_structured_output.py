from pydantic import BaseModel, Field
from strands import Agent


class AIAgentInfo(BaseModel):
    """AIエージェントに関する情報"""

    definition: str = Field(description="AIエージェントの定義")
    key_features: list[str] = Field(description="主な特徴のリスト")
    use_cases: list[str] = Field(description="具体的なユースケース")
    benefits: list[str] = Field(description="導入メリット")


agent = Agent()

result = agent.structured_output(
    AIAgentInfo,
    "AIエージェントについて教えてください",
)

print("=== AIエージェント情報 ===")
print(f"\n【定義】\n{result.definition}")
print("\n【主な特徴】")
for feature in result.key_features:
    print(f"  - {feature}")
print("\n【ユースケース】")
for use_case in result.use_cases:
    print(f"  - {use_case}")
print("\n【メリット】")
for benefit in result.benefits:
    print(f"  - {benefit}")
