from .time_node import TimeNode
from .time_provider import TimeProvider

class Profiler:
    def __init__(self, time_provider=None):
        self._time_provider = time_provider or TimeProvider()
        self._root_node = None
        self._cur_node = None
        self._prev_node = None

    def reset(self):
        self._root_node = None
        self._cur_node = None
        self._prev_node = None

    def start(self, name):
        if self._root_node is None:
            # new root node
            self._cur_node = TimeNode(name, time_provider=self._time_provider)
            self._root_node = self._cur_node
            self._cur_node.start()
        else:
            if name in self._cur_node.children:
                # child already exists
                self._cur_node = self._cur_node.children[name]
            else:
                # new child
                self._cur_node = TimeNode(name, parent=self._cur_node, time_provider=self._time_provider)
            self._cur_node.start()

    def stop(self):
        self._cur_node.stop()
        self._prev_node = self._cur_node
        self._cur_node = self._cur_node.parent


    def to_string(self):
        assert self._root_node is not None
        dotlist = self._root_node.to_dotlist()
        # 9.2f --> up to 11.5d
        return "\n".join([f"{node.total_time:9.2f} {name}" for name, node in dotlist])