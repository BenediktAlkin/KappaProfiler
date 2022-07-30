import kappaprofiler as kp
import time


@kp.profile
def main():
    time.sleep(0.3)  # simulate some operation
    some_method()


@kp.profile
def some_method():
    time.sleep(0.5)  # simulate some operation


if __name__ == "__main__":
    main()
    print(kp.profiler.to_string())