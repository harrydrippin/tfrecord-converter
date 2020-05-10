from abc import ABC
from typing import Generic, TypeVar, List
import tensorflow as tf

T = TypeVar("T")

class BaseStrategy(ABC, Generic[T]):
    name = "Base"

    def __init__(self):
        pass

    def __iter__(self, f: TextIO):
        for line in f:
            row = self.parse_row(line)
            feature = self.convert(row)
            yield tf.train.Example(features=tf.train.Features(feature=feature))

    def __call__(self, f: TextIO):
        rows: List[T] = [self.parse_row(line) for line in f]
        features: List[Dict[str, tf.train.Feature]] = [self.convert(row) for row in rows]
        examples: List[tf.train.Feature] = [tf.train.Example(features=tf.train.Features(feature=feature)) for feature in features]
        return examples

    @abstractmethod
    def parse_row(self, line: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def convert(self, row: T) -> Dict[str, tf.train.Feature]:
        raise NotImplementedError