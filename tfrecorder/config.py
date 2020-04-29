import enum
import logging
from typing import List, NamedTuple

from .datatype import Column


class ExecutionMode(enum.Enum):
    CONVERT_AND_UPLOAD = 0
    UPLOAD = 1
    CONVERT = 2


class Config(NamedTuple):
    #: Metadata file path
    metadata_path: str

    """Configuration From Argument"""
    #: Do only convert
    only_convert: bool
    #: Do only upload
    only_upload: bool
    #: Delete file after upload, if execution mode is CONVERT_AND_UPLOAD
    delete_after_upload: bool

    #: Batch size for writing and uploading TFRecord file
    batch_size: int
    #: Max pool size for multiprocessing
    max_pool_size: int
    #: Chunksize to distribute for multiprocessing
    chunk_size: int
    #: Convert - Compression type
    compression_type: str
    #: Convert - Max Error to tolerate
    max_error: int
    #: Upload - Project ID on GCP
    gcp_project_id: str
    #: Upload - Location of the bucket
    bucket_location: str

    """Configuration From Metadata"""
    #: Dataset Name
    name: str
    #: Dataset path
    from_path: str
    #: TFRecord path
    to_path: str
    #: File type, 'csv' or 'tsv'
    file_type: str
    #: Skip header
    skip_header: bool
    #: Column information
    columns: List[Column]

    @property
    def exec_mode(self) -> str:
        return ExecutionMode(((2 if self.only_convert else 0) + (1 if self.only_upload else 0)) % 3)

    def print(self):
        exec_mode = ("Convert & Upload", "Upload", "Convert")

        logging.info("Configuration:")
        logging.info(f" * Execution Mode: {exec_mode[self.exec_mode.value]}")
        logging.info(f" * Dataset Path: {self.dataset_path}")
        logging.info(f" * TFRecord Path: {self.tfrecord_path}")
        logging.info(f" * File Mode: {self.mode}")
        logging.info(f" * Compression Type: {self.compression_type}")
        logging.info(f" * Multiprocessing: Max {self.max_pool_size} cores (chunksize {self.chunksize})")
