import time

# Custom decorator for logging
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Logging: Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Custom decorator for timing
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Timing: {func.__name__} took {elapsed:.2f} seconds")
        return res
    return wrapper
