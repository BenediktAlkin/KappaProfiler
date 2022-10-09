from .stopwatch import Stopwatch
from .profiler import Profiler
from typing import Callable, Any

profiler: Profiler = Profiler()
_profiler_start_async: Callable[[], Any] = None
_profiler_end_async: Callable[[Any], float] = None

def reset() -> None:
    global profiler
    profiler.reset()

def profile(func: Callable[..., Any]) -> Callable[..., Any]:
    def _profile(*args, **kwargs) -> Any:
        with profiler.profile(func.__name__):
            return func(*args, **kwargs)
    return _profile

def named_profile(name: str, profiler_to_use: Profiler = None) -> None:
    global profiler
    profiler_to_use = profiler_to_use or profiler
    return profiler_to_use.profile(name)

#region async
def setup_async(profiler_start_async: Callable[[], Any], profiler_end_async: Callable[[Any], float]):
    global _profiler_start_async, _profiler_end_async
    _profiler_start_async = profiler_start_async
    _profiler_end_async = profiler_end_async

def profile_async(func: Callable[..., Any]) -> Callable[..., Any]:
    global _profiler_start_async, _profiler_end_async

    def _profile(*args, **kwargs) -> Any:
        with profiler.profile_async(func.__name__, _profiler_start_async, _profiler_end_async):
            return func(*args, **kwargs)
    return _profile

def named_profile_async(name: str, profiler_to_use: Profiler = None) -> None:
    global profiler, _profiler_start_async, _profiler_end_async
    profiler_to_use = profiler_to_use or profiler
    return profiler_to_use.profile_async(name, _profiler_start_async, _profiler_end_async)
#endregion

#region setup async as sync
def setup_async_as_sync():
    global _profiler_start_async, _profiler_end_async
    _profiler_start_async = _sync_start_event
    _profiler_end_async = _sync_end_event

def _sync_start_event():
    return time()

def _sync_end_event(start_time):
    end_time = time()
    return end_time - start_time
#endregion

def pprofile(profiler_to_use: Profiler = None) -> Callable[..., Any]:
    global profiler
    profiler_to_use = profiler_to_use or profiler

    def _profile(func: Callable[..., Any]) -> Callable[..., Any]:
        def __profile(*args, **kwargs) -> Any:
            with profiler_to_use.profile(func.__name__):
                return func(*args, **kwargs)
        return __profile
    return _profile
