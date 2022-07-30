import unittest
import kappaprofiler as kp


class TestInit(unittest.TestCase):
    def test_imports(self):
        kp.Stopwatch()
        kp.Profiler()
        self.assertIsNotNone(kp.profiler)