import time


class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._elapsed_seconds = None
        self._elapsed_seconds_laps = []

    def start(self):
        assert self._start_time is None, "can't start running stopwatch"
        self._start_time = time.time()
        return self

    def stop(self):
        assert self._start_time is not None, "can't stop a stopped stopwatch"
        self._elapsed_seconds = time.time() - self._start_time
        self._start_time = None
        return self._elapsed_seconds

    def lap(self):
        assert self._start_time is not None, "lap requires stopwatch to be started"
        if len(self._elapsed_seconds_laps) > 0:
            lap_time = time.time() - self._elapsed_seconds_laps[-1]
        else:
            lap_time = time.time() - self._start_time
        self._elapsed_seconds_laps.append(lap_time)
        return lap_time

    @property
    def last_lap_time(self):
        assert len(self._elapsed_seconds_laps) > 0, "last_lap_time requires lap() to be called at least once"
        return self._elapsed_seconds_laps[-1]

    @property
    def lap_count(self):
        return len(self._elapsed_seconds_laps)

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