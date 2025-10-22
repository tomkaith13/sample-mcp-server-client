# MCP Server with Context

A Model Context Protocol (MCP) server built with FastMCP that demonstrates middleware usage and context management.

## Overview

This project showcases how to build an MCP server with:
- **Custom Middleware**: Authentication and request logging using `UserAuthMiddleware`
- **Context Management**: Stateful information passing between middleware and tools
- **HTTP Transport**: Streamable HTTP server on port 8888

## Features

- **Custom Middleware** (`UserAuthMiddleware`):
  - Intercepts tool calls, requests, and tool listings
  - Logs request headers and metadata
  - Stores user authentication data (user_id, permissions) in context state

- **Tools**:
  - `add`: Simple addition with context-aware output showing user info
  - `calculate_health_savings_account_contributions`: Calculate HSA contributions

## Installation

```bash
# Install dependencies
uv sync
```

## Usage

### Running the Server

```bash
uv run main.py
```

The server will start on `http://localhost:8888` using streamable HTTP transport.

### Testing with MCP Client

```bash
python mcp-client.py
```

## Architecture

### Middleware Flow

1. **on_request**: Logs incoming request headers and method
2. **on_list_tools**: Intercepts tool listing requests
3. **on_call_tool**: Sets user context (user_id, permissions) before tool execution

### Context Usage

Tools can access middleware-set state via the `Context` object:

```python
user_id = ctx.get_state("user_id")
permissions = ctx.get_state("permissions")
```

## Requirements

- Python >= 3.13
- fastmcp >= 2.11.2
- mcp[cli] >= 1.12.4

## Project Structure

```
.
├── main.py           # MCP server with middleware
├── mcp-client.py     # Test client
├── pyproject.toml    # Project configuration
└── README.md         # This file
```

## License

See project documentation for license details.
