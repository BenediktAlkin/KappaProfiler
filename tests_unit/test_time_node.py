import unittest
from kappaprofiler.node import Node

class TestNode(unittest.TestCase):
    def test_to_dotlist(self):
        root = Node("root")
        child1 = Node("child1", parent=root)
        child11 = Node("child11", parent=child1)
        child2 = Node("child2", parent=root)

        dotlist = root.to_dotlist()

        self.assertEqual(3, len(dotlist))
        self.assertEqual(("child1", child1), dotlist[0])
        self.assertEqual(("child1.child11", child11), dotlist[1])
        self.assertEqual(("child2", child2), dotlist[2])

    def test_is_running(self):
        root = Node("root")
        self.assertFalse(root.is_running)
        root.start()
        self.assertTrue(root.is_running)
        root.stop()
        self.assertFalse(root.is_running)
