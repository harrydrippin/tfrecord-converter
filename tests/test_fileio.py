import pytest

from tfrecorder.fileio import get_filenames, read_file


@pytest.fixture
def expected_file_output():
    return [
        ["SEND", "20200427030101", "1", "Hello! Nice to meet you :)"],
        ["RECV", "20200427030202", "1", "Good to see you!"],
    ]


def test_get_filenames():
    expected = set(["./tests/data/sample_tsv.tsv", "./tests/data/sample_tsv_with_header.tsv",])
    assert expected == set(get_filenames("./tests/data/*.tsv"))


@pytest.mark.parametrize(
    "path, mode, skip_header",
    [
        pytest.param("./tests/data/sample_csv.csv", "csv", False),
        pytest.param("./tests/data/sample_csv_with_header.csv", "csv", True),
        pytest.param("./tests/data/sample_tsv.tsv", "tsv", False),
        pytest.param("./tests/data/sample_tsv_with_header.tsv", "tsv", True),
    ],
    ids=["CSV", "CSV (Header)", "TSV", "TSV (Header)"],
)
def test_read_file(path, mode, skip_header, expected_file_output):
    assert expected_file_output == read_file(path, mode, skip_header=skip_header)
