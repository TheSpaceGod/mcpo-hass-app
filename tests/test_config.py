import json
import subprocess

import pytest


def _wrap_config(servers):
    """Mimics what the run script produces: {"mcpServers": <servers>}."""
    return json.dumps({"mcpServers": servers})


class TestConfigGeneration:

    def test_jq_rejects_invalid_json(self):
        """Malformed JSON is caught before reaching MCP runtime."""
        bad_inputs = [
            "not json at all",
            "[{missing quotes}",
        ]
        for bad in bad_inputs:
            result = subprocess.run(
                ["jq", "empty"],
                input=bad,
                text=True,
                capture_output=True,
            )
            assert result.returncode != 0, f"Expected jq to reject: {bad}"

    def test_config_wrapping_structure(self):
        """The wrapper function produces valid MCP configuration structure."""
        servers = [
            {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
            },
        ]
        config = json.loads(_wrap_config(servers))

        assert "mcpServers" in config
        assert len(config["mcpServers"]) == 1
        assert config["mcpServers"][0]["command"] == "npx"

    def test_wrapped_config_is_valid_json(self):
        """Wrapped config parses cleanly with jq."""
        servers = [
            {"command": "echo", "args": ["test"]},
        ]
        wrapped = _wrap_config(servers)

        result = subprocess.run(
            ["jq", "."],
            input=wrapped,
            text=True,
            capture_output=True,
        )
        assert result.returncode == 0

    def test_wrapped_config_has_mcp_servers_key(self):
        """Wrapped config always has the mcpServers envelope."""
        servers = [{"name": "test-server"}]
        wrapped = _wrap_config(servers)

        parsed = json.loads(wrapped)
        assert "mcpServers" in parsed
        assert len(parsed) == 1
