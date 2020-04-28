from tfrecorder.datatype import Column, FeatureType, parse_metadata


def test_parse_metadata():
    expected = {
        "dataset_path": "./tests/data/sample_tsv.tsv",
        "tfrecord_path": "./tests/data.tfrecords/",
        "skip_header": False,
        "columns": [
            Column("message_type", FeatureType.STRING),
            Column("timestamp", FeatureType.STRING),
            Column("concat_count", FeatureType.INT),
            Column("utterance", FeatureType.STRING),
        ],
    }
    assert expected == parse_metadata("./tests/data/sample_metadata.json")
