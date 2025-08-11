import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from fastmcp import FastMCP, Context

async def main():
    # Define how to start the server via subprocess
    params = StdioServerParameters(
        command="python",
        args=["main.py"]
    )

    # Spawn the server and connect via stdio
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:",tools)


            result = await session.call_tool(
                name="add",
                arguments={
                    "a": 10,
                    "b": 5,
                }
            )
    
            print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
