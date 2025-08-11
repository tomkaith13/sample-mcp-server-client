from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
class UserAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        print(f"context: {context}")
        print("Transport:", getattr(context, "transport", None))

        # Middleware stores user info in context state
        context.fastmcp_context.set_state("user_id", "user_123")
        context.fastmcp_context.set_state("permissions", ["read", "write"])
        
        return await call_next(context)


mcp = FastMCP("context-demo-server")
mcp.add_middleware(UserAuthMiddleware())


@mcp.tool
async def add(a: int, b: int,  ctx: Context):
    """Add two numbers, and print out context info if provided."""
    
    await ctx.info("Adding two numbers....")
    # mcp.metadata.settings


    

    user_id = ctx.get_state("user_id")
    permissions = ctx.get_state("permissions")

    return f"{a} + {b} = {a + b} User ID: {user_id} Permissions: {permissions}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
