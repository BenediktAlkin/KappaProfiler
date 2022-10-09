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

    def test_get_node(self):
        time_provider = MockTimeProvider(initial_time=0.)
        p = Profiler(time_provider=time_provider)
        with p.profile("root"):
            for _ in range(2):
                time_provider.add_time(1.2)
                with p.profile("nested"):
                    time_provider.add_time(1.7)

        with self.assertRaises(AssertionError) as e:
            p.get_node("root.invalid")
        self.assertEquals("invalid node query 'root.invalid'", str(e.exception))
        self.assertEquals("3.40", p.get_node("root.nested").to_string(time_format="4.2f"))


    def test_profile_async(self):
        time_provider = MockTimeProvider(initial_time=0.)
        p = Profiler(time_provider=time_provider)

        start_async = lambda: MockTimeProvider(initial_time=0.)

        def end_async(mtp: MockTimeProvider):
            mtp.add_time(1.2)
            return mtp.time()

        with p.profile_async("test", start_async, end_async):
            with p.profile("nested"):
                time_provider.add_time(0.3)


        self.assertEquals("1.20", p.get_node("test").to_string(time_format="4.2f"))
        self.assertEquals("0.30", p.get_node("test.nested").to_string(time_format="4.2f"))

    def test_noop_without_async_setup(self):
        p = Profiler()
        with p.profile_async("test", None, None):
            pass
        self.assertIsNone(p.last_node)

    def test_async_changes_cur_node(self):
        p = Profiler()

        start_async = lambda: MockTimeProvider(initial_time=0.)

        def end_async(mtp: MockTimeProvider):
            mtp.add_time(1.2)
            return mtp.time()

        with p.profile_async("test", start_async, end_async):
            pass
        self.assertEqual(p.root_node, p.cur_node)
        self.assertEqual("test", p.last_node.name)
