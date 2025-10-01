from pathlib import Path

from pydantic import BaseModel, Field
from strands import Agent


class ImageComparison(BaseModel):
    """2つの画像の比較結果"""

    image1_description: str = Field(description="1枚目の画像の説明")
    image2_description: str = Field(description="2枚目の画像の説明")
    differences: list[str] = Field(description="2つの画像の違いのリスト")
    similarities: list[str] = Field(description="2つの画像の共通点のリスト")
    overall_assessment: str = Field(description="全体的な評価・まとめ")


agent = Agent()

image1_path = Path("data/images/image1.png")
image2_path = Path("data/images/image2.png")

with image1_path.open("rb") as fp:
    image1_bytes = fp.read()

with image2_path.open("rb") as fp:
    image2_bytes = fp.read()

result = agent.structured_output(
    ImageComparison,
    [
        {"text": "これら2つの画像を比較して、違いを説明してください"},
        {"image": {"format": "png", "source": {"bytes": image1_bytes}}},
        {"image": {"format": "png", "source": {"bytes": image2_bytes}}},
    ],
)

print("=== 画像比較結果 ===")
print(f"\n【画像1の説明】\n{result.image1_description}")
print(f"\n【画像2の説明】\n{result.image2_description}")
print("\n【違い】")
for diff in result.differences:
    print(f"  - {diff}")
print("\n【共通点】")
for sim in result.similarities:
    print(f"  - {sim}")
print(f"\n【総合評価】\n{result.overall_assessment}")
