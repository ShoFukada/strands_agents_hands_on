from strands import Agent
from strands.hooks import AfterInvocationEvent, BeforeInvocationEvent

agent = Agent()


def before_invocation_callback(event: BeforeInvocationEvent) -> None:
    print(f"エージェント呼び出し開始: {event.agent.name}")


def after_invocation_callback(event: AfterInvocationEvent) -> None:
    print(f"エージェント呼び出し終了: {event.agent.name}")


agent.hooks.add_callback(BeforeInvocationEvent, before_invocation_callback)
agent.hooks.add_callback(AfterInvocationEvent, after_invocation_callback)

agent("AIエージェントについて教えてください")
