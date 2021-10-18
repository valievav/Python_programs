import queue
import requests
from codetiming import Timer


# ########## SYNC example
def get_url(task_name, url_queue):
    """
    Get URL based on url_queue
    """
    timer = Timer(text=f"{task_name} elapsed time: {{:.1f}}")
    with requests.Session() as session:
        while not url_queue.empty():
            url = url_queue.get()
            print(f"{task_name} getting URL: {url}")
            timer.start()
            session.get(url)
            timer.stop()
            yield


def main_sync():
    # Create the queue
    work_queue = queue.Queue()

    # Define URLs the queue
    for url in [
        "http://google.com",
        "http://youtube.com/",
        "http://udemy.com/",
        "http://pluralsight.com/",
        "http://realpython.com/",
        "https://developer.ibm.com/"
    ]:
        work_queue.put(url)

    tasks = [get_url("Task 1", work_queue),
             get_url("Task 2", work_queue)]

    # Run the tasks
    done = False
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        while not done:
            for t in tasks:
                try:
                    next(t)
                except StopIteration:
                    tasks.remove(t)
                if len(tasks) == 0:
                    done = True


main_sync()
# Task 1 getting URL: http://google.com
# Task 1 elapsed time: 0.4
# Task 2 getting URL: http://youtube.com/
# Task 2 elapsed time: 0.6
# Task 1 getting URL: http://udemy.com/
# Task 1 elapsed time: 0.8
# Task 2 getting URL: http://pluralsight.com/
# Task 2 elapsed time: 1.6
# Task 1 getting URL: http://realpython.com/
# Task 1 elapsed time: 0.8
# Task 2 getting URL: https://developer.ibm.com/
# Task 2 elapsed time: 0.8
#
# Total elapsed time: 5.0

# ############## Rewritten to async
import asyncio  #instead of requests
import aiohttp


async def get_url_async(task_name, url_queue):  # translated to coroutine
    """
    Get URL based on url_queue
    """
    timer = Timer(text=f"{task_name} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession() as session:
        while not url_queue.empty():
            url = await url_queue.get()  # wait until loaded url_queue
            print(f"{task_name} getting URL: {url}")
            timer.start()
            async with session.get(url) as response:
                await response.text()  # wait until got response
            timer.stop()


async def main_async():
    # Create the queue
    work_queue = asyncio.Queue()

    # Define URLs the queue
    for url in [
        "http://google.com",
        "http://youtube.com/",
        "http://udemy.com/",
        "http://pluralsight.com/",
        "http://realpython.com/",
        "https://developer.ibm.com/"
    ]:
        await work_queue.put(url)

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(get_url_async("Task 1", work_queue)),
            asyncio.create_task(get_url_async("Task 2", work_queue))
        )  # create tasks and gather under event loop


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Windows has problem with EventLoopPolicy
asyncio.run(main_async())   # run with async since this is coroutine
# Task 1 getting URL: http://google.com
# Task 2 getting URL: http://youtube.com/
# Task 1 elapsed time: 0.4
# Task 1 getting URL: http://udemy.com/
# Task 2 elapsed time: 0.6
# Task 2 getting URL: http://pluralsight.com/
# Task 1 elapsed time: 0.8
# Task 1 getting URL: http://realpython.com/
# Task 2 elapsed time: 0.7
# Task 2 getting URL: https://developer.ibm.com/
# Task 1 elapsed time: 0.7
# Task 2 elapsed time: 0.7
#
# Total elapsed time: 2.0  # time twice as less than sync program!
