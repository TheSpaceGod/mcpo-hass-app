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

The MCPO service listens on port `8000` inside the container. To expose it to your network, go to the add-on's configuration screen in Home Assistant, open the **Network** tab, and set a host port for `8000/tcp`. Setting it to `8000` matches the internal port and is recommended.

If you do not configure a host port mapping, the container will only be reachable from within the Home Assistant OS environment.

## Example Server Configs

### Home Assistant MCP Server (streamable-http)

A common use case is exposing the unofficial [Home Assistant MCP server](https://github.com/home-assistant-ai/ha-mcp) through MCPO:

```json
{
  "homeassistant": {
    "type": "streamable-http",
    "url": "http://your-hass-host:<ha-mcp-port>/api/mcp/<your-long-lived-access-token>"
  }
}
```

Replace `<ha-mcp-port>` with the port your Home Assistant MCP server is listening on, and `<your-long-lived-access-token>` with a valid Long-Lived Access Token from your Home Assistant profile.

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

#### Mixed Content Errors

If your Open WebUI instance runs over HTTPS and your Home Assistant add-on is only served over HTTP, your browser will block the connection as mixed content. This error may appear hidden in Open WebUI's developer settings rather than on the main screen. You have a few options to resolve this:

- **Allow insecure origins in your browser** — In Chrome, open `chrome://flags`, search for *Insecure Origins*, and add your Home Assistant URL (e.g. `http://hass.local:8000`). This is the quickest fix for local setups.
- **Use HTTPS on your HA host too** — Set up a reverse proxy (Nginx, Traefik, etc.) to serve both Open WebUI and this add-on over HTTPS.
- **Run Open WebUI without HTTPS** — Only recommended if you're running locally and aren't concerned about encryption in transit.

## Troubleshooting

- **Mixed Content error from Open WebUI** — If Open WebUI is served over HTTPS, the browser will block requests to the HTTP proxy. See the Mixed Content note above for workarounds.
- **Invalid JSON error**: Check your Servers JSON for proper format (trailing commas, missing quotes, etc.)
- **Server not starting**: Verify `command` and `args` are valid within the container environment
