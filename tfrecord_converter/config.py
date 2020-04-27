from typing import NamedTuple
import enum
import logging


class Config(NamedTuple):
    #: Origin dataset path
    dataset_path: str
    #: Destination TFRecord path
    tfrecord_path: str
    #: Compression type
    compression_type: str
    #: Google application credentials path
    google_application_credentials: str
    #: Only convert
    only_convert: bool
    #: Only upload
    only_upload: bool

    def get_exec_mode(self) -> str:
        modes = ("Convert & Upload", "Upload", "Convert")
        return modes[((2 if self.only_convert else 0) + (1 if self.only_upload else 0)) % 3]

    def print(self):
        logging.info("Configuration:")
        logging.info(f" * Execution Mode: {self.get_exec_mode()}")
        logging.info(f" * Dataset Path: {self.dataset_path}")
        logging.info(f" * TFRecord Path: {self.tfrecord_path}")
        logging.info(f" * Compression Type: {self.compression_type}")
        logging.info(f" * Google Application Credentials: {self.google_application_credentials}")
