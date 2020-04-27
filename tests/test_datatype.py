import pytest

from tfrecorder.datatype import Metadata, FeatureType, parse_metadata


def test_parse_metadata():
    expected = [
        Metadata("first", FeatureType.STRING),
        Metadata("second", FeatureType.FLOAT),
        Metadata("third", FeatureType.INT),
        Metadata("fourth", FeatureType.BOOL),
    ]
    assert expected == parse_metadata("./tests/data/sample_metadata.json")
