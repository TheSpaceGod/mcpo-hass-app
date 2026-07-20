import os
import pytest

MCPO_DOCKERFILE = os.path.join(os.path.dirname(__file__), "..", "mcpo")
IMAGE_TAG = "mcpo-test:latest"


@pytest.fixture(scope="session")
def docker_sdk():
    import docker
    return docker.from_env()


@pytest.fixture(scope="session")
def mcpo_image(docker_sdk):
    """Build the mcpo Docker image once for all tests.

    Raises SkipTest if the build fails (e.g., no network inside containers).
    """
    try:
        _build_image(docker_sdk, IMAGE_TAG)
        # Verify it exists
        docker_sdk.images.get(IMAGE_TAG)
    except Exception as exc:
        pytest.skip(f"Could not build MCPo image: {exc}")

    yield IMAGE_TAG


def _build_image(client, tag):
    for line in client.api.build(
        path=MCPO_DOCKERFILE,
        tag=tag,
        dockerfile="Dockerfile",
        rm=True,
        decode=True,
    ):
        if "error" in line:
            raise RuntimeError(line["error"])
