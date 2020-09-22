from functools import wraps
from time import perf_counter, sleep


### Function-based

def get_runtime(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        print(f'Started')
        result = fn(*args, **kwargs)
        end = perf_counter() - start
        print(f'Run time {end}')
        return result
    return inner


@get_runtime
def function(x):
    sleep(3)
    result = [i for i in x]
    return result

print(function(range(11)))


### Class-based

class GetTime:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        print('Started')
        start = perf_counter()
        result = self.fn(*args, **kwargs)
        end = perf_counter() - start
        print(f'Run time {end}')
        return result

@GetTime
def function2(x):
    sleep(3)
    result = [i for i in x]
    return result

print(function2("simple sentence"))
