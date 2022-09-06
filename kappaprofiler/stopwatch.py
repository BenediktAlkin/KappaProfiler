from .time_provider import TimeProvider

class Stopwatch:
    def __init__(self, time_provider=None):
        self._start_time = None
        self._elapsed_seconds = []
        self._lap_start_time = None
        self._time_provider = time_provider or TimeProvider()

    def start(self):
        assert self._start_time is None, "can't start running stopwatch"
        self._start_time = self._time_provider.time()
        return self

    def stop(self):
        assert self._start_time is not None, "can't stop a stopped stopwatch"
        self._elapsed_seconds.append(self._time_provider.time() - self._start_time)
        self._start_time = None
        self._lap_start_time = None
        return self._elapsed_seconds[-1]

    def lap(self):
        assert self._start_time is not None, "lap requires stopwatch to be started"
        if self._lap_start_time is None:
            # first lap
            lap_time = self._time_provider.time() - self._start_time
        else:
            lap_time = self._time_provider.time() - self._lap_start_time
        self._elapsed_seconds.append(lap_time)
        self._lap_start_time = self._time_provider.time()
        return lap_time

    @property
    def last_lap_time(self):
        assert len(self._elapsed_seconds) > 0, "last_lap_time requires lap()/stop() to be called at least once"
        return self._elapsed_seconds[-1]

    @property
    def lap_count(self):
        return len(self._elapsed_seconds)

    @property
    def average_lap_time(self):
        assert len(self._elapsed_seconds) > 0, "average_lap_time requires lap()/stop() to be called at least once"
        return sum(self._elapsed_seconds) / len(self._elapsed_seconds)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    @property
    def elapsed_time(self):
        return self.elapsed_seconds

    @property
    def elapsed_seconds(self):
        assert self._start_time is None, "elapsed_seconds requires stopwatch to be stopped"
        assert len(self._elapsed_seconds) > 0, "elapsed_seconds requires stopwatch to have been started and stopped"
        return sum(self._elapsed_seconds)

    @property
    def elapsed_milliseconds(self):
        return self.elapsed_seconds * 1000