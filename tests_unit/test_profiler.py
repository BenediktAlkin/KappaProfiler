import unittest
from tests_util.mock_time_provider import MockTimeProvider
from kappaprofiler.profiler import Profiler


class TestProfiler(unittest.TestCase):
    def test_profile(self):
        p = Profiler()
        with p.profile("root"):
            with p.profile("nested"):
                pass
        dotlist = p.root_node.to_dotlist()
        self.assertEqual(2, len(dotlist))
        self.assertEquals("root", dotlist[0][0])
        self.assertEquals("root.nested", dotlist[1][0])

    def test_start_stop(self):
        p = Profiler()
        p.start("root")
        p.start("nested")
        p.stop()
        p.stop()
        dotlist = p.root_node.to_dotlist()
        self.assertEqual(2, len(dotlist))
        self.assertEquals("root", dotlist[0][0])
        self.assertEquals("root.nested", dotlist[1][0])

    def test_to_string(self):
        time_provider = MockTimeProvider(initial_time=0.)
        p = Profiler(time_provider=time_provider)
        with p.profile("root"):
            for _ in range(2):
                time_provider.add_time(1.2)
                with p.profile("nested"):
                    time_provider.add_time(1.7)

        expected = "\n".join([
            "5.80 root",
            "3.40 root.nested",
        ])
        self.assertEquals(expected, p.to_string(time_format="4.2f"))
