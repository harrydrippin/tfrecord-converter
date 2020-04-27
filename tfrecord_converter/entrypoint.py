import argparse
import sys
import logging
import os

from .config import Config

# Logging configuration
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.INFO)

# Argparse Configuration
parser = argparse.ArgumentParser(
    description="Automatically convert CSV or TSV files to TFRecord, and upload them to Google Cloud Storage.",
)
parser.add_argument("dataset_path", metavar="DATASET_PATH", type=str, help="File path described with glob pattern")
parser.add_argument("tfrecord_path", metavar="TFRECORD_PATH", type=str, help="File path to store TFRecord files")
parser.add_argument(
    "-c",
    "--compression-type",
    dest="compression_type",
    type=str,
    default="GZIP",
    help="TFRecord compression type. default: GZIP",
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


def parse_arguments() -> Config:
    """Parse command line arguments."""
    args = parser.parse_args()

    # Validation
    if args.only_convert and args.only_upload:
        raise Exception("You cannot assign both option: --only-convert, --only-upload")
    if not args.only_convert and args.google_application_credentials == "":
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            args.google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            logging.info("Using environment variable for Google application credentials file")
            logging.info(f"Path: {args.google_application_credentials}")
        else:
            raise Exception(
                "There are no GOOGLE_APPLICATION_CREDENTIALS provided.",
                "Please provide the environment variable or the path directly into this program with `-g`.",
            )
    if args.compression_type not in ("GZIP", "ZLIB", ""):
        logging.error(f"Invalid compression type `{args.compression_type}`")
        logging.error('Compression type should be one of: GZIP, ZLIB, "" (Empty string)')

    return Config(**vars(args))


def main():
    logging.info("Initializing")
    try:
        config: Config = parse_arguments()
    except Exception as e:
        for msg in e.args:
            logging.error(msg)
        return 1

    config.print()
    confirm = input("[?] Do you want to proceed? (Type 'Y' to start) > ")
    if confirm != "Y":
        logging.info("Abort.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
