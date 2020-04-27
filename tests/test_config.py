import pytest

from tfrecorder.config import Config


@pytest.mark.parametrize(
    "only_convert, only_upload, expected",
    [
        pytest.param(False, False, "Convert & Upload"),
        pytest.param(True, False, "Convert"),
        pytest.param(False, True, "Upload"),
    ],
    ids=["Convert & Upload", "Only Convert", "Only Upload"],
)
def test_get_exec_mode(only_convert, only_upload, expected):
    config = Config("", "", "", [], "", "", only_convert, only_upload, 0, 0)
    assert expected == config.get_exec_mode()
