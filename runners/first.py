import asyncio

async def run():
    delay = .5

    for i in range(0, 3):
        print("going to sleep {}".format(i))
        await asyncio.sleep(delay)
        print("woke up {}".format(i))

def execute():
    print("creating loop")
    loop = asyncio.get_event_loop()

    print("creating corouting")
    coroutine = run()

    print("running coroutine")
    loop.run_until_complete(coroutine)

    print("closing loop")
    loop.close()

