# Automation

Scripts for automating infrastructure and DevOps tasks with Python.

## Files

| File | Purpose | Key Libraries |
|------|---------|---------------|
| `docker_utils.py` | Docker container management | docker-py: build, run, logs, cleanup |
| `aws_boto3.py` | AWS operations | boto3: S3, EC2, Lambda, IAM |
| `ssh_fabric.py` | Remote server management | Fabric: SSH commands, file transfer, sudo |
| `file_renamer.py` | Batch file renaming | pathlib, regex: bulk rename with patterns |

## Path

```
automation/
├── aws_boto3.py
├── docker_utils.py
├── file_renamer.py
├── requirements.txt
└── ssh_fabric.py
```

## Setup

```bash
cd automation
pip install -r requirements.txt  # docker, boto3, fabric
```
