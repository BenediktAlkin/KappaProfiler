from .time_node import TimeNode

class Profiler:
    def __init__(self):
        self._root_node = None
        self._cur_node = None
        self._prev_node = None
        self._global_nodes = {}
        self._cur_global_node = None

    def start_global(self, name):
        self.start(name, is_global=True)

    def start(self, name, is_global=False):
        if is_global:
            self._start_global_node(name)
        else:
            self._start_node(name)

    def _start_global_node(self, name):
        if name not in self._global_nodes:
            self._global_nodes[name] = TimeNode(name)
        node = self._global_nodes[name]
        node.start()
        self._cur_global_node = node

    def _start_node(self, name):
        if self._root_node is None:
            # new root node
            self._cur_node = TimeNode(name)
            self._root_node = self._cur_node
            self._cur_node.start()
        else:
            if name in self._cur_node.children:
                # child already exists
                self._cur_node = self._cur_node.children[name]
            else:
                # new child
                self._cur_node = TimeNode(name, parent=self._cur_node)
            self._cur_node.start()

    def stop_global(self, name=None):
        self.stop(name=name, is_global=True)

    def stop(self, name=None, is_global=False):
        if is_global:
            if name is None:
                self._cur_global_node.stop()
                self._cur_global_node = None
            else:
                self._global_nodes[name].stop()
        else:
            self._cur_node.stop()
            self._prev_node = self._cur_node
            self._cur_node = self._cur_node.parent

    def to_string_lines(self):
        lines = []
        if len(self._global_nodes) > 0:
            for global_node in self._global_nodes.values():
                lines += global_node.to_string_lines(prefix="global")

        if self._root_node is not None:
            lines += self._root_node.to_string_lines()

        return lines