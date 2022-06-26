import unittest

from kappaprofiler.profiler import Profiler


class TestProfiler(unittest.TestCase):
    def test_global_and_root_lines(self):
        p = Profiler()
        p.start("test")
        p.start("nested")
        p.start_global("global")
        p.stop("nested")
        p.stop("test")
        p.stop_global()
        lines = p.to_string_lines()
        self.assertEqual(3, len(lines))
        self.assertTrue(lines[0].endswith("global.global"))
        self.assertTrue(lines[1].endswith("test"))
        self.assertTrue(lines[2].endswith("test.nested"))

