import pytest

from tfrecorder.config import Config, ExecutionMode


@pytest.mark.parametrize(
    "only_convert, only_upload, expected",
    [
        pytest.param(False, False, ExecutionMode.CONVERT_AND_UPLOAD),
        pytest.param(True, False, ExecutionMode.CONVERT),
        pytest.param(False, True, ExecutionMode.UPLOAD),
    ],
    ids=["Convert & Upload", "Only Convert", "Only Upload"],
)
def test_get_exec_mode(only_convert, only_upload, expected, config):
    config["only_convert"] = only_convert
    config["only_upload"] = only_upload
    config = Config(**config)
    assert expected == config.exec_mode
