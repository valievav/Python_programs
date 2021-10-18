# AsyncIO - framework enabling asynchronous single-threaded concurrent code

# Asynchronous programming - concurrent programming (as opposed to sequential)
# in a single process (as opposed to multiprocessing) and in a single thread (as opposed to multithreading) -
# runs functions interchangeably if CPU is idle / in really rapid alternation between functions
# (network operations, i/o operation etc.)

# Concurrency vs parallelism:
# concurrent execution - context switching - at the same time runs either func_1 OR func_2
# parallel execution - at the same time run BOTH functions

# Event loop - runs async tasks and callbacks (one operation at a time)

# Coroutine (or task) -  function that can be entered and exited multiple times, suspended and resumed each time

import asyncio


# ######################## synchronous programming in asynchronous function
async def main_sync():
    print('--- SYNC')
    print('main 1')
    await other_function()  # forced to wait for results with await - so NOT async, but simple sync programming
    print('main 2')


async def other_function():
    print('other function 1')
    # important! this is suspend point - we tell to hand over processing time to the event loop,
    # which will activate another function
    await asyncio.sleep(1)
    print('other function 2')

asyncio.run(main_sync())
# main 1
# other function 1
# other function 2
# main 2


# ######################## asynchronous programming
async def main_async():  # coroutine (need to be awaited OR passed to an event loop)
    print('--- ASYNC')
    task = asyncio.create_task(other_function())
    print('main 1')
    print('main 2')
    await task  # to wait for sleep in other_function, else will stop at 'other function 1'

asyncio.run(main_async())
# main 1
# main 2
# other function 1
# other function 2  # only if we have await task! else this line will not be awaited for


async def main_async_2_with_await_task():
    print('--- ASYNC with await task')
    task = asyncio.create_task(other_function())
    print('main 1')
    await asyncio.sleep(1)
    print('main 2')
    await task  # to wait for sleep in other_function, else will stop at 'other function 1'

asyncio.run(main_async_2_with_await_task())
# main 1
# other function 1  # executed during main func sleep
# main 2
# other function 2  # because we have await task


async def other_function_2_with_return():
    print('other function 1')
    await asyncio.sleep(1)
    print('other function 2')
    return 10


async def main_async_3_with_return():
    print('--- ASYNC with return')
    task = asyncio.create_task(other_function_2_with_return())
    print('main 1')
    await asyncio.sleep(1)
    print('main 2')
    return_value = await task  # get return value
    print(f'return value is {return_value}')


asyncio.run(main_async_3_with_return())
# main 1
# other function 1
# main 2
# other function 2
# return value is 10
