from tfrecorder.utils import batch


def test_batch():
    assert [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]] == list(batch(list(range(0, 10)), 3))
