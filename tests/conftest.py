import pytest

from tfrecorder.datatype import Column, FeatureType


@pytest.fixture(scope="session")
def config():
    return {
        "metadata_path": "./tests/data.tfrecord",
        # Argument Configuration
        "only_convert": False,
        "only_upload": False,
        "delete_after_upload": True,
        "batch_size": 1000,
        "max_pool_size": 8,
        "chunk_size": 10,
        "compression_type": "GZIP",
        "max_error": -1,
        "gcp_project_id": "PROJECT_ID",
        "bucket_location": "us-central1",
        # Metadata Configuration
        "name": "sample_dataset",
        "from_path": "./tests/data/sample_metadata.json",
        "to_path": "./tests/data/*.tsv",
        "file_type": "tsv",
        "skip_header": False,
        "columns": [
            Column("first", FeatureType.STRING),
            Column("second", FeatureType.FLOAT),
            Column("third", FeatureType.INT),
            Column("fourth", FeatureType.BOOL),
        ],
    }
