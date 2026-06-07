"""
CLI with argparse argument parsing patterns, subcommands, config from env.

argparse is stdlib and handles 90% of CLI needs. For fancier CLIs,
consider click or typer (both built on top of this).
"""
import argparse
import os
import sys
from pathlib import Path


# =============================================================================
# BASIC CLI simple command with arguments
# =============================================================================

def build_basic_parser() -> argparse.ArgumentParser:
    """Basic argument parser with common patterns."""
    parser = argparse.ArgumentParser(
        description="Process data files",
        # Show defaults in help text
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Positional argument (required)
    parser.add_argument("input_file", help="Path to input file")

    # Optional argument with short and long form
    parser.add_argument(
        "-o", "--output",
        default="output.json",
        help="Output file path"
    )

    # Flag (boolean True if present)
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Integer argument with validation
    parser.add_argument(
        "-n", "--num-workers",
        type=int,
        default=4,
        choices=range(1, 17),
        metavar="N",
        help="Number of workers (1-16)"
    )

    # Choice from a list
    parser.add_argument(
        "--format",
        choices=["json", "csv", "yaml"],
        default="json",
        help="Output format"
    )

    # Multiple values
    parser.add_argument(
        "--tags",
        nargs="+",  # One or more values
        default=[],
        help="Tags to apply"
    )

    # Environment variable fallback
    parser.add_argument(
        "--api-key",
        default=os.getenv("API_KEY", ""),
        help="API key (or set API_KEY env var)"
    )

    return parser


# =============================================================================
# SUBCOMMANDS git-style CLI (e.g., `app user create`, `app user list`)
# =============================================================================

def build_subcommand_parser() -> argparse.ArgumentParser:
    """Parser with subcommands like git, docker, kubectl."""
    parser = argparse.ArgumentParser(
        prog="myapp",
        description="My application CLI"
    )

    # Global arguments (apply to all subcommands)
    parser.add_argument(
        "--config",
        default=os.getenv("APP_CONFIG", "config.yaml"),
        help="Config file path"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- user subcommand ---
    user_parser = subparsers.add_parser("user", help="User management")
    user_subparsers = user_parser.add_subparsers(dest="action")

    # user create
    user_create = user_subparsers.add_parser("create", help="Create a user")
    user_create.add_argument("--name", required=True)
    user_create.add_argument("--email", required=True)
    user_create.add_argument("--role", default="user", choices=["user", "admin"])

    # user list
    user_list = user_subparsers.add_parser("list", help="List users")
    user_list.add_argument("--role", help="Filter by role")
    user_list.add_argument("--limit", type=int, default=50)

    # user delete
    user_delete = user_subparsers.add_parser("delete", help="Delete a user")
    user_delete.add_argument("user_id", type=int)
    user_delete.add_argument("--force", action="store_true")

    # --- deploy subcommand ---
    deploy_parser = subparsers.add_parser("deploy", help="Deploy application")
    deploy_parser.add_argument("environment", choices=["dev", "staging", "prod"])
    deploy_parser.add_argument("--version", required=True)
    deploy_parser.add_argument("--dry-run", action="store_true")

    # --- db subcommand ---
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_subparsers = db_parser.add_subparsers(dest="action")

    db_migrate = db_subparsers.add_parser("migrate", help="Run migrations")
    db_migrate.add_argument("--target", help="Target migration version")

    db_seed = db_subparsers.add_parser("seed", help="Seed database")
    db_seed.add_argument("--file", default="seeds.json")

    return parser


# =============================================================================
# HANDLER FUNCTIONS what each command actually does
# =============================================================================

def handle_user_create(args: argparse.Namespace):
    """Handle: myapp user create --name Alice --email alice@example.com"""
    print(f"Creating user: name={args.name}, email={args.email}, role={args.role}")


def handle_user_list(args: argparse.Namespace):
    """Handle: myapp user list --role admin --limit 10"""
    print(f"Listing users: role={args.role}, limit={args.limit}")


def handle_user_delete(args: argparse.Namespace):
    """Handle: myapp user delete 42 --force"""
    if not args.force:
        confirm = input(f"Delete user {args.user_id}? [y/N] ")
        if confirm.lower() != "y":
            print("Cancelled")
            return
    print(f"Deleted user {args.user_id}")


def handle_deploy(args: argparse.Namespace):
    """Handle: myapp deploy staging --version 1.2.3 --dry-run"""
    action = "Would deploy" if args.dry_run else "Deploying"
    print(f"{action} version {args.version} to {args.environment}")


# =============================================================================
# CONFIG FROM ENVIRONMENT the 12-factor app way
# =============================================================================

def get_config_from_env() -> dict:
    """Load configuration from environment variables with defaults.

    The 12-factor app methodology recommends env vars for config.
    This pattern makes it easy to run locally and in containers.
    """
    return {
        "db_host": os.getenv("DB_HOST", "localhost"),
        "db_port": int(os.getenv("DB_PORT", "5432")),
        "db_name": os.getenv("DB_NAME", "myapp"),
        "db_user": os.getenv("DB_USER", "postgres"),
        "db_password": os.getenv("DB_PASSWORD", ""),  # No default for secrets
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "debug": os.getenv("DEBUG", "false").lower() in ("true", "1", "yes"),
        "port": int(os.getenv("PORT", "8000")),
        "workers": int(os.getenv("WORKERS", "4")),
        "allowed_hosts": os.getenv("ALLOWED_HOSTS", "localhost").split(","),
    }


# =============================================================================
# CUSTOM ARGUMENT TYPES validation during parsing
# =============================================================================

def existing_file(path: str) -> Path:
    """Argparse type that validates file exists."""
    p = Path(path)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"File not found: {path}")
    return p


def existing_dir(path: str) -> Path:
    """Argparse type that validates directory exists."""
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"Directory not found: {path}")
    return p


def port_number(value: str) -> int:
    """Argparse type for valid port numbers."""
    port = int(value)
    if not (1 <= port <= 65535):
        raise argparse.ArgumentTypeError(f"Invalid port: {port} (must be 1-65535)")
    return port


def positive_int(value: str) -> int:
    """Argparse type for positive integers."""
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError(f"Must be positive, got: {n}")
    return n


if __name__ == "__main__":
    print("=" * 60)
    print("CLI Demo")
    print("=" * 60)

    # Demo the subcommand parser
    parser = build_subcommand_parser()

    # Simulate different command invocations
    demo_commands = [
        ["user", "create", "--name", "Alice", "--email", "alice@example.com"],
        ["user", "list", "--role", "admin", "--limit", "10"],
        ["deploy", "staging", "--version", "1.2.3", "--dry-run"],
    ]

    for cmd_args in demo_commands:
        print(f"\n  $ myapp {' '.join(cmd_args)}")
        args = parser.parse_args(cmd_args)

        if args.command == "user":
            if args.action == "create":
                handle_user_create(args)
            elif args.action == "list":
                handle_user_list(args)
        elif args.command == "deploy":
            handle_deploy(args)

    # Show config from env
    print("\n--- Config from Environment ---")
    config = get_config_from_env()
    for key, value in config.items():
        print(f"  {key}: {value}")
