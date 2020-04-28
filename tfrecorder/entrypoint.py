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
from .fileio import get_filenames, save_tfrecord_file
from .utils import batch

# Logging configuration
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.INFO)
# Disable logs from TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Argparse Configuration
parser = argparse.ArgumentParser(
    description="Automatically convert CSV or TSV files to TFRecord, and upload them to Google Cloud Storage.",
)
parser.add_argument("metadata_path", metavar="METADATA_PATH", type=str, help="Path of JSON file which have metadata")
parser.add_argument("-m", "--mode", type=str, default="tsv", help="Method to parse the file. Use tsv by default.")
parser.add_argument(
    "--max-error", type=int, default=-1, help="Max error records while parsing. Not set (-1) by default."
)
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
    "--batch-size",
    dest="batch_size",
    type=int,
    default=1000,
    help="Size of the examples one file should have. Use 1000 by default.",
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
    args = vars(parser.parse_args())
    metadata = parse_metadata(args["metadata_path"])
    for key in ("dataset_path", "tfrecord_path", "skip_header", "columns"):
        args[key] = metadata[key]

    # Validation
    if args["tfrecord_path"][-1] != "/":
        raise ValueError("Given tfrecord_path is not a directory.", "Did you put '/' at the end of the path?")
    if args["mode"] not in ("csv", "tsv"):
        raise ValueError("`-m` / `--mode` option can only have 'csv' or 'tsv'.")
    if args["only_convert"] and args["only_upload"]:
        raise ValueError("You cannot assign both option: --only-convert, --only-upload")
    if not args["only_convert"] and args["google_application_credentials"] == "":
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            args["google_application_credentials"] = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            logging.info("Using environment variable for Google application credentials file")
            logging.info(f"Path: {args['google_application_credentials']}")
        else:
            raise ValueError(
                "There are no GOOGLE_APPLICATION_CREDENTIALS provided.",
                "Please provide the environment variable or the path directly into this program with `-g`.",
            )
    if args["compression_type"] not in ("GZIP", "ZLIB", ""):
        raise ValueError(
            f"Invalid compression type `{args['compression_type']}`",
            'Compression type should be one of: GZIP, ZLIB, "" (Empty string)',
        )

    return Config(**args)


def convert(config: Config):
    logging.info(f"Obtaining filenames from dataset path...")
    filenames = get_filenames(config.dataset_path)
    logging.info(f"{len(filenames)} files were found")
    pool_size = min(config.max_pool_size, len(filenames))

    logging.info(f"Start to convert with pool size {pool_size}")
    with multiprocessing.Pool(pool_size) as pool:
        argument_pack = zip(filenames, itertools.repeat(config))
        results = list(
            tqdm.tqdm(
                pool.imap_unordered(Converter.convert_one_file, argument_pack, chunksize=config.chunksize),
                total=len(filenames),
            )
        )
    examples = [example for result in results for example in result[0]]
    logging.info(f"All {sum([item[1] for item in results])} records are converted")
    logging.info(f"Finished to convert. Saving files...")

    tfrecord_path = os.path.dirname(config.tfrecord_path)
    os.makedirs(tfrecord_path, exist_ok=True)
    for idx, example_batch in enumerate(batch(examples, config.batch_size)):
        filename = tfrecord_path + f"/result.{idx:04d}.tfrecord"
        save_tfrecord_file(example_batch, filename, compression_type=config.compression_type)

    logging.info(f"Finished to save.")


def upload(config: Config):
    pass


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

    exec_mode = config.get_exec_mode()

    # Need to convert (0 or 2)
    if exec_mode % 2 == 0:
        convert(config)
    # Need to Upload (0 or 1)
    if exec_mode < 2:
        upload(config)


if __name__ == "__main__":
    sys.exit(main())
