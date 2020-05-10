from typing import Union, List

import tensorflow as tf

def convert_bytes(value: Union[str, bytes]) -> tf.train.Feature:
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    if isinstance(value, str):
        value = value.encode()  # Transition from string to bytes
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def convert_floats(value: Union[List[float], List[int]]) -> tf.train.Feature:
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def convert_ints(value: Union[List[int], List[bool]]) -> tf.train.Feature:
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def batch(iterable, n=1):
    """Batch iterable by n."""
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx : min(ndx + n, length)]