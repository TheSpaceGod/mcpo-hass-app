# MCPO Home Assistant App Repository

Home Assistant app repository that wraps [MCPO](https://github.com/open-webui/mcpo) — the MCP-to-OpenAPI proxy server from Open WebUI.

Run MCPO as a managed container on Home Assistant OS to expose MCP tool servers as HTTP endpoints, enabling remote Open WebUI instances to connect to MCP servers running locally or on your LAN.

## Apps

This repository contains the following apps:

### [mcpo](./mcpo)

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

Run the MCP-to-OpenAPI proxy server with configurable MCP servers via the Home Assistant app UI.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
