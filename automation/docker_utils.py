"""
Docker Utilities docker SDK: list containers, build, exec.

The docker Python SDK lets you manage containers programmatically.
Useful for CI/CD scripts, testing, and automation.

Install: pip install docker
"""
import docker
from docker.errors import DockerException, ImageNotFound, NotFound


def get_client() -> docker.DockerClient:
    """Connect to Docker daemon.

    Uses the default socket (/var/run/docker.sock on Linux).
    Set DOCKER_HOST env var for remote Docker.
    """
    try:
        client = docker.from_env()
        client.ping()
        return client
    except DockerException as e:
        print(f"Cannot connect to Docker: {e}")
        print("Is Docker running? Try: systemctl start docker")
        raise


# =============================================================================
# CONTAINERS list, run, stop, exec
# =============================================================================

def list_containers(client: docker.DockerClient, all: bool = False) -> list[dict]:
    """List containers (running or all)."""
    containers = client.containers.list(all=all)
    return [
        {
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else c.image.short_id,
            "ports": c.ports,
        }
        for c in containers
    ]


def run_container(
    client: docker.DockerClient,
    image: str,
    name: str = None,
    command: str = None,
    ports: dict = None,
    environment: dict = None,
    volumes: dict = None,
    detach: bool = True,
    remove: bool = False,
) -> docker.models.containers.Container:
    """Run a container with common options.

    Args:
        image: Docker image (e.g., "python:3.12-slim")
        name: Container name
        command: Command to run
        ports: Port mapping {"8080/tcp": 8080}
        environment: Env vars {"KEY": "value"}
        volumes: Volume mapping {"/host/path": {"bind": "/container/path", "mode": "rw"}}
        detach: Run in background
        remove: Auto-remove when stopped
    """
    return client.containers.run(
        image,
        command=command,
        name=name,
        ports=ports,
        environment=environment,
        volumes=volumes,
        detach=detach,
        remove=remove,
    )


def exec_in_container(
    client: docker.DockerClient,
    container_name: str,
    command: str,
    workdir: str = None,
) -> tuple[int, str]:
    """Execute a command inside a running container.

    Returns (exit_code, output).
    """
    try:
        container = client.containers.get(container_name)
        result = container.exec_run(
            command,
            workdir=workdir,
            demux=True,
        )
        stdout = result.output[0].decode() if result.output[0] else ""
        stderr = result.output[1].decode() if result.output[1] else ""
        output = stdout + stderr
        return result.exit_code, output.strip()
    except NotFound:
        return -1, f"Container '{container_name}' not found"


def stop_container(client: docker.DockerClient, name: str, timeout: int = 10) -> bool:
    """Stop a container gracefully."""
    try:
        container = client.containers.get(name)
        container.stop(timeout=timeout)
        return True
    except NotFound:
        print(f"Container '{name}' not found")
        return False


def get_container_logs(
    client: docker.DockerClient,
    name: str,
    tail: int = 100,
    since: int = None,
) -> str:
    """Get container logs.

    Args:
        tail: Number of lines from end
        since: Unix timestamp logs since this time
    """
    try:
        container = client.containers.get(name)
        logs = container.logs(tail=tail, since=since, timestamps=True)
        return logs.decode("utf-8")
    except NotFound:
        return f"Container '{name}' not found"


# =============================================================================
# IMAGES build, pull, list
# =============================================================================

def build_image(
    client: docker.DockerClient,
    path: str,
    tag: str,
    dockerfile: str = "Dockerfile",
    build_args: dict = None,
) -> str:
    """Build a Docker image from a Dockerfile.

    Returns the image ID.
    """
    print(f"Building image '{tag}' from {path}...")
    image, build_log = client.images.build(
        path=path,
        tag=tag,
        dockerfile=dockerfile,
        buildargs=build_args or {},
        rm=True,  # Remove intermediate containers
    )

    # Print build output
    for chunk in build_log:
        if "stream" in chunk:
            line = chunk["stream"].strip()
            if line:
                print(f"  {line}")

    print(f"Built: {image.tags}")
    return image.id


def pull_image(client: docker.DockerClient, image: str, tag: str = "latest") -> None:
    """Pull an image from registry."""
    print(f"Pulling {image}:{tag}...")
    client.images.pull(image, tag=tag)
    print(f"Pulled {image}:{tag}")


def list_images(client: docker.DockerClient) -> list[dict]:
    """List local Docker images."""
    images = client.images.list()
    return [
        {
            "id": img.short_id,
            "tags": img.tags,
            "size_mb": round(img.attrs["Size"] / 1024 / 1024, 1),
            "created": img.attrs["Created"][:10],
        }
        for img in images
        if img.tags  # Skip untagged images
    ]


def cleanup_images(client: docker.DockerClient, dangling_only: bool = True) -> int:
    """Remove unused images. Returns number of images removed."""
    removed = client.images.prune(filters={"dangling": dangling_only})
    count = len(removed.get("ImagesDeleted", []) or [])
    space = removed.get("SpaceReclaimed", 0) / 1024 / 1024
    print(f"Removed {count} images, freed {space:.1f} MB")
    return count


# =============================================================================
# NETWORKS AND VOLUMES
# =============================================================================

def create_network(client: docker.DockerClient, name: str) -> str:
    """Create a Docker network for container communication."""
    network = client.networks.create(name, driver="bridge")
    return network.id


def list_volumes(client: docker.DockerClient) -> list[dict]:
    """List Docker volumes."""
    volumes = client.volumes.list()
    return [
        {"name": v.name, "driver": v.attrs["Driver"], "mountpoint": v.attrs["Mountpoint"]}
        for v in volumes
    ]


# =============================================================================
# DOCKER COMPOSE programmatic control
# =============================================================================

def compose_up(compose_file: str = "docker-compose.yml", detach: bool = True) -> str:
    """Run docker compose up (via subprocess SDK doesn't support compose)."""
    import subprocess
    cmd = ["docker", "compose", "-f", compose_file, "up"]
    if detach:
        cmd.append("-d")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr


def compose_down(compose_file: str = "docker-compose.yml", volumes: bool = False) -> str:
    """Run docker compose down."""
    import subprocess
    cmd = ["docker", "compose", "-f", compose_file, "down"]
    if volumes:
        cmd.append("-v")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr


if __name__ == "__main__":
    print("=" * 60)
    print("Docker Utils Demo")
    print("=" * 60)

    try:
        client = get_client()
        print(f"Docker version: {client.version()['Version']}")

        # List containers
        print("\n--- Running Containers ---")
        containers = list_containers(client)
        if containers:
            for c in containers:
                print(f"  {c['name']:20} {c['status']:10} {c['image']}")
        else:
            print("  No running containers")

        # List images
        print("\n--- Local Images ---")
        images = list_images(client)
        for img in images[:10]:
            tags = ", ".join(img["tags"][:2])
            print(f"  {tags:40} {img['size_mb']:>8.1f} MB")

    except DockerException:
        print("\nDocker is not available. Install Docker and start the daemon.")
        print("  sudo apt install docker.io")
        print("  sudo systemctl start docker")
