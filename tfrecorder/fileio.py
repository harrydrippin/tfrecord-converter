import glob
from typing import List

import tensorflow as tf


def get_filenames(glob_string: str) -> List[str]:
    """Load every filenames matches with given glob string."""
    return glob.glob(glob_string, recursive=True)


def read_file(path: str, mode: str, skip_header: bool = False) -> List[List[str]]:
    """
    Read the file by given mode and path.

    :param path: File path.
    :param mode: File parsing mode. e.g. csv, tsv
    :param skip_header: Whether skip the header or not
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
    return [line.split(delimiter) for line in raw]


def save_tfrecord_file(examples: List[tf.train.Example], filename: str, compression_type: str = "GZIP"):
    """Save given examples to TFRecord file."""
    if compression_type not in ("GZIP", "ZLIB", ""):
        raise ValueError(f"Invalid compression type `{compression_type}` is present.")

    options = tf.io.TFRecordOptions(compression_type=compression_type)
    with tf.io.TFRecordWriter(filename, options) as writer:
        for example in examples:
            writer.write(example)
