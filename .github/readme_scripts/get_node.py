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
    query = "main.some_method"
    node = kp.profiler.get_node(query)
    print(f"{query} was called {node.count} time and took {node.to_string()} seconds in total")