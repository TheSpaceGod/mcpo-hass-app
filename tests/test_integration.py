
import time

import pytest
import requests


class TestMcpoIntegration:

    def test_mcpo_start_and_serve(self, docker_sdk, mcpo_image):
        """mcpo starts and serves on port 8000 with a valid config."""
        config_json = '{"mcpServers": []}'

        container = docker_sdk.containers.run(
            mcpo_image,
            command=f"sh -c \"echo '{config_json}' > /data/mcpo-config.json && mcpo --config /data/mcpo-config.json --port 8000\"",
            ports={"8000/tcp": None},
            detach=True,
        )

        host = container.attrs["NetworkSettings"]["Ports"]["8000/tcp"][0]["HostIp"]
        port = int(container.attrs["NetworkSettings"]["Ports"]["8000/tcp"][0]["HostPort"])

        self._wait_for_ready(host, port)

        resp = requests.get(f"http://{host}:{port}/")
        assert resp.status_code == 200

        container.stop()

    def test_mcpo_with_api_key(self, docker_sdk, mcpo_image):
        """mcpo accepts optional --api-key flag without crashing."""
        config_json = '{"mcpServers": []}'

        container = docker_sdk.containers.run(
            mcpo_image,
            command=f"sh -c \"echo '{config_json}' > /data/mcpo-config.json && mcpo --config /data/mcpo-config.json --port 8000 --api-key test-secret\"",
            ports={"8000/tcp": None},
            detach=True,
        )

        host = container.attrs["NetworkSettings"]["Ports"]["8000/tcp"][0]["HostIp"]
        port = int(container.attrs["NetworkSettings"]["Ports"]["8000/tcp"][0]["HostPort"])

        self._wait_for_ready(host, port)

        resp = requests.get(f"http://{host}:{port}/")
        assert resp.status_code in (200, 401, 403)

        container.stop()

    def test_mcpo_with_custom_port(self, docker_sdk, mcpo_image):
        """mcpo starts on a configurable port."""
        config_json = '{"mcpServers": []}'
        custom_port = 9090

        container = docker_sdk.containers.run(
            mcpo_image,
            command=f"sh -c \"echo '{config_json}' > /data/mcpo-config.json && mcpo --config /data/mcpo-config.json --port {custom_port}\"",
            ports={f"{custom_port}/tcp": None},
            detach=True,
        )

        host = container.attrs["NetworkSettings"]["Ports"][f"{custom_port}/tcp"][0]["HostIp"]
        port = int(container.attrs["NetworkSettings"]["Ports"][f"{custom_port}/tcp"][0]["HostPort"])

        self._wait_for_ready(host, port)

        resp = requests.get(f"http://{host}:{port}/")
        assert resp.status_code == 200

        container.stop()

    @staticmethod
    def _wait_for_ready(host: str, port: int, timeout: int = 25):
        """Poll until the HTTP port responds."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                requests.get(f"http://{host}:{port}/", timeout=2)
                return
            except (requests.ConnectionError, requests.ReadTimeout):
                time.sleep(0.5)
        raise RuntimeError(f"Port {port} did not become ready within {timeout}s")
