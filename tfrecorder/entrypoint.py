import argparse
import itertools
import logging
import multiprocessing
import os
import sys

import tqdm

from .config import Config
from .convert import Converter
from .datatype import parse_metadata
from .fileio import get_filenames

# Logging configuration
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.INFO)

# Argparse Configuration
parser = argparse.ArgumentParser(
    description="Automatically convert CSV or TSV files to TFRecord, and upload them to Google Cloud Storage.",
)
parser.add_argument("metadata_path", metavar="METADATA_PATH", type=str, help="Path of JSON file which have metadata")
parser.add_argument(
    "-c",
    "--compression-type",
    dest="compression_type",
    type=str,
    default="GZIP",
    help="TFRecord compression type. Use GZIP by default.",
)
parser.add_argument(
    "--only-convert",
    dest="only_convert",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    help="Only convert the files, not upload to GCS",
)
parser.add_argument(
    "--only-upload",
    dest="only_upload",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    help="Only upload the files to GCS, not convert (will read TFRECORD_PATH only)",
)
parser.add_argument(
    "-g",
    "--google-application-credentials",
    dest="google_application_credentials",
    type=str,
    default="",
    help="Google Application Credential JSON file path. Will use environment variable as a default.",
)
parser.add_argument(
    "--max-pool-size",
    dest="max_pool_size",
    type=int,
    default=multiprocessing.cpu_count(),
    help="Max pool size for multiprocessing. Use all cores by default.",
)
parser.add_argument("--chunksize", type=int, default=10, help="Chunksize for multiprocessing. Use 10 by default.")


def parse_arguments() -> Config:
    """Parse command line arguments."""
    args = parser.parse_args()
    dataset_path, tfrecord_path, columns = parse_metadata(args.metadata_path)
    args.dataset_path = dataset_path
    args.tfrecord_path = tfrecord_path
    args.columns = columns

    # Validation
    if args.only_convert and args.only_upload:
        raise ValueError("You cannot assign both option: --only-convert, --only-upload")
    if not args.only_convert and args.google_application_credentials == "":
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            args.google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            logging.info("Using environment variable for Google application credentials file")
            logging.info(f"Path: {args.google_application_credentials}")
        else:
            raise ValueError(
                "There are no GOOGLE_APPLICATION_CREDENTIALS provided.",
                "Please provide the environment variable or the path directly into this program with `-g`.",
            )
    if args.compression_type not in ("GZIP", "ZLIB", ""):
        logging.error(f"Invalid compression type `{args.compression_type}`")
        logging.error('Compression type should be one of: GZIP, ZLIB, "" (Empty string)')

    return Config(**vars(args))


def main():
    try:
        config: Config = parse_arguments()
    except ValueError as e:
        for msg in e.args:
            logging.error(msg)
        return 1

    config.print()
    confirm = input("[?] Do you want to proceed? (Type 'Y' to start) > ")
    if confirm != "Y":
        logging.info("Abort.")
        return 1

    logging.info(f"Obtaining filenames from dataset path...")
    filenames = get_filenames(config.dataset_path)
    logging.info(f"{len(filenames)} files were found")
    pool_size = min(config.max_pool_size, len(filenames))

    logging.info(f"Start to convert with pool size {pool_size}")
    with multiprocessing.Pool(pool_size) as pool:
        argument_pack = zip(filenames, itertools.repeat(config))
        _ = list(
            tqdm.tqdm(
                pool.imap_unordered(Converter.convert_one_file, argument_pack, chunksize=config.chunksize),
                total=len(filenames),
            )
        )

    logging.info(f"Finished to convert.")


if __name__ == "__main__":
    sys.exit(main())
