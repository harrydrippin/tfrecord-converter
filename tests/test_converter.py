import pytest
import tensorflow as tf

from tfrecorder.config import Config
from tfrecorder.convert import Converter
from tfrecorder.datatype import Column, FeatureType


@pytest.fixture(scope="session")
def features():
    return [
        tf.train.Feature(bytes_list=tf.train.BytesList(value=["String".encode()])),
        tf.train.Feature(float_list=tf.train.FloatList(value=[4.5])),
        tf.train.Feature(int64_list=tf.train.Int64List(value=[1])),
        tf.train.Feature(int64_list=tf.train.Int64List(value=[True])),
    ]


@pytest.mark.parametrize(
    "tensor, feature_type, expected_index",
    [
        pytest.param("String", FeatureType.STRING, 0),
        pytest.param(4.5, FeatureType.FLOAT, 1),
        pytest.param(1, FeatureType.INT, 2),
        pytest.param(True, FeatureType.BOOL, 3),
    ],
    ids=["String", "Float", "Int", "Bool"],
)
def test_featurize(features, tensor, feature_type, expected_index):
    assert features[expected_index] == Converter.featurize(tensor, feature_type)


@pytest.mark.parametrize(
    "data_list, columns",
    [
        pytest.param(
            ["String", 4.5, 1, True],
            Config(
                "",
                "",
                "",
                [
                    Column("first", FeatureType.STRING),
                    Column("second", FeatureType.FLOAT),
                    Column("third", FeatureType.INT),
                    Column("fourth", FeatureType.BOOL),
                ],
                "",
                "GZIP",
                False,
                False,
                8,
                10,
            ),
        )
    ],
    ids=["Base"],
)
def test_build_example(data_list, columns, features):
    example = tf.train.Example(
        features=tf.train.Features(
            feature={"first": features[0], "second": features[1], "third": features[2], "fourth": features[3]}
        )
    )
    assert example == Converter.build_example(data_list, columns)
