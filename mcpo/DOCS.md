# mcpo MCP Proxy for Home Assistant

Expose MCP tool servers as OpenAPI-compatible HTTP endpoints via the [MCPO proxy](https://github.com/open-webui/mcpo). This is useful for connecting remote Open WebUI instances to MCP servers running on or near your Home Assistant installation.

## Overview

MCPO converts stdio-based MCP servers into standard RESTful OpenAPI endpoints that Open WebUI can consume over HTTP.

This app runs MCPO inside a Home Assistant managed container, with configurable MCP servers defined via the app's configuration UI.

## Configuration

| Setting | Description |
|---|---|
| **MCP Servers JSON** | JSON object defining your MCP servers (same format as Claude Desktop config) |
| **API Key** | Optional API key to protect the proxy endpoint |

### Port

The MCPO service listens on port `8000` inside the container. To access it remotely, set a host port mapping in the app's network settings after installation.

## Example Server Configs

### Local stdio command (using uvx)
```json
{
  "time": {
    "command": "uvx",
    "args": ["mcp-server-time", "--local-timezone=America/New_York"]
  }
}
```

### Local stdio command (using npx)
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  }
}
```

### SSE-style server
```json
{
  "sse-server": {
    "type": "sse",
    "url": "http://192.168.1.50:3001/sse"
  }
}
```

### Multiple servers
```json
{
  "time": {
    "command": "uvx",
    "args": ["mcp-server-time"]
  },
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  },
  "sse-api": {
    "type": "sse",
    "url": "http://192.168.1.50:3001/sse"
  }
}
```

## Connecting from Open WebUI

Once running, the MCPO proxy is available at:

```
http://<your-hass-host>:<exposed-port>/<server-name>/docs
```

For example, with the default config and port `8000`:
- Tool endpoint: `http://<host>:8000/time`
- API docs: `http://<host>:8000/time/docs`

In Open WebUI, add an **OpenAPI tool server** pointing to the MCPO endpoint URL. If an API key is configured, pass it as the Bearer token.

## Troubleshooting

- **Invalid JSON error**: Check your Servers JSON for proper format (trailing commas, missing quotes, etc.)
- **Server not starting**: Verify `command` and `args` are valid within the container environment
