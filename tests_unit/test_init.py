import unittest
import kappaprofiler as kp


class TestInit(unittest.TestCase):
    test_decorator_single_profiler = kp.Profiler()
    test_decorator_nested_profiler = kp.Profiler()

    def test_imports(self):
        kp.Stopwatch()
        kp.Profiler()
        self.assertIsNotNone(kp.profiler)


    @kp.pprofile(profiler_to_use=test_decorator_single_profiler)
    def single_decorated_method(self):
        pass

    def test_decorator_single(self):
        self.single_decorated_method()
        dotlist = self.test_decorator_single_profiler.root_node.to_dotlist()
        self.assertEqual(1, len(dotlist))
        self.assertEqual("single_decorated_method", dotlist[0][0])



    @kp.pprofile(profiler_to_use=test_decorator_nested_profiler)
    def root_decorated_method(self):
        self.nested_decorated_method()

    @kp.pprofile(profiler_to_use=test_decorator_nested_profiler)
    def nested_decorated_method(self):
        pass

    def test_decorator_nested(self):
        self.root_decorated_method()
        dotlist = self.test_decorator_nested_profiler.root_node.to_dotlist()
        self.assertEqual(2, len(dotlist))
        self.assertEqual("root_decorated_method", dotlist[0][0])
        self.assertEqual("root_decorated_method.nested_decorated_method", dotlist[1][0])