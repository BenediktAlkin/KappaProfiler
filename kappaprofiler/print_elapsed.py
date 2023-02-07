from contextlib import contextmanager
from time import time

@contextmanager
def print_elapsed_seconds(name, seconds_format: str = ".2f", print_fn=print):
    start_time = time()
    yield
    end_time = time()
    # noinspection PyStringFormat
    seconds_str = f"{{:{seconds_format}}}".format(end_time - start_time)
    print_fn(f"{name} took {seconds_str} seconds")