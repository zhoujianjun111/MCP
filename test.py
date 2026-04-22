import os
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器实例，名称为 "FileSystem"
mcp = FastMCP("FileSystem")

@mcp.tool()
def get_desktop_files() -> list:
    """获取当前用户的桌面文件列表"""
    desktop_path = os.path.expanduser("~/Desktop")
    try:
        return os.listdir(desktop_path)
    except FileNotFoundError:
        return ["Desktop folder not found"]

@mcp.tool()
def calculator(a: float, b: float, operator: str) -> float:
    """
    执行基础数学运算（支持 + - * /）

    Args:
        a: 第一个数字
        b: 第二个数字
        operator: 运算符，必须是 '+', '-', '*', '/' 之一
    """
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b
    else:
        raise ValueError("无效运算符，请使用 + - * /")

if __name__ == "__main__":
    # 使用标准输入/输出通信（适合被 MCP 客户端调用）
    mcp.run(transport='stdio')