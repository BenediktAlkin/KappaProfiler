

class MockTimeProvider:
    def __init__(self, initial_time: float = None):
        self._time = initial_time

    @staticmethod
    def _check_valid_time_param(time):
        assert isinstance(time, float) and time >= 0.

    def set_time(self, time: float) -> None:
        self._check_valid_time_param(time)
        self._time = time

    def add_time(self, time: float) -> None:
        self._check_valid_time_param(time)
        assert self._time is not None
        self._time += time

    def time(self) -> float:
        assert self._time is not None
        return self._time