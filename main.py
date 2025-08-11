from fastmcp import FastMCP, Context





mcp = FastMCP("context-demo-server")

@mcp.tool()
async def add(a: int, b: int, user_token: bytes,  ctx: Context):
    """Add two numbers, and print out context info if provided."""
    print(f"Context: {ctx}")
    await ctx.info("Adding two numbers....")
    # mcp.metadata.settings
    
    return f"{a} + {b} = {a + b} {ctx.request_context}"

if __name__ == "__main__":
    mcp.run()
