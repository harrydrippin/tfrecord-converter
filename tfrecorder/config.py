import logging
from typing import List, NamedTuple

from .datatype import Column


class Config(NamedTuple):
    #: Metadata file path
    metadata_path: str
    #: Dataset path
    dataset_path: str
    #: TFRecord path
    tfrecord_path: str
    #: Column information
    columns: List[Column]
    #: Compression type
    compression_type: str
    #: Google application credentials path
    google_application_credentials: str
    #: Only convert
    only_convert: bool
    #: Only upload
    only_upload: bool
    #: Max pool size
    max_pool_size: int
    #: Chunksize
    chunksize: int

    def get_exec_mode(self) -> str:
        modes = ("Convert & Upload", "Upload", "Convert")
        return modes[((2 if self.only_convert else 0) + (1 if self.only_upload else 0)) % 3]

    def print(self):
        logging.info("Configuration:")
        logging.info(f" * Execution Mode: {self.get_exec_mode()}")
        logging.info(f" * Dataset Path: {self.dataset_path}")
        logging.info(f" * TFRecord Path: {self.tfrecord_path}")
        logging.info(f" * Compression Type: {self.compression_type}")
        logging.info(f" * Multiprocessing: Max {self.max_pool_size} cores (chunksize {self.chunksize})")
