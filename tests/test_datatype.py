from tfrecorder.datatype import Column, FeatureType, parse_metadata


def test_parse_metadata():
    expected = {
        "name": "sample_dataset",
        "from_path": "./tests/data/sample_tsv.tsv",
        "to_path": "./tests/data.tfrecords/",
        "file_type": "tsv",
        "skip_header": False,
        "columns": [
            Column("message_type", FeatureType.STRING),
            Column("timestamp", FeatureType.STRING),
            Column("concat_count", FeatureType.INT),
            Column("utterance", FeatureType.STRING),
        ],
    }
    assert expected == parse_metadata("./tests/data/sample_metadata.json")
