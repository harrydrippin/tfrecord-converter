def batch(iterable, n=1):
    """Batch iterable by n."""
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx : min(ndx + n, length)]
