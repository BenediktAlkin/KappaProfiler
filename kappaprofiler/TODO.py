
# decorator/context manager for arbitrary method
class profile(DecoratorContextManager):
    def __init__(self, name, is_global=False):
        self.name = name
        self.is_global = is_global

    def __enter__(self):
        start(self.name, is_global=self.is_global)

    def __exit__(self, exc_type, exc_value, traceback):
        stop(is_global=self.is_global, name=self.name)


# decorator for @profile("%s.<method_name>" % self.<property_name>)
def profile_dynamic_name(property_name, format_str="%s", is_global=False):
    def decorater(func):
        def wrapper(self, *args, **kwargs):
            name = format_str % getattr(self, property_name)
            start(name, is_global=is_global)
            ret = func(self, *args, **kwargs)
            stop(is_global=is_global, name=name)
            return ret

        return wrapper

    return decorater

