import torch.distributed as dist

def end_async(start_event):
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
    end_event = torch.cuda.Event(enable_timing=True)
    end_event.record()
    torch.cuda.synchronize()
    # torch.cuda.Event.elapsed_time returns milliseconds but kappaprofiler expects seconds
    return start_event.elapsed_time(end_event) / 1000