from queue import Queue, Empty
import time
import asyncio
import concurrent

def consume(write_file, transform, queue, should_consume):
    while True:
        try:
            item = queue.get(True, 1)
            transformed_item = transform(item)
            if transformed_item is not None:
                write_file.write(transformed_item)
            queue.task_done()
        except Empty:
            if not should_consume():
                break
            time.sleep(1)

def produce(queue, item):
    queue.put(item)

class AsyncWriterContext:
    def __init__(self, loop):
        self.loop = loop
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.queue = Queue()
        self.should_consume = False

    async def stop_consuming(self):
        self.should_consume = False
        self.queue.join()

    async def start_consuming(self, write_file, transform_item):
        self.should_consume = True
        await self.loop.run_in_executor(self.executor, consume, write_file, transform_item, self.queue, lambda: self.should_consume)

    async def put(self, item):
        await self.loop.run_in_executor(self.executor, produce, self.queue, item)

async def entry_point(async_writer_context):
    for i in range(0, 5):
        await async_writer_context.put(i)

    time.sleep(3)

    for i in range(8, 12):
        await async_writer_context.put(i)
        
    await async_writer_context.stop_consuming()

def execute():
    loop = asyncio.get_event_loop()
    async_writer_context = AsyncWriterContext(loop)

    with open('out.bin', 'wb') as file:
        loop.run_until_complete(
            asyncio.gather(
                entry_point(async_writer_context),
                async_writer_context.start_consuming(file, bytes)
            )
        )