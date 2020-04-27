"""Utility class for converting each feature into tf.train.Features."""
import tensorflow as tf
from typing import Union, NamedTuple, List
import enum


class FeatureType(enum.Enum):
    STRING = "str"
    FLOAT = "float"
    BOOL = "bool"
    INT = "int"
    BYTES = "bytes"


class Metadata(NamedTuple):
    name: str
    feature_type: FeatureType


class Converter:
    @classmethod
    def build_example(
        cls, data_list: List[Union[str, bytes, float, int, bool]], metadatas: List[Metadata]
    ) -> tf.train.Example:
        """
        Build tf.train.Example object by given data list and metadata.

        :param data_list: List of target data Tensor
        :param metadatas: List of :class:`<tfrecord_converter.converter.Metadata>`
        :return: tf.train.Example object
        """
        if len(data_list) != len(metadatas):
            raise ValueError("Length of data list should be equal with length of metadata list.")

        feature = {
            metadata.name: cls.featurize(data, metadata.feature_type) for data, metadata in zip(data_list, metadatas)
        }

        return tf.train.Example(features=tf.train.Features(feature=feature))

    @classmethod
    def featurize(cls, tensor: Union[str, bytes, float, int, bool], feature_type: FeatureType) -> tf.train.Feature:
        """
        Featurize one Tensor into tf.train.Feature.

        :param tensor: Target Tensor
        :param feature_type: :class:`<tfrecord_converter.converter.FeatureType>`
        :returns: tf.train.Feature object
        """
        if feature_type in (FeatureType.STRING, FeatureType.BYTES):
            return cls._bytes_feature(tensor)
        if feature_type == FeatureType.FLOAT:
            return cls._float_feature(tensor)
        if feature_type in (FeatureType.INT, FeatureType.BOOL):
            return cls._int64_feature(tensor)
        raise ValueError(f"Got unexpected feature type: {feature_type}")

    @staticmethod
    def _bytes_feature(value: Union[str, bytes]) -> tf.train.Feature:
        """Returns a bytes_list from a string / byte."""
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
        if isinstance(value, str):
            value = value.encode()  # Transition from string to bytes
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _float_feature(value: Union[float, int]) -> tf.train.Feature:
        """Returns a float_list from a float / double."""
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _int64_feature(value: Union[int, bool]) -> tf.train.Feature:
        """Returns an int64_list from a bool / enum / int / uint."""
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
