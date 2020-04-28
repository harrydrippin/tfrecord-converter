import glob
import logging
from typing import List

import tensorflow as tf


def get_filenames(glob_string: str) -> List[str]:
    """Load every filenames matches with given glob string."""
    return glob.glob(glob_string, recursive=True)


def read_file(path: str, mode: str, skip_header: bool = False, max_error: int = -1) -> List[List[str]]:
    """
    Read the file by given mode and path.

    :param path: File path.
    :param mode: File parsing mode. e.g. csv, tsv
    :param skip_header: Whether skip the header or not
    :param max_error: Max error count to tolerate
    """
    mode = mode.lower()
    if mode not in ("csv", "tsv"):
        raise ValueError(f"File mode should be 'csv' or 'tsv', not {mode}")
    with open(path, "r") as f:
        raw = f.read().split("\n")
        if skip_header:
            raw = raw[1:]
        if raw[-1] == "":
            raw = raw[:-1]

    delimiter = "," if mode == "csv" else "\t"

    result = []
    error_count = 0
    for line in raw:
        try:
            result.append(line.split(delimiter))
        except Exception as e:
            logging.error(f"Error has occurred while parsing file {path}:")
            logging.error(e)
            error_count += 1
            if max_error != -1 and error_count >= max_error:
                raise ValueError("Max error count reached, Stop to parse")
    return result


def save_tfrecord_file(examples: List[tf.train.Example], filename: str, compression_type: str = "GZIP"):
    """Save given examples to TFRecord file."""
    if compression_type not in ("GZIP", "ZLIB", ""):
        raise ValueError(f"Invalid compression type `{compression_type}` is present.")
    options = tf.io.TFRecordOptions(compression_type=compression_type)
    with tf.io.TFRecordWriter(filename, options) as writer:
        for example in examples:
            writer.write(example.SerializeToString())
