from .time_provider import TimeProvider

class TimeNode:
    def __init__(self, name, parent=None, time_provider=None):
        self._name = name
        self._time_provider = time_provider or TimeProvider()
        self._parent = parent
        if self._parent is not None:
            assert name not in self._parent.children
            self._parent.children[name] = self
        self.children = {}
        self._last_time = None
        self._total_time = 0.
        self._count = 0
        self._start_time = None

    @property
    def count(self):
        return self._count

    @property
    def parent(self):
        return self._parent

    @property
    def last_time(self):
        return self._last_time

    @property
    def total_time(self):
        return self._total_time

    def start(self):
        assert self._start_time is None, "need to stop TimeNode before starting it again"
        self._start_time = self._time_provider.time()

    def stop(self):
        assert self._start_time is not None, "need to start TimeNode before stopping it"
        self._last_time = self._time_provider.time() - self._start_time
        self._total_time += self._last_time
        self._count += 1
        self._start_time = None

    def to_dotlist(self):
        return self._to_dotlist()

    def _to_dotlist(self, prefix=None, result=None):
        if result is None:
            result = []
        if prefix is None:
            name = self._name
        else:
            name = f"{prefix}.{self._name}"
        result.append((name, self))

        for child in self.children.values():
            child._to_dotlist(prefix=name, result=result)
        return result

    def __repr__(self):
        return self._name