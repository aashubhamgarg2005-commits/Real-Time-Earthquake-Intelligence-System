from minio import Minio
from minio.error import S3Error
from src.config.config import (
    minio_endpoint,
    minio_access_key,
    minio_secret_key,
    minio_bucket,
    minio_secure
)

class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=minio_secure
        )

    def bucket_exists(self):
        return self.client.bucket_exists(
            bucket_name=minio_bucket
        )

    def create_bucket(self):
        try:
            if not self.bucket_exists():
                self.client.make_bucket(
                    bucket_name=minio_bucket
                )
                print(f"Bucket created successfully: {minio_bucket}")

            else:
                print(
                    f"Bucket already exists:"
                    f"{minio_bucket}"
                )
        except S3Error as e:
            print(f"Minio error: {e}")

