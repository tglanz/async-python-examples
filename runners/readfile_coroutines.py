import asyncio
import aiofiles

async def read_file(file_path):
    print("reading file")
    async with aiofiles.open(file_path, mode='r') as file:
        while True:
            line = await file.readline()
            if not line:
                break
            print(line.strip())

async def print_loop(count):
    print("print loop start")
    for i in range(0, count):
        await asyncio.sleep(.01)
        print("index {}".format(i))
    print("print loop end")

async def run():
    await asyncio.gather(
        read_file("data/lorem-ipsum.txt"),
        print_loop(300)
    )

def execute():
    print("creating event loop")
    loop = asyncio.get_event_loop()

    print("creating coroutine")
    coro = run()

    print("dispatching coroutine to event loop")
    loop.run_until_complete(coro)