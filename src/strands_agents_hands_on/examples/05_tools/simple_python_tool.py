"""uv run python -m strands_agents_hands_on.examples.05_tools.simple_python_tool"""
from strands import Agent, tool


@tool
def calculator(x: float, y: float, operation: str) -> float:
    """数値計算を実行するツール。

    Args:
        x: 第一オペランド
        y: 第二オペランド
        operation: 演算の種類 (add, subtract, multiply, divide)

    Returns:
        計算結果

    Raises:
        ValueError: 不正な演算子が指定された場合
        ZeroDivisionError: ゼロ除算が発生した場合

    """
    if operation == "add":
        return x + y
    if operation == "subtract":
        return x - y
    if operation == "multiply":
        return x * y
    if operation == "divide":
        if y == 0:
            raise ZeroDivisionError("ゼロで除算することはできません")
        return x / y
    msg = f"不正な演算子: {operation}"
    raise ValueError(msg)


@tool
def temperature_converter(value: float, from_unit: str, to_unit: str) -> float:
    """温度単位を変換するツール。

    Args:
        value: 変換する温度の値
        from_unit: 元の単位 (celsius, fahrenheit, kelvin)
        to_unit: 変換先の単位 (celsius, fahrenheit, kelvin)

    Returns:
        変換後の温度

    """
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        msg = f"不正な単位: {from_unit}"
        raise ValueError(msg)

    if to_unit == "celsius":
        return celsius
    if to_unit == "fahrenheit":
        return celsius * 9 / 5 + 32
    if to_unit == "kelvin":
        return celsius + 273.15
    msg = f"不正な単位: {to_unit}"
    raise ValueError(msg)


agent = Agent(tools=[calculator, temperature_converter])

print("=== 計算ツールの使用 ===")
result1 = agent("125掛ける37はいくつ")

print("=== 温度変換ツールの使用 ===")
result2 = agent("摂氏25度は華氏で何度")

print("=== 複数のツールを組み合わせた使用 ===")
result3 = agent("摂氏20度と30度の平均を華氏で教えて")
