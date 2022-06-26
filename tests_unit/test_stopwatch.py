import unittest

from kappaprofiler.stopwatch import Stopwatch


class TestStopwatch(unittest.TestCase):
    def test_with(self):
        with Stopwatch() as s:
            pass
        self.assertIsNotNone(s._elapsed_seconds)

    def test_double_start(self):
        self.assertRaises(AssertionError, lambda: Stopwatch().start().start())

    def test_stop_without_start(self):
        self.assertRaises(AssertionError, lambda: Stopwatch().stop())
