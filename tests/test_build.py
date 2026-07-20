
import pytest


class TestDockerBuild:

    def test_image_exists(self, mcpo_image, docker_sdk):
        image = docker_sdk.images.get(mcpo_image)
        assert image.id is not None

    def test_has_mcpo_binary(self, docker_sdk, mcpo_image):
        container = docker_sdk.containers.run(
            mcpo_image,
            command=["mcpo", "--version"],
            remove=True,
        )
        # uv-installed mcpo returns 0 for --version or --help
        exit_code = container.get("State").get("ExitCode")
        assert exit_code == 0

    def test_has_jq(self, docker_sdk, mcpo_image):
        container = docker_sdk.containers.run(
            mcpo_image,
            command=["jq", "--version"],
            remove=True,
        )
        exit_code = container.get("State").get("ExitCode")
        assert exit_code == 0

    def test_has_node(self, docker_sdk, mcpo_image):
        container = docker_sdk.containers.run(
            mcpo_image,
            command=["node", "--version"],
            remove=True,
        )
        exit_code = container.get("State").get("ExitCode")
        assert exit_code == 0
