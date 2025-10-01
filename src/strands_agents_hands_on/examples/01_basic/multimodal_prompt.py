from pathlib import Path

from strands import Agent

agent = Agent()

image1_path = Path("data/images/image1.png")
image2_path = Path("data/images/image2.png")

with image1_path.open("rb") as fp:
    image1_bytes = fp.read()

with image2_path.open("rb") as fp:
    image2_bytes = fp.read()

response = agent(
    [
        {"text": "これら2つの画像を比較して、違いを説明してください"},
        {"image": {"format": "png", "source": {"bytes": image1_bytes}}},
        {"image": {"format": "png", "source": {"bytes": image2_bytes}}},
    ]
)
