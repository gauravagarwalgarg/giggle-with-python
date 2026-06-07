"""
AWS Boto3 S3 upload/download, EC2 list, Lambda invoke.

Boto3 is the AWS SDK for Python. This file covers the most common
operations you'll need for automation and DevOps scripts.

Install: pip install boto3
Configure: aws configure (or set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
"""
import json
import os
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


# =============================================================================
# CLIENT SETUP
# =============================================================================

def get_session(profile: str = None, region: str = None) -> boto3.Session:
    """Create a boto3 session with optional profile and region.

    Auth resolution order:
    1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    2. AWS credentials file (~/.aws/credentials)
    3. IAM role (if running on EC2/Lambda/ECS)
    """
    return boto3.Session(
        profile_name=profile or os.getenv("AWS_PROFILE"),
        region_name=region or os.getenv("AWS_REGION", "ap-south-1"),
    )


# =============================================================================
# S3 Object Storage
# =============================================================================

def s3_upload_file(
    filepath: str,
    bucket: str,
    key: str = None,
    content_type: str = None,
    session: boto3.Session = None,
) -> str:
    """Upload a file to S3.

    Args:
        filepath: Local file path
        bucket: S3 bucket name
        key: S3 object key (defaults to filename)
        content_type: MIME type (auto-detected if not set)

    Returns:
        S3 URI (s3://bucket/key)
    """
    s3 = (session or boto3).client("s3")
    key = key or Path(filepath).name

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    s3.upload_file(filepath, bucket, key, ExtraArgs=extra_args or None)
    return f"s3://{bucket}/{key}"


def s3_download_file(
    bucket: str,
    key: str,
    filepath: str = None,
    session: boto3.Session = None,
) -> str:
    """Download a file from S3.

    Returns local filepath.
    """
    s3 = (session or boto3).client("s3")
    filepath = filepath or key.split("/")[-1]

    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, key, filepath)
    return filepath


def s3_list_objects(
    bucket: str,
    prefix: str = "",
    max_keys: int = 1000,
    session: boto3.Session = None,
) -> list[dict]:
    """List objects in S3 bucket with optional prefix filter."""
    s3 = (session or boto3).client("s3")
    objects = []

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, PaginationConfig={"MaxItems": max_keys}):
        for obj in page.get("Contents", []):
            objects.append({
                "key": obj["Key"],
                "size_mb": round(obj["Size"] / 1024 / 1024, 2),
                "modified": obj["LastModified"].isoformat(),
            })

    return objects


def s3_generate_presigned_url(
    bucket: str,
    key: str,
    expiration: int = 3600,
    session: boto3.Session = None,
) -> str:
    """Generate a presigned URL for temporary access (default: 1 hour)."""
    s3 = (session or boto3).client("s3")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration,
    )
    return url


def s3_delete_objects(
    bucket: str,
    keys: list[str],
    session: boto3.Session = None,
) -> int:
    """Delete multiple objects from S3. Returns count of deleted objects."""
    s3 = (session or boto3).client("s3")
    response = s3.delete_objects(
        Bucket=bucket,
        Delete={"Objects": [{"Key": k} for k in keys]},
    )
    return len(response.get("Deleted", []))


# =============================================================================
# EC2 Virtual Machines
# =============================================================================

def ec2_list_instances(
    state: str = None,
    tag_filters: dict = None,
    session: boto3.Session = None,
) -> list[dict]:
    """List EC2 instances with optional filtering.

    Args:
        state: Filter by state (running, stopped, terminated)
        tag_filters: Filter by tags {"Name": "web-server"}
    """
    ec2 = (session or boto3).client("ec2")

    filters = []
    if state:
        filters.append({"Name": "instance-state-name", "Values": [state]})
    if tag_filters:
        for key, value in tag_filters.items():
            filters.append({"Name": f"tag:{key}", "Values": [value]})

    response = ec2.describe_instances(Filters=filters or None)

    instances = []
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            name = ""
            for tag in inst.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]

            instances.append({
                "id": inst["InstanceId"],
                "name": name,
                "type": inst["InstanceType"],
                "state": inst["State"]["Name"],
                "private_ip": inst.get("PrivateIpAddress"),
                "public_ip": inst.get("PublicIpAddress"),
                "launch_time": inst["LaunchTime"].isoformat(),
            })

    return instances


def ec2_start_instances(instance_ids: list[str], session: boto3.Session = None) -> dict:
    """Start one or more EC2 instances."""
    ec2 = (session or boto3).client("ec2")
    return ec2.start_instances(InstanceIds=instance_ids)


def ec2_stop_instances(instance_ids: list[str], session: boto3.Session = None) -> dict:
    """Stop one or more EC2 instances."""
    ec2 = (session or boto3).client("ec2")
    return ec2.stop_instances(InstanceIds=instance_ids)


# =============================================================================
# LAMBDA Serverless Functions
# =============================================================================

def lambda_invoke(
    function_name: str,
    payload: dict = None,
    invocation_type: str = "RequestResponse",
    session: boto3.Session = None,
) -> dict:
    """Invoke a Lambda function.

    Args:
        function_name: Lambda function name or ARN
        payload: JSON payload to send
        invocation_type: "RequestResponse" (sync) or "Event" (async)
    """
    client = (session or boto3).client("lambda")

    kwargs = {
        "FunctionName": function_name,
        "InvocationType": invocation_type,
    }
    if payload:
        kwargs["Payload"] = json.dumps(payload)

    response = client.invoke(**kwargs)

    result = {
        "status_code": response["StatusCode"],
        "function_error": response.get("FunctionError"),
    }

    if invocation_type == "RequestResponse" and "Payload" in response:
        result["payload"] = json.loads(response["Payload"].read())

    return result


def lambda_list_functions(session: boto3.Session = None) -> list[dict]:
    """List Lambda functions."""
    client = (session or boto3).client("lambda")
    response = client.list_functions()

    return [
        {
            "name": fn["FunctionName"],
            "runtime": fn.get("Runtime", "N/A"),
            "memory_mb": fn["MemorySize"],
            "timeout_s": fn["Timeout"],
            "last_modified": fn["LastModified"],
        }
        for fn in response["Functions"]
    ]


# =============================================================================
# SSM Parameter Store (secrets/config)
# =============================================================================

def ssm_get_parameter(name: str, decrypt: bool = True, session: boto3.Session = None) -> str:
    """Get a parameter from AWS Systems Manager Parameter Store."""
    ssm = (session or boto3).client("ssm")
    response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    return response["Parameter"]["Value"]


def ssm_put_parameter(
    name: str,
    value: str,
    param_type: str = "SecureString",
    session: boto3.Session = None,
) -> None:
    """Store a parameter in SSM Parameter Store."""
    ssm = (session or boto3).client("ssm")
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type=param_type,
        Overwrite=True,
    )


# =============================================================================
# SQS Message Queue
# =============================================================================

def sqs_send_message(queue_url: str, message: dict, session: boto3.Session = None) -> str:
    """Send a message to SQS queue. Returns message ID."""
    sqs = (session or boto3).client("sqs")
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
    )
    return response["MessageId"]


def sqs_receive_messages(
    queue_url: str,
    max_messages: int = 10,
    wait_seconds: int = 5,
    session: boto3.Session = None,
) -> list[dict]:
    """Receive messages from SQS queue (long polling)."""
    sqs = (session or boto3).client("sqs")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_seconds,
    )
    return [
        {
            "id": msg["MessageId"],
            "body": json.loads(msg["Body"]),
            "receipt_handle": msg["ReceiptHandle"],
        }
        for msg in response.get("Messages", [])
    ]


if __name__ == "__main__":
    print("=" * 60)
    print("AWS Boto3 Demo")
    print("=" * 60)

    try:
        session = get_session()
        sts = session.client("sts")
        identity = sts.get_caller_identity()
        print(f"\nAuthenticated as: {identity['Arn']}")
        print(f"Account: {identity['Account']}")
        print(f"Region: {session.region_name}")

        # List S3 buckets
        s3 = session.client("s3")
        buckets = s3.list_buckets()["Buckets"]
        print(f"\nS3 Buckets ({len(buckets)}):")
        for b in buckets[:5]:
            print(f"  {b['Name']}")

    except NoCredentialsError:
        print("\nNo AWS credentials found. Configure with:")
        print("  aws configure")
        print("  # or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
    except ClientError as e:
        print(f"\nAWS Error: {e}")
