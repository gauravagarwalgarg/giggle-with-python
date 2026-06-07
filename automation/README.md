# Automation DevOps & Scripting Helpers

Python scripts for infrastructure automation, CI/CD, and server management.

## Files

| File | What it does |
|------|-------------|
| `docker_utils.py` | Docker SDK containers, images, builds, compose |
| `aws_boto3.py` | AWS S3, EC2, Lambda, SSM, SQS |
| `ssh_fabric.py` | Remote execution SSH, file transfer, deployment |

## Setup

```bash
pip install -r requirements.txt
```

## Prerequisites

- **Docker**: Docker daemon running (`systemctl start docker`)
- **AWS**: Configured credentials (`aws configure` or env vars)
- **SSH**: SSH key pair and access to target servers

## Quick Examples

### Docker
```python
from automation.docker_utils import get_client, list_containers, run_container

client = get_client()
containers = list_containers(client)
```

### AWS S3
```python
from automation.aws_boto3 import s3_upload_file, s3_list_objects

s3_upload_file("report.pdf", "my-bucket", "reports/2024/report.pdf")
objects = s3_list_objects("my-bucket", prefix="reports/")
```

### SSH
```python
from automation.ssh_fabric import connect, run_command, check_disk_space

conn = connect("server.example.com", user="deploy")
result = run_command(conn, "uptime")
disk = check_disk_space(conn)
conn.close()
```
