import unittest
import kappaprofiler as kp

class TestRaiseException(unittest.TestCase):
    def test_stop_node_before_reraise(self):
        p = kp.Profiler()
        try:
            with p.profile("forward"):
                raise RuntimeError
            self.fail()
        except RuntimeError:
            pass
        self.assertEqual("root", p.cur_node.name)
        self.assertEqual("forward", p.last_node.name)
        self.assertFalse(p.last_node.is_running)
        self.assertGreater(p.last_node.count, 0)

    def test_stop_node_before_reraise_async_as_sync(self):
        p = kp.Profiler()
        try:
            with p.profile_async("forward", async_profile_start=kp.sync_start_event, async_profile_end=kp.sync_end_event):
                raise RuntimeError
            self.fail()
        except RuntimeError:
            pass
        self.assertEqual("root", p.cur_node.name)
        self.assertEqual("forward", p.last_node.name)
        self.assertFalse(p.last_node.is_running)
        self.assertGreater(p.last_node.count, 0)

    def test_stop_node_before_reraise_no_async_setup(self):
        p = kp.Profiler()
        try:
            with p.profile_async("forward", async_profile_start=None, async_profile_end=None):
                raise RuntimeError
            self.fail()
        except RuntimeError:
            pass
        # no asnyc setup -> nothing is recorded
        self.assertEqual("root", p.cur_node.name)
        self.assertIsNone(p.last_node)
        self.assertEqual(0, len(p.cur_node.children))
