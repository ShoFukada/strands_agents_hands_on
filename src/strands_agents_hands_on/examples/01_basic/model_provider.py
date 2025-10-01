from strands import Agent
from strands.models.openai import OpenAIModel

from strands_agents_hands_on.config import Settings

settings = Settings()

model = OpenAIModel(
    client_args={
        "api_key": settings.OPENAI_API_KEY,
    },
    model_id="gpt-5-mini",
    params={"reasoning_effort": "minimal"},
)

agent = Agent(model=model)

response = agent("AIエージェントについて教えてください")
