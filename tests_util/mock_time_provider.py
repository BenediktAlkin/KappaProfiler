

class MockTimeProvider:
    def __init__(self, initial_time=None):
        self._time = initial_time

    @staticmethod
    def _check_valid_time_param(time):
        assert isinstance(time, float) and time >= 0.

    def set_time(self, time):
        self._check_valid_time_param(time)
        self._time = time

    def add_time(self, time):
        self._check_valid_time_param(time)
        assert self._time is not None
        self._time += time

    def time(self):
        assert self._time is not None
        return self._time