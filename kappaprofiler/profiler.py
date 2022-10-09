import logging
from contextlib import contextmanager
from typing import Callable, Any

from .node import Node
from .time_provider import TimeProvider

class Profiler:
    def __init__(self, time_provider: TimeProvider = None):
        self._time_provider: TimeProvider = None
        self._root_node: Node = None
        self._cur_node: Node = None
        self._last_node: Node = None
        self.reset(time_provider=time_provider)


    def reset(self, time_provider: TimeProvider = None) -> None:
        self._time_provider: TimeProvider = time_provider or TimeProvider()
        self._root_node: Node = Node()
        self._cur_node: Node = self._root_node
        self._last_node: Node = None


    @property
    def root_node(self) -> Node:
        return self._root_node

    @property
    def last_node(self) -> Node:
        return self._last_node

    @property
    def cur_node(self) -> Node:
        return self._cur_node

    def _start(self, name: str) -> None:
        if name in self._cur_node.children:
            # child already exists
            self._cur_node = self._cur_node.children[name]
        else:
            # new child
            self._cur_node = Node(name, parent=self._cur_node, time_provider=self._time_provider)

    def start(self, name: str) -> None:
        self._start(name)
        self._cur_node.start()

    def start_async(self, name: str) -> Node:
        self._start(name)
        return self._cur_node

    def _stop(self) -> None:
        self._last_node = self._cur_node
        self._cur_node = self._cur_node.parent

    def stop(self) -> None:
        self._stop()
        self._cur_node.stop()

    @contextmanager
    def profile(self, name: str) -> None:
        self.start(name)
        yield
        self.stop()

    @contextmanager
    def profile_async(
            self,
            name: str,
            async_profile_start: Callable[[], Any],
            async_profile_end: Callable[[Any], float],
    ) -> None:
        if async_profile_start is None or async_profile_end is None:
            yield
        else:
            node = self.start_async(name)
            async_event = async_profile_start()
            yield
            elapsed_time = async_profile_end(async_event)
            node.add_time(elapsed_time)
        self._stop()

    def to_string(self, time_format: str = "9.2f") -> str:
        # 9.2f --> up to 11.5d
        assert self._root_node is not None
        dotlist = self._root_node.to_dotlist()
        return "\n".join([f"{node.to_string(time_format)} {name}" for name, node in dotlist if node.count > 0])

    def get_node(self, query: str) -> Node:
        accessors = query.split(".")
        cur_node = self._root_node
        for i, accessor in enumerate(accessors):
            assert accessor in cur_node.children, f"invalid node query '{'.'.join(accessors[:i+1])}'"
            cur_node = cur_node.children[accessor]
        return cur_node