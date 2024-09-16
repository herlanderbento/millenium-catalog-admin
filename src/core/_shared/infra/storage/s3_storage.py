import boto3
from pathlib import Path
import mimetypes
from django.conf import settings
from src.core._shared.application.storage_interface import IStorage


class S3Storage(IStorage):
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            region_name="auto",
        )
        self.bucket_name = settings.R2_BUCKET_NAME

    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        if not content_type:
            content_type, _ = mimetypes.guess_type(str(file_path))

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=str(file_path),
            Body=content,
            ContentType=content_type or "application/octet-stream",
        )

        return f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com/{self.bucket_name}/{file_path}"

    def get(self, file_path: Path) -> bytes:
        response = self.s3_client.get_object(
            Bucket=self.bucket_name, Key=str(file_path)
        )
        return response["Body"].read()
