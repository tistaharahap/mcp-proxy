# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastMCP-based HTTP proxy server that bridges HTTP clients to MCP (Model Context Protocol) servers. The application serves as a streamable HTTP transport layer for MCP protocol communication.

**Key Architecture:**
- Single-file application (`main.py`) with Pydantic-based configuration
- Settings class with dual configuration support (file path or JSON string)
- FastMCP proxy initialization with configurable MCP server backends
- HTTP server with environment-based configuration

## Development Commands

### Core uv Commands
- `uv sync` - Install/sync dependencies from lockfile
- `uv run python main.py` - Run the proxy server locally
- `uv add <package>` - Add new dependency
- `uv remove <package>` - Remove dependency
- `uv lock` - Update lockfile with latest compatible versions

### Testing and Validation
- `uv run python -c "from main import settings; print(settings)"` - Validate settings loading
- `python -c "import json; json.load(open('mcp.json'))"` - Validate MCP config syntax

### Docker Operations
- `docker build -t mcp-proxy .` - Build container image
- `docker run -p 8080:8080 mcp-proxy` - Run container locally
- `docker run -p 8080:8080 --env-file .env mcp-proxy` - Run with environment file

## Configuration Architecture

### Settings Class (`main.py:11-27`)
The `Settings` class uses Pydantic BaseSettings with model validation:
- **Dual Config Support**: Either `config` (file path) or `config_json` (JSON string)
- **Validation Logic**: Ensures exactly one config method is provided
- **Auto-conversion**: JSON string config writes temporary config.json file
- **Environment Integration**: Supports .env file via python-dotenv

### MCP Configuration (`mcp.json`)

Follows Claude Desktop's MCP config schema.

## Code Patterns

### Configuration Pattern
```python
# Settings with dual config validation
class Settings(BaseSettings):
    config: str | None = Field(None, description="Path to MCP config file")
    config_json: str | None = Field(None, description="MCP config as JSON string")
    
    @model_validator(mode="after")
    def validate_config(self):
        # Ensure exactly one config method
```

### FastMCP Proxy Pattern
```python
# Configuration loading and proxy initialization
config = json.load(Path(settings.config).open())
proxy = FastMCP.as_proxy(config, name="Bango29 MCP Proxy")

# HTTP transport server
proxy.run(transport="streamable-http", host=settings.host, port=settings.port)
```

## Environment Variables

Required environment variables should be defined in `.env`:
- `CONFIG` - Path to MCP configuration file (alternative to config_json)
- `CONFIG_JSON` - JSON string with MCP configuration (alternative to config file)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8080)

## Dependencies

- **fastmcp>=2.11.3** - Core MCP protocol framework
- **pydantic-settings>=2.10.1** - Environment-based configuration management
- Python 3.13+ (specified in `.python-version`)

## Task Completion Checklist

When making changes:
1. Run `uv sync --locked` to verify dependencies
2. Test configuration: `uv run python -c "from main import settings; print(settings)"`
3. Validate MCP config: `python -c "import json; json.load(open('mcp.json'))"`
4. Test server startup: `uv run python main.py` (Ctrl+C to stop)
5. If Dockerfile changed: `docker build -t mcp-proxy .` and test run