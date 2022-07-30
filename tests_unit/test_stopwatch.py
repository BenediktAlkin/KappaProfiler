import unittest
from tests_util.mock_time_provider import MockTimeProvider
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
        laps = 10
        time_provider = MockTimeProvider()
        time_provider.set_time(0.)
        sw = Stopwatch(time_provider=time_provider).start()
        for i in range(laps):
            time_provider.add_time(1.5 + i)
            lap_time = sw.lap()
            self.assertEquals(1.5 + i, lap_time)
        self.assertEqual(laps, sw.lap_count)