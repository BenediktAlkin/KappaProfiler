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