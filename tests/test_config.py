import pytest

from tfrecorder.config import Config


@pytest.mark.parametrize(
    "only_convert, only_upload, expected",
    [pytest.param(False, False, 0), pytest.param(True, False, 2), pytest.param(False, True, 1)],
    ids=["Convert & Upload", "Only Convert", "Only Upload"],
)
def test_get_exec_mode(only_convert, only_upload, expected, config):
    config["only_convert"] = only_convert
    config["only_upload"] = only_upload
    config = Config(**config)
    assert expected == config.get_exec_mode()
