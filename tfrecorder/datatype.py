import enum
import json
from typing import List, NamedTuple, Tuple


class FeatureType(enum.Enum):
    STRING = "str"
    FLOAT = "float"
    BOOL = "bool"
    INT = "int"
    BYTES = "bytes"


class Column(NamedTuple):
    name: str
    feature_type: FeatureType


def parse_metadata(file_path: str) -> Tuple[str, str, List[Column]]:
    """Parse JSON file by given path and generate a list of metadata."""
    with open(file_path, "r") as f:
        obj = json.load(f)
    return (
        obj["dataset_path"],
        obj["tfrecord_path"],
        [Column(column["name"], FeatureType(column["feature_type"])) for column in obj["columns"]],
    )
