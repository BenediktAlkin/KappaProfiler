from .stopwatch import Stopwatch
from .profiler import Profiler

profiler = Profiler()

def profile(func):
    def _profile(*args, **kwargs):
        with profiler.profile(func.__name__):
            return func(*args, **kwargs)
    return _profile

def named_profile(name, profiler_to_use=None):
    global profiler
    profiler_to_use = profiler_to_use or profiler
    return profiler_to_use.profile(name)

def pprofile(profiler_to_use=None):
    global profiler
    profiler_to_use = profiler_to_use or profiler

    def _profile(func):
        def __profile(*args, **kwargs):
            with profiler_to_use.profile(func.__name__):
                return func(*args, **kwargs)

        return __profile
    return _profile