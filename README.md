# MCP Server 从零开发指南

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-green.svg)](https://modelscope.cn/mcp)

## 📖 简介

本项目是一个基于 MCP (Model Context Protocol) 协议的服务器端示例，展示如何从零开发一个 MCP 服务。MCP 为大语言模型提供了标准化的工具调用接口，让 AI 能够执行文件操作、数学计算等实际功能。

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建 Python 3.13+ 虚拟环境
conda create -n MCP python=3.13
conda activate MCP
```

### 2. 安装依赖

```bash
# 安装 MCP 库
pip install mcp
pip install mcp[cli]
```

### 3. 创建服务器端代码

创建 `test.py` 文件：

```python
import os
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("FileSystem")  # 服务名称

@mcp.tool()
def get_desktop_files() -> list:
    """获取当前用户的桌面文件列表"""
    return os.listdir(os.path.expanduser("~/Desktop"))

@mcp.tool()
def calculator(a: float, b: float, operator: str) -> float:
    """执行基础数学运算（支持+-*/）
    
    Args:
        a: 第一个数字
        b: 第二个数字  
        operator: 运算符，必须是'+','-','*','/'之一
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
    mcp.run(transport='stdio')  # 使用标准输入输出通信
```

### 4. 启动服务

```bash
# 方式一：直接运行
python test.py

# 方式二：使用 MCP 开发模式
mcp dev test.py
```

> ✅ 启动成功后终端没有任何输出，服务持续运行中

### 5. 查看服务状态

```bash
# 查看 MCP 服务器后台进程
ps aux | grep mcp
```

## 🔌 客户端连接示例

创建 `client.py` 来连接 MCP 服务器：

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters

async def main():
    # 配置服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["test.py"]
    )
    
    # 创建客户端会话
    async with ClientSession(server_params) as session:
        # 初始化连接
        await session.initialize()
        
        # 获取可用工具列表
        tools = await session.list_tools()
        print("可用工具:", [tool.name for tool in tools])
        
        # 调用 calculator 工具
        result = await session.call_tool(
            "calculator",
            arguments={"a": 10, "b": 5, "operator": "+"}
        )
        print(f"10 + 5 = {result.content[0].text}")
        
        # 调用 get_desktop_files 工具
        files = await session.call_tool("get_desktop_files")
        print(f"桌面文件: {files.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

运行客户端：

```bash
python client.py
```

## 📚 相关资源

- [魔搭 MCP 广场](https://modelscope.cn/mcp) - 发现更多 MCP 服务
- [MCP 官方文档](https://modelcontextprotocol.io)

## 📝 注意事项

- Python 版本必须 ≥ 3.13
- 确保 `~/Desktop` 目录存在（Linux/macOS）
- Windows 用户需将路径修改为 `~/Desktop` 或 `C:\\Users\\用户名\\Desktop`

## 📄 License

MIT