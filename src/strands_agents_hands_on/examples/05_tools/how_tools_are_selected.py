"""uv run python -m strands_agents_hands_on.examples.05_tools.how_tools_are_selected"""

import json

from mcp import StdioServerParameters, stdio_client
from strands import tool
from strands.tools.mcp import MCPClient


@tool(
    name="calculator",
    description="数値計算を実行するツール。加算、減算、乗算、除算",
)
def calculator(x: float, y: float, operation: str) -> float:
    """数値計算を実行するツール。

    Args:
        x: 第一オペランド
        y: 第二オペランド
        operation: 演算の種類 (add, subtract, multiply, divide)

    Returns:
        計算結果

    """
    if operation == "add":
        return x + y
    if operation == "subtract":
        return x - y
    if operation == "multiply":
        return x * y
    if operation == "divide":
        if y == 0:
            msg = "ゼロで除算することはできません"
            raise ZeroDivisionError(msg)
        return x / y
    msg = f"不正な演算子: {operation}"
    raise ValueError(msg)


# Python Toolのスペック確認
print("=" * 80)
print("【Python Tool】LLMに渡されるツール情報")
print("=" * 80)

python_tool_spec = calculator.tool_spec

print(f"\n【ツール名 (name)】: {python_tool_spec['name']}")
print(f"\n【説明文 (description)】:\n{python_tool_spec.get('description', 'なし')}")
print("\n【入力スキーマ (inputSchema)】:")
if "inputSchema" in python_tool_spec:
    print(json.dumps(python_tool_spec["inputSchema"], indent=2, ensure_ascii=False))
print("\n【出力スキーマ (outputSchema)】:")
if "outputSchema" in python_tool_spec:
    print(json.dumps(python_tool_spec["outputSchema"], indent=2, ensure_ascii=False))
else:
    print("なし")


# MCP Toolのスペック確認
print("\n" + "=" * 80)
print("【MCP Tool】LLMに渡されるツール情報")
print("=" * 80)

fetch_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch@latest"],
        )
    )
)

with fetch_mcp_client:
    mcp_tools = fetch_mcp_client.list_tools_sync()

    if mcp_tools:
        mcp_tool_spec = mcp_tools[0].tool_spec

        print(f"\n【ツール名 (name)】: {mcp_tool_spec['name']}")
        print(f"\n【説明文 (description)】:\n{mcp_tool_spec.get('description', 'なし')}")
        print("\n【入力スキーマ (inputSchema)】:")
        if "inputSchema" in mcp_tool_spec:
            print(json.dumps(mcp_tool_spec["inputSchema"], indent=2, ensure_ascii=False))
        print("\n【出力スキーマ (outputSchema)】:")
        if "outputSchema" in mcp_tool_spec:
            print(json.dumps(mcp_tool_spec["outputSchema"], indent=2, ensure_ascii=False))
        else:
            print("なし")
