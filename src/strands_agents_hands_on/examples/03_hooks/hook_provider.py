from strands import Agent
from strands.hooks import AfterInvocationEvent, BeforeInvocationEvent, HookProvider, HookRegistry

agent = Agent()


class LoggingHook(HookProvider):
    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:  # noqa: ANN003
        registry.add_callback(BeforeInvocationEvent, self.before_invocation_callback)
        registry.add_callback(AfterInvocationEvent, self.after_invocation_callback)

    def before_invocation_callback(self, event: BeforeInvocationEvent) -> None:
        print(f"エージェント呼び出し開始: {event.agent.name}")

    def after_invocation_callback(self, event: AfterInvocationEvent) -> None:
        print(f"エージェント呼び出し終了: {event.agent.name}")


agent.hooks.add_hook(LoggingHook())

agent("AIエージェントについて教えてください")
