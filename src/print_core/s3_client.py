import boto3
from mypy_boto3_s3.client import S3Client
from typing_extensions import cast

from print_core.config import get_settings

settings = get_settings()
session = boto3.Session(
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
)
s3_client = cast(
    S3Client,
    session.client(
        service_name="s3",
        endpoint_url=settings.s3_endpoint_url,
    ),
)
