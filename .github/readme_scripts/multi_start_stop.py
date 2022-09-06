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