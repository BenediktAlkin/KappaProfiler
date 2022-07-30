class RootNode:
    def __init__(self):
        self.children = {}

    def to_dotlist(self):
        dotlist = []
        for root_node in self.children.values():
            dotlist += root_node.to_dotlist()
        return dotlist