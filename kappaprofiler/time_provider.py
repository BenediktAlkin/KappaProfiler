from time import time

class TimeProvider:
    @staticmethod
    def time() -> float:
        return time()