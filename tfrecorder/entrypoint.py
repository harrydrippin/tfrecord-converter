import argparse
import asyncio
import logging
import multiprocessing
import os

from .config import Config
from .datatype import parse_metadata
from .worker import Worker

# Logging configuration
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.INFO)
# Disable logs from TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

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
    "--max-error", type=int, default=-1, help="Max error records while parsing. Not set (-1) by default."
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
    "--batch-size",
    dest="batch_size",
    type=int,
    default=1000,
    help="Size of the examples one file should have. Use 1000 by default.",
)
parser.add_argument(
    "--max-pool-size",
    dest="max_pool_size",
    type=int,
    default=multiprocessing.cpu_count(),
    help="Max pool size for multiprocessing. Use all cores by default.",
)
parser.add_argument(
    "--chunk-size", dest="chunk_size", type=int, default=10, help="Chunksize for multiprocessing. Use 10 by default."
)
parser.add_argument(
    "--gcp-project-id",
    dest="gcp_project_id",
    type=str,
    default=None,
    help=(
        "ID of the project you have on GCP. "
        + "Use None by default, which will be treated as default project ID that your credential has."
    ),
)
parser.add_argument(
    "--bucket-location",
    dest="bucket_location",
    type=str,
    default=None,
    help="Location of the bucket when upload. Use None by default, which will be treated as US-CENTRAL1 by Google.",
)


def parse_arguments() -> Config:
    """Parse command line arguments."""
    # Merge two configuration source
    args = vars(parser.parse_args())
    metadata = parse_metadata(args["metadata_path"])
    args.update(metadata)

    # Validation
    if args["from_path"][-1] != "/":
        raise ValueError("Given from_path is not a directory.", "Did you put '/' at the end of the path?")
    if args["file_type"] not in ("csv", "tsv"):
        raise ValueError("`file_type` can only have 'csv' or 'tsv'.")
    if args["only_convert"] and args["only_upload"]:
        raise ValueError("You cannot assign both option: --only-convert, --only-upload")
    if not args["only_convert"]:
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            raise ValueError(
                "You should provide the environment variable GOOGLE_APPLICATION_CREDENTIALS.",
                "See https://cloud.google.com/docs/authentication/getting-started for detail.",
            )
    if args["compression_type"] not in ("GZIP", "ZLIB", ""):
        raise ValueError(
            f"Invalid compression type `{args['compression_type']}`",
            'Compression type should be one of: GZIP, ZLIB, "" (Empty string)',
        )

    return Config(**args)


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

    worker = Worker(config)
    asyncio.run(worker)
