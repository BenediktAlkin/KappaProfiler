import kappaprofiler as kp
import time


def main():
    with kp.named_profile("main"):
        time.sleep(0.3)  # simulate some operation
        with kp.named_profile("method"):
            some_method()
    with kp.named_profile("main2"):
        time.sleep(0.2)  # simulate some operation


def some_method():
    time.sleep(0.5)  # simulate some operation


if __name__ == "__main__":
    main()
    print(kp.profiler.to_string())