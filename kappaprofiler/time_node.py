import time

class TimeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        if self.parent is not None:
            self.parent.children[name] = self
        self.children = {}
        self.total_time = 0.
        self.count = 0
        self.start_time = None

    def start(self):
        assert self.start_time is None, "need to stop TimeNode before starting it again"
        self.start_time = time.time()

    def stop(self):
        assert self.start_time is not None, "need to start TimeNode before stopping it"
        self.total_time += time.time() - self.start_time
        self.count += 1
        self.start_time = None

    def to_string_lines(self, prefix=None):
        lines = []
        for name, node in self._traverse(prefix=prefix):
            # 9.2f --> up to 11.5d
            lines.append(f"{node.total_time:9.2f} {name}")
        return lines

    def _traverse(self, prefix=None, ret=None):
        if ret is None:
            ret = []
        if prefix is None:
            name = self.name
        else:
            name = f"{prefix}.{self.name}"
        ret.append((name, self))

        for child in self.children.values():
            child._traverse(prefix=name, ret=ret)
        return ret

    def __repr__(self):
        return self.name