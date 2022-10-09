# KappaProfiler
Lightweight profiling utilities for identifying bottlenecks and timing program parts in your python application. 
Support for async profiling 

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

## Query nodes
Each profiling entry is represented by a node from which detailed information can be retrieved
```
query = "main.some_method"
node = kp.profiler.get_node(query)
print(f"{query} was called {node.count} time and took {node.to_string()} seconds in total")
```
`main.some_method was called 1 time and took 0.51 seconds in total`

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

## Time async operations
Showcase timing [cuda](https://developer.nvidia.com/cuda-toolkit) operations in 
[pytorch](https://github.com/pytorch/pytorch)

Asynchronous operations can only be timed properly when the asynchronous call is awaited or a synchronization point is
created after the timing should end. Natively in pytorch this would look something like this:
```
# submit a start event to the event stream
start_event = torch.cuda.Event(enable_timing=True)
start_event.record()

# submit a async operation to the event stream
...

# submit a end event to the event stream
end_event = torch.cuda.Event(enable_timing=True)
end_event.record()

# synchronize
torch.cuda.synchronize()

print(start_event.elapsed_time(end_event))
```
which is quite a lot of boilerplate for timing one operation.

With kappaprofiler it looks like this:
```
import kappaprofiler as kp
import torch

def main():
    device = torch.device("cuda")
    x = torch.randn(15000, 15000, device=device)
    with kp.named_profile("matmul_wrong"):
        # matrix multiplication (@) is asynchronous
        _ = x @ x
    # the timing for "matmul_wrong" is only the time it took to
    # submit the x @ x operation to the cuda event stream
    # not the actual time the x @ x operation took

    with kp.named_profile_async("matmul_right"):
        _ = x @ x
    matmul_method(x)

@kp.profile_async
def matmul_method(x):
    _ = x @ x

def start_async():
    start_event = torch.cuda.Event(enable_timing=True)
    start_event.record()
    return start_event

def end_async(start_event):
    end_event = torch.cuda.Event(enable_timing=True)
    end_event.record()
    torch.cuda.synchronize()
    # torch.cuda.Event.elapsed_time returns milliseconds but kappaprofiler expects seconds
    return start_event.elapsed_time(end_event) / 1000


if __name__ == "__main__":
    kp.setup_async(start_async, end_async)
    main()
    print(kp.profiler.to_string())
```
```
0.56 matmul_wrong
4.69 matmul_right
4.72 matmul_right.matmul_method
```

If you want to remove all synchronization points in your program, simply remove the 
`kp.setup_async(start_async, end_async)` call and `kp.named_profile_async`/`kp.profile_async` will default to a noop.