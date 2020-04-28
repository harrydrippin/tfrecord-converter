import pytest

from tfrecorder.datatype import Column, FeatureType


@pytest.fixture(scope="session")
def config():
    return {
        "metadata_path": "./tests/data.tfrecord",
        "dataset_path": "./tests/data/sample_metadata.json",
        "tfrecord_path": "./tests/data/*.tsv",
        "mode": "tsv",
        "skip_header": False,
        "max_error": -1,
        "columns": [
            Column("first", FeatureType.STRING),
            Column("second", FeatureType.FLOAT),
            Column("third", FeatureType.INT),
            Column("fourth", FeatureType.BOOL),
        ],
        "compression_type": "GZIP",
        "google_application_credentials": "GOOGLE",
        "only_convert": False,
        "only_upload": False,
        "batch_size": 1000,
        "max_pool_size": 8,
        "chunksize": 10,
    }
