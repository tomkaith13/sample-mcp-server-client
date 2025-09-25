from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
class UserAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        request = context.fastmcp_context.get_http_request()
        
        # print("request::", request.__dict__)
        print(f"headers: {request.headers}")
        session = context.fastmcp_context.session
        # print("Session:", session.__dict__)

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


@mcp.tool
async def calculate_health_savings_account_contributions(ctx: Context) -> int:
    """Calculate potential health savings account contributions."""

    await ctx.info("Calculating health savings account contributions...")
    return 42

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8888)
