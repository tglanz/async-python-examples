import io

import asyncio
import concurrent

def read_file(file_path):
    print("reading file")
    with open(file_path, mode='r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            print(line.strip())

def print_loop(count, context):
    print("print loop start")
    for i in range(0, count):
        print("index {} - {}".format(context, i))
    print("print loop end")

async def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        await asyncio.gather(
            loop.run_in_executor(executor, read_file, "data/lorem-ipsum.txt"),
            loop.run_in_executor(executor, print_loop, 140, 'a'),
            loop.run_in_executor(executor, print_loop, 140, 'b'),
        )

def execute():
    print("creating event loop")
    loop = asyncio.get_event_loop()

    print("creating coroutine")
    coro = run()

    print("dispatching coroutine to event loop")
    loop.run_until_complete(coro)
    loop.close()