"""uv run python -m strands_agents_hands_on.examples.05_tools.mcp_and_python_tools"""

from mcp import StdioServerParameters, stdio_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient


@tool
def analyze_stock_data(prices: list[float], volumes: list[int] | None = None) -> dict:
    """株価データを分析して統計情報を返すツール。

    Args:
        prices: 株価のリスト
        volumes: 取引量のリスト (オプション)

    Returns:
        株価の統計情報を含む辞書

    """
    if not prices:
        return {"error": "データがありません"}

    result = {
        "データ数": len(prices),
        "最高値": f"${max(prices):.2f}",
        "最安値": f"${min(prices):.2f}",
        "平均株価": f"${sum(prices) / len(prices):.2f}",
        "価格変動幅": f"${max(prices) - min(prices):.2f}",
        "変動率": f"{((max(prices) - min(prices)) / min(prices) * 100):.2f}%",
    }

    if volumes:
        result["平均取引量"] = f"{sum(volumes) / len(volumes):,.0f}"
        result["総取引量"] = f"{sum(volumes):,}"

    return result


@tool()
def format_stock_report(analysis_data: dict, company_info: dict | None = None) -> str:
    """株価分析結果をMarkdown形式のレポートとして整形するツール。

    Args:
        analysis_data: 株価分析データの辞書
        company_info: 企業情報の辞書 (オプション)

    Returns:
        Markdown形式のレポート文字列

    """
    report = "# 株価分析レポート\n\n"

    if company_info:
        report += "## 企業情報\n\n"
        for key, value in company_info.items():
            report += f"- **{key}**: {value}\n"
        report += "\n"

    report += "## 分析結果\n\n"
    report += "| 指標 | 値 |\n"
    report += "|------|------|\n"

    for key, value in analysis_data.items():
        report += f"| {key} | {value} |\n"

    return report


# Fetch MCP Serverへの接続設定
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

    agent = Agent(tools=[analyze_stock_data, format_stock_report, *mcp_tools])

    result = agent(
        """
以下のタスクを実行してください:

1. Alpha Vantage APIから株価データを取得
   URL: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo

2. 取得したJSONデータから直近10日分の終値を抽出

3. 抽出した株価データを分析

4. 分析結果をMarkdown形式のレポートとして整形して表示

エージェントは利用可能なツールを自動的に判断して使用してください。
"""
    )
