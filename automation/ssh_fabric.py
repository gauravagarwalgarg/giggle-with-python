"""
SSH & Remote Execution fabric and paramiko for remote server management.

Fabric is a high-level SSH library for running commands on remote servers.
Paramiko is the lower-level SSH implementation underneath.

Install: pip install fabric paramiko
"""
import os
from pathlib import Path
from typing import Any

# Fabric (high-level, recommended for most use cases)
from fabric import Connection, Config
from invoke import Responder


# =============================================================================
# CONNECTION SETUP
# =============================================================================

def connect(
    host: str,
    user: str = None,
    key_filename: str = None,
    password: str = None,
    port: int = 22,
    gateway: str = None,
) -> Connection:
    """Create an SSH connection.

    Auth priority:
    1. SSH key (key_filename)
    2. SSH agent
    3. Password

    Args:
        host: Hostname or IP
        user: SSH username (defaults to current user)
        key_filename: Path to private key
        password: SSH password (prefer keys!)
        port: SSH port
        gateway: Jump host for bastion/proxy access
    """
    connect_kwargs = {}

    if key_filename:
        connect_kwargs["key_filename"] = key_filename
    if password:
        connect_kwargs["password"] = password

    # Jump host / bastion support
    gateway_conn = None
    if gateway:
        gateway_conn = Connection(gateway, user=user, connect_kwargs=connect_kwargs)

    conn = Connection(
        host=host,
        user=user or os.getenv("USER"),
        port=port,
        connect_kwargs=connect_kwargs,
        gateway=gateway_conn,
    )
    return conn


# =============================================================================
# REMOTE COMMAND EXECUTION
# =============================================================================

def run_command(conn: Connection, command: str, sudo: bool = False, hide: bool = False) -> dict:
    """Run a command on remote server.

    Args:
        conn: Fabric connection
        command: Shell command to run
        sudo: Run as root
        hide: Suppress output

    Returns:
        dict with stdout, stderr, exit_code, ok
    """
    try:
        if sudo:
            result = conn.sudo(command, hide=hide, warn=True)
        else:
            result = conn.run(command, hide=hide, warn=True)

        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.return_code,
            "ok": result.ok,
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "ok": False,
        }


def run_commands(conn: Connection, commands: list[str], stop_on_error: bool = True) -> list[dict]:
    """Run multiple commands sequentially."""
    results = []
    for cmd in commands:
        result = run_command(conn, cmd)
        results.append({"command": cmd, **result})
        if stop_on_error and not result["ok"]:
            break
    return results


# =============================================================================
# FILE TRANSFER
# =============================================================================

def upload_file(conn: Connection, local_path: str, remote_path: str) -> None:
    """Upload a file to remote server."""
    conn.put(local_path, remote=remote_path)
    print(f"Uploaded: {local_path} → {remote_path}")


def download_file(conn: Connection, remote_path: str, local_path: str = None) -> str:
    """Download a file from remote server.

    Returns local path of downloaded file.
    """
    local_path = local_path or Path(remote_path).name
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    conn.get(remote_path, local=local_path)
    print(f"Downloaded: {remote_path} → {local_path}")
    return local_path


def upload_directory(conn: Connection, local_dir: str, remote_dir: str) -> None:
    """Upload an entire directory (tar + transfer + extract)."""
    import tempfile

    local_dir_path = Path(local_dir)
    tar_name = f"{local_dir_path.name}.tar.gz"

    with tempfile.TemporaryDirectory() as tmp:
        tar_path = f"{tmp}/{tar_name}"

        # Create tarball locally
        import tarfile
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(local_dir, arcname=local_dir_path.name)

        # Upload and extract
        conn.put(tar_path, remote=f"/tmp/{tar_name}")
        conn.run(f"mkdir -p {remote_dir}")
        conn.run(f"tar -xzf /tmp/{tar_name} -C {remote_dir}")
        conn.run(f"rm /tmp/{tar_name}")

    print(f"Uploaded directory: {local_dir} → {remote_dir}/{local_dir_path.name}")


# =============================================================================
# SERVER MANAGEMENT RECIPES
# =============================================================================

def check_disk_space(conn: Connection) -> list[dict]:
    """Check disk usage on remote server."""
    result = run_command(conn, "df -h --output=source,size,used,avail,pcent,target", hide=True)
    lines = result["stdout"].split("\n")

    disks = []
    for line in lines[1:]:  # Skip header
        parts = line.split()
        if len(parts) >= 6 and not parts[0].startswith("tmpfs"):
            disks.append({
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "use_percent": parts[4],
                "mount": parts[5],
            })
    return disks


def check_memory(conn: Connection) -> dict:
    """Check memory usage on remote server."""
    result = run_command(conn, "free -m", hide=True)
    lines = result["stdout"].split("\n")

    # Parse "Mem:" line
    mem_parts = lines[1].split()
    return {
        "total_mb": int(mem_parts[1]),
        "used_mb": int(mem_parts[2]),
        "free_mb": int(mem_parts[3]),
        "available_mb": int(mem_parts[6]) if len(mem_parts) > 6 else None,
        "percent_used": round(int(mem_parts[2]) / int(mem_parts[1]) * 100, 1),
    }


def get_running_services(conn: Connection) -> list[dict]:
    """List running systemd services."""
    result = run_command(
        conn,
        "systemctl list-units --type=service --state=running --no-pager --plain",
        hide=True,
    )
    services = []
    for line in result["stdout"].split("\n")[1:]:
        parts = line.split()
        if len(parts) >= 4 and parts[0].endswith(".service"):
            services.append({
                "name": parts[0].replace(".service", ""),
                "state": parts[2],
                "description": " ".join(parts[4:]),
            })
    return services


def deploy_app(
    conn: Connection,
    repo_url: str,
    deploy_dir: str,
    branch: str = "main",
    post_deploy_commands: list[str] = None,
) -> bool:
    """Simple git-based deployment.

    Pulls latest code, installs deps, restarts service.
    """
    commands = [
        f"mkdir -p {deploy_dir}",
        f"cd {deploy_dir} && git pull origin {branch} || git clone -b {branch} {repo_url} .",
        f"cd {deploy_dir} && pip install -r requirements.txt --quiet",
    ]

    if post_deploy_commands:
        commands.extend([f"cd {deploy_dir} && {cmd}" for cmd in post_deploy_commands])

    results = run_commands(conn, commands)

    for r in results:
        status = "✓" if r["ok"] else "✗"
        print(f"  {status} {r['command']}")
        if not r["ok"]:
            print(f"    Error: {r['stderr']}")
            return False

    return True


# =============================================================================
# MULTI-SERVER OPERATIONS
# =============================================================================

def run_on_multiple(hosts: list[str], command: str, user: str = None, **kwargs) -> dict[str, dict]:
    """Run a command on multiple servers."""
    results = {}
    for host in hosts:
        print(f"  → {host}")
        conn = connect(host, user=user, **kwargs)
        results[host] = run_command(conn, command)
        conn.close()
    return results


# =============================================================================
# PARAMIKO (lower-level) for when you need more control
# =============================================================================

def paramiko_example():
    """Lower-level SSH with paramiko for interactive sessions, tunneling, etc."""
    import paramiko

    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown hosts

    try:
        # Connect
        client.connect(
            hostname="example.com",
            port=22,
            username="deploy",
            key_filename=os.path.expanduser("~/.ssh/id_rsa"),
        )

        # Execute command
        stdin, stdout, stderr = client.exec_command("uname -a")
        output = stdout.read().decode().strip()
        print(f"Remote system: {output}")

        # SFTP file operations
        sftp = client.open_sftp()
        sftp.put("local_file.txt", "/remote/path/file.txt")
        sftp.get("/remote/path/file.txt", "downloaded_file.txt")
        sftp.close()

    finally:
        client.close()


if __name__ == "__main__":
    print("=" * 60)
    print("SSH / Fabric Demo")
    print("=" * 60)

    print("\nUsage examples:")
    print("""
    # Connect to a server
    conn = connect("web-server.example.com", user="deploy", key_filename="~/.ssh/id_rsa")

    # Run commands
    result = run_command(conn, "uptime")
    print(result["stdout"])

    # Check server health
    disk = check_disk_space(conn)
    memory = check_memory(conn)
    print(f"Memory: {memory['percent_used']}% used")

    # Deploy
    deploy_app(
        conn,
        repo_url="git@github.com:user/app.git",
        deploy_dir="/opt/myapp",
        post_deploy_commands=["systemctl restart myapp"]
    )

    # Multi-server
    results = run_on_multiple(
        ["web1.example.com", "web2.example.com"],
        "systemctl status nginx",
        user="deploy"
    )

    conn.close()
    """)
