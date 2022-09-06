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


#### Time subparts
```
import kappaprofiler as kp
import time

sw1 = kp.Stopwatch()
sw2 = kp.Stopwatch()

for i in range(1, 3):
    with sw1:
        # operation1
        time.sleep(0.1 * i)
    with sw2:
        # operation2
        time.sleep(0.2 * i)

print(f"operation1 took {sw1.elapsed_seconds:.2f} seconds (average {sw1.average_lap_time:.2f})")
print(f"operation2 took {sw2.elapsed_seconds:.2f} seconds (average {sw2.average_lap_time:.2f})")
```
```
operation1 took 0.32 seconds (average 0.16)
operation2 took 0.61 seconds (average 0.30)
```