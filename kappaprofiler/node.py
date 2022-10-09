from .time_provider import TimeProvider
from typing import List, Dict

class Node:
    def __init__(self, name: str = None, parent: "Node" = None, time_provider: TimeProvider = None):
        super().__init__()
        self._parent: "Node" = parent
        self.children: Dict[str, "Node"] = {}
        if self._parent is not None:
            assert name is not None
            assert name not in self._parent.children
            self._parent.children[name] = self
            self._name: str = name
        else:
            assert name is None or name == "root"
            self._name: str = "root"

        self._time_provider: TimeProvider = time_provider or TimeProvider()
        self._last_time: float = None
        self._total_time: float = 0.
        self._count: int = 0
        self._start_time: float = None

    @property
    def count(self) -> int:
        return self._count

    @property
    def parent(self) -> "Node":
        return self._parent

    @property
    def last_time(self) -> float:
        return self._last_time

    @property
    def total_time(self) -> float:
        return self._total_time

    def start(self) -> None:
        assert self._start_time is None, "need to stop Node before starting it again"
        self._start_time = self._time_provider.time()

    def stop(self) -> None:
        assert self._start_time is not None, "need to start Node before stopping it"
        self.add_time(self._time_provider.time() - self._start_time)
        self._start_time = None

    def add_time(self, time: float) -> None:
        self._last_time = time
        self._total_time += self._last_time
        self._count += 1

    def to_dotlist(self) -> List[str]:
        if self._parent is None:
            # root node
            dotlist = []
            for node in self.children.values():
                dotlist += node.to_dotlist()
            return dotlist
        else:
            return self._to_dotlist()

    def _to_dotlist(self, prefix: str = None, result: List[str] = None) -> List[str]:
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

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    def to_string(self, time_format: str = ".2f") -> str:
        return format(self.total_time, time_format)