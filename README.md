# MCP Proxy

A FastMCP-based HTTP proxy server that bridges HTTP clients to MCP (Model Context Protocol) servers. This application provides a streamable HTTP transport layer for MCP protocol communication.

## Features

- **HTTP-to-MCP Bridge**: Converts HTTP requests to MCP protocol calls
- **Multiple MCP Backends**: Supports various MCP servers (GitHub, MongoDB, Context7, etc.)
- **Flexible Configuration**: File-based or JSON string configuration options
- **Environment Integration**: Supports .env files and environment variables
- **Docker Ready**: Containerized deployment with uv package management

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-proxy
```

2. Install dependencies:
```bash
uv sync
```

3. Configure MCP servers by either:
   - Setting `CONFIG` environment variable to path of your MCP config file
   - Setting `CONFIG_JSON` environment variable with JSON configuration string

### Running Locally

```bash
# Start the proxy server
uv run python main.py

# Or with custom host/port
HOST=localhost PORT=3000 uv run python main.py
```

The server will start on `http://0.0.0.0:8080` by default.

### Docker Deployment

```bash
# Build the image
docker build -t mcp-proxy .

# Run the container
docker run -p 8080:8080 --env-file .env mcp-proxy
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8080` |
| `CONFIG` | Path to MCP config file | None |
| `CONFIG_JSON` | MCP config as JSON string | None |

### MCP Configuration

The proxy requires either a `CONFIG` file path or `CONFIG_JSON` string. The configuration follows Claude Desktop's MCP server schema:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

## Development

### Adding Dependencies

```bash
# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name
```

### Testing Configuration

```bash
# Validate settings loading
uv run python -c "from main import settings; print(settings)"

# Validate MCP config syntax
python -c "import json; json.load(open('mcp.json'))"
```

### Development Workflow

1. Make code changes
2. Test configuration loading: `uv run python -c "from main import settings; print(settings)"`
3. Start server: `uv run python main.py`
4. Test endpoints and functionality
5. Validate with `uv sync --locked`

## Architecture

The application consists of:

- **Settings Class**: Pydantic-based configuration with validation
- **Dual Config Support**: File path or JSON string configuration methods
- **FastMCP Integration**: Proxy initialization with configurable backends
- **HTTP Transport**: Streamable HTTP server for MCP communication

### Key Components

- `main.py` - Single-file application with all core logic
- `pyproject.toml` - uv project configuration and dependencies
- `Dockerfile` - Container deployment configuration

## Troubleshooting

### Common Issues

**Configuration Errors**: Ensure exactly one of `CONFIG` or `CONFIG_JSON` is provided, not both.

**MCP Server Failures**: Check that required environment variables are set for external services.

**Port Conflicts**: Change the `PORT` environment variable if 8080 is already in use.

### Validation Commands

```bash
# Check dependency status
uv sync --locked

# Validate configuration
uv run python -c "from main import settings; print(settings)"

# Test MCP config
python -c "import json; json.load(open('mcp.json'))"
```

## License

MIT License. See `LICENSE` file for details.