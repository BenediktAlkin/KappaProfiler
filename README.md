# KappaProfiler
Lightweight profiling utilities for identifying bottlenecks and timing program parts in your python application. 

# Setup
- new install: `pip install kappaprofiler`
- uprade to new version: `pip install kappaprofiler --upgrade` 

# Usage
## Time your whole application
### With decorators
```
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
```
The result will be (time.sleep calls are not 100% accurate)
```
0.82 main
0.51 main.some_method
```
### With contextmanagers
```
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
```
The result will be (time.sleep calls are not 100% accurate)
```
0.82 main
0.51 main.method
0.20 main2
```


## Time only a part of your program
```
import kappaprofiler as kp
with kp.Stopwatch() as sw:
    # some operation
    ...
print(f"operation took {sw.elapsed_milliseconds} milliseconds")
print(f"operation took {sw.elapsed_seconds} seconds")
```