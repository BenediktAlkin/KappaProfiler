import unittest
from kappaprofiler.time_node import TimeNode

class TestTimeNode(unittest.TestCase):
    def test_to_dotlist(self):
        root = TimeNode("root")
        child1 = TimeNode("child1", parent=root)
        child11 = TimeNode("child11", parent=child1)
        child2 = TimeNode("child2", parent=root)

        dotlist = root.to_dotlist()

        self.assertEqual(3, len(dotlist))
        self.assertEqual(("child1", child1), dotlist[0])
        self.assertEqual(("child1.child11", child11), dotlist[1])
        self.assertEqual(("child2", child2), dotlist[2])
