from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
class UserAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        request = context.fastmcp_context.get_http_request()
        
        # print("request::", request.__dict__)
        print(f"[ON_CALL_TOOL] Request headers: {request.headers}")
        session = context.fastmcp_context.session
        # print("Session:", session.__dict__)

        print(f"[ON_CALL_TOOL] Transport: {getattr(context, 'transport', None)}")


        # Middleware stores user info in context state
        context.fastmcp_context.set_state("user_id", "user_123")
        context.fastmcp_context.set_state("permissions", ["read", "write"])
        
        return await call_next(context)
    
    async def on_request(self, context: MiddlewareContext, call_next):
        request = context.fastmcp_context.get_http_request()

        print(f"[ON_REQUEST] Request headers: {request.headers}")
        print(f"[ON_REQUEST] Request method: {context.method}")
        return await call_next(context)
    
    async def on_list_tools(self, context, call_next):

        print("[ON_LIST_TOOLS] Listing tools...")
        print(f"[ON_LIST_TOOLS] Method: {context.method}")
        
        request = context.fastmcp_context.get_http_request()
        print(f"[ON_LIST_TOOLS] header: {request.headers}")
        return await call_next(context)


mcp = FastMCP("benefits_mcp")
mcp.add_middleware(UserAuthMiddleware())


@mcp.tool
async def add(a: int, b: int,  ctx: Context):
    """Add two numbers, and print out context info if provided."""
    
    await ctx.info("Adding two numbers....")
    # mcp.metadata.settings
    user_id = ctx.get_state("user_id")
    permissions = ctx.get_state("permissions")

    return f"{a} + {b} = {a + b} User ID: {user_id} Permissions: {permissions}"


@mcp.tool(
        name="calculate_health_savings_account_contributions",
        description="Calculate potential health savings account (referred to as HSA) contributions.",
)
async def calculate_health_savings_account_contributions(ctx: Context) -> int:
    """Calculate potential health savings account (referred to as HSA) contributions."""

    await ctx.info("Calculating health savings account (HSA) contributions...")
    return 42

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8888)
