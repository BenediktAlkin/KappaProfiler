import time
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

    def test_lap_without_start(self):
        self.assertRaises(AssertionError, lambda: Stopwatch().lap())

    def test_lap_after_stop(self):
        with self.assertRaises(AssertionError):
            sw = Stopwatch().start()
            sw.stop()
            sw.lap()

    def test_lap(self):
        sw = Stopwatch().start()
        sw.lap()
        self.assertEqual(1, sw.lap_count)

    def test_laps(self):
        sleep_time = 0.001
        laps = 10
        sw = Stopwatch().start()
        for _ in range(laps):
            time.sleep(sleep_time)
            self.assertGreater(sw.lap(), sleep_time)
        self.assertEqual(laps, sw.lap_count)