from contextlib import contextmanager

from .time_node import TimeNode
from .root_node import RootNode
from .time_provider import TimeProvider

class Profiler:
    def __init__(self, time_provider=None):
        self._time_provider = time_provider or TimeProvider()
        self._root_node = RootNode()
        self._cur_node = self._root_node
        self._last_node = None

    @property
    def root_node(self):
        return self._root_node

    @property
    def last_node(self):
        return self._last_node

    def reset(self):
        self._root_node = None
        self._cur_node = None
        self._last_node = None

    def start(self, name):
        if name in self._cur_node.children:
            # child already exists
            self._cur_node = self._cur_node.children[name]
        else:
            # new child
            self._cur_node = TimeNode(name, parent=self._cur_node, time_provider=self._time_provider)
        self._cur_node.start()

    def stop(self):
        self._cur_node.stop()
        self._last_node = self._cur_node
        self._cur_node = self._cur_node.parent

    @contextmanager
    def profile(self, name):
        self.start(name)
        yield
        self.stop()

    def to_string(self, time_format="9.2f"):
        # 9.2f --> up to 11.5d
        assert self._root_node is not None
        dotlist = self._root_node.to_dotlist()
        return "\n".join([f"{format(node.total_time, time_format)} {name}" for name, node in dotlist if node.count > 0])