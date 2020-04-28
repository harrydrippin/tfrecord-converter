"""Utility class for converting each feature into tf.train.Features."""
import logging
from typing import List, Tuple, Union

import tensorflow as tf

from .config import Config
from .datatype import FeatureType
from .fileio import read_file


class Converter:
    @classmethod
    def convert_one_file(cls, inp: Tuple[str, Config]) -> Tuple[List[tf.train.Example], int]:
        file_path, config = inp
        try:
            parsed = read_file(file_path, config.mode, skip_header=config.skip_header, max_error=config.max_error)
        except ValueError as e:
            logging.error(e)

        return [cls.build_example(line, config) for line in parsed], len(parsed)

    @classmethod
    def build_example(cls, data_list: List[str], config: Config) -> tf.train.Example:
        """
        Build tf.train.Example object by given data list and metadata.

        :param data_list: List of target data Tensor
        :param metadatas: List of :class:`<tfrecorder.converter.Column>`
        :return: tf.train.Example object
        """
        if len(data_list) != len(config.columns):
            raise ValueError("Length of data list should be equal with length of metadata list.")

        feature = {
            column.name: cls.featurize(data, column.feature_type) for data, column in zip(data_list, config.columns)
        }

        return tf.train.Example(features=tf.train.Features(feature=feature))

    @classmethod
    def featurize(cls, value: str, feature_type: FeatureType) -> tf.train.Feature:
        """
        Featurize one Tensor into tf.train.Feature.

        :param value: Target value
        :param feature_type: :class:`<tfrecorder.converter.FeatureType>`
        :returns: tf.train.Feature object
        """
        if feature_type in (FeatureType.STRING, FeatureType.BYTES):
            return cls._bytes_feature(value)
        if feature_type == FeatureType.FLOAT:
            return cls._float_feature(float(value))
        if feature_type == FeatureType.INT:
            return cls._int64_feature(int(value))
        if feature_type == FeatureType.BOOL:
            # Only supports `0`, `1`, `True`, `true`, `False`, `false`
            value = value.strip().lower()
            return cls._int64_feature(value in ("1", "true"))
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
