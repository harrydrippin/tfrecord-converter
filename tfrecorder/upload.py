import logging
import os
from typing import Awaitable, Optional

from google.cloud import storage
from google.cloud.exceptions import NotFound

from .config import Config


class Uploader:
    def __init__(self, config: Config, bucket_name: Optional[str] = None):
        self.config: Config = config
        self.bucket_name: str = bucket_name if bucket_name is not None else config.name + ".tfrecord"

        self._client = storage.Client(project=config.gcp_project_id)
        self._bucket = self._get_bucket()

    def _get_bucket(self) -> storage.Bucket:
        """Try to get bucket, and make one if not exist"""
        try:
            return self._client.get_bucket(self.bucket_name)
        except NotFound:
            logging.info(f"Bucket {self.bucket_name} not found, make one")
            return self._client.create_bucket(self.bucket_name)

    async def upload_file(self, file_path: str, delete_after_success: bool = False) -> Awaitable[int]:
        """Upload single file to the Google Cloud Storage."""
        try:
            blob = self._bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            return 1
        except Exception as e:
            logging.error("Failed while uploading file")
            logging.error(e)
            return 0
