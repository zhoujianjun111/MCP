import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["test.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # list_tools() 返回一个对象，其中 tools 属性是工具列表
            tools_result = await session.list_tools()
            tools = tools_result.tools
            print("可用工具：", [tool.name for tool in tools])

            # 调用 get_desktop_files
            result = await session.call_tool("get_desktop_files", arguments={})
            print("桌面文件：", result.content[0].text)

            # 调用 calculator
            result = await session.call_tool(
                "calculator",
                arguments={"a": 10, "b": 3, "operator": "/"}
            )
            print("10 / 3 =", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())