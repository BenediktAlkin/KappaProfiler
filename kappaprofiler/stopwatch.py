import time


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self._elapsed_seconds = None

    def start(self):
        assert self.start_time is None, "can't start running stopwatch"
        self.start_time = time.time()
        return self

    def stop(self):
        assert self.start_time is not None, "can't stop a stopped stopwatch"
        self._elapsed_seconds = time.time() - self.start_time
        self.start_time = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    @property
    def elapsed_seconds(self):
        assert self._elapsed_seconds is not None, "stopwatch has to be started and stopped before a time can be read"
        return self._elapsed_seconds

    @property
    def elapsed_milliseconds(self):
        return self.elapsed_seconds * 1000