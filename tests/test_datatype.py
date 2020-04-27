import pytest

from tfrecorder.datatype import Column, FeatureType, parse_metadata


def test_parse_metadata():
    expected = (
        "./tests/data/sample_tsv.tsv",
        "./tests/data.tfrecords",
        [
            Column("first", FeatureType.STRING),
            Column("second", FeatureType.FLOAT),
            Column("third", FeatureType.INT),
            Column("fourth", FeatureType.BOOL),
        ],
    )
    assert expected == parse_metadata("./tests/data/sample_metadata.json")
