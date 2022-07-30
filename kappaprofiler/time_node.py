from .time_provider import TimeProvider

class TimeNode:
    def __init__(self, name, parent=None, time_provider=None):
        self.name = name
        self.time_provider = time_provider or TimeProvider()
        self.parent = parent
        if self.parent is not None:
            assert name not in self.parent.children
            self.parent.children[name] = self
        self.children = {}
        self.total_time = 0.
        self.count = 0
        self.start_time = None

    def start(self):
        assert self.start_time is None, "need to stop TimeNode before starting it again"
        self.start_time = self.time_provider.time()

    def stop(self):
        assert self.start_time is not None, "need to start TimeNode before stopping it"
        self.total_time += self.time_provider.time() - self.start_time
        self.count += 1
        self.start_time = None

    def to_dotlist(self):
        return self._to_dotlist()

    def _to_dotlist(self, prefix=None, result=None):
        if result is None:
            result = []
        if prefix is None:
            name = self.name
        else:
            name = f"{prefix}.{self.name}"
        result.append((name, self))

        for child in self.children.values():
            child._to_dotlist(prefix=name, result=result)
        return result

    def __repr__(self):
        return self.name