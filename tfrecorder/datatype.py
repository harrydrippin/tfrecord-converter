import enum
from typing import NamedTuple, List
import json


class FeatureType(enum.Enum):
    STRING = "str"
    FLOAT = "float"
    BOOL = "bool"
    INT = "int"
    BYTES = "bytes"


class Metadata(NamedTuple):
    name: str
    feature_type: FeatureType


def parse_metadata(file_path: str) -> List[Metadata]:
    """Parse JSON file by given path and generate a list of metadata."""
    with open(file_path, "r") as f:
        obj = json.load(f)
    return [Metadata(item["name"], FeatureType(item["feature_type"])) for item in obj]
