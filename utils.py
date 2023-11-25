import functools
import time


def timer(fn):
    @functools.wraps(fn)
    def timed(*args, **kwargs):
        start_time = time.perf_counter()
        value = fn(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {fn.__name__!r} in {run_time*1000:.4f} ms")
        return value
    return timed

