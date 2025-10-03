import time

# Custom decorator for logging
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Logging: Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
