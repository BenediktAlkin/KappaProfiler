import unittest
from kappaprofiler.time_node import TimeNode

class TestTimeNode(unittest.TestCase):
    def test_to_dotlist(self):
        root = TimeNode("root")
        child1 = TimeNode("child1", parent=root)
        child11 = TimeNode("child11", parent=child1)
        child2 = TimeNode("child2", parent=root)

        dotlist = root.to_dotlist()

        self.assertEqual(4, len(dotlist))
        self.assertEqual(("root", root), dotlist[0])
        self.assertEqual(("root.child1", child1), dotlist[1])
        self.assertEqual(("root.child1.child11", child11), dotlist[2])
        self.assertEqual(("root.child2", child2), dotlist[3])
