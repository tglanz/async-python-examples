from argparse import ArgumentParser

import runners.first
import runners.producer_consumer
import runners.readfile_coroutines
import runners.readfile_threads
import runners.async_writer

runners_by_name = {
    'first': runners.first,
    'producer-consumer': runners.producer_consumer,
    'readfile-coroutines': runners.readfile_coroutines,
    'readfile-threads': runners.readfile_threads,
    'async_writer': runners.async_writer,
}

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('runner', type=str)
    args = parser.parse_args()
    runner_name = args.runner
    
    runner = runners_by_name[runner_name]
    if runner is None:
        print("No such runner {}", runner_name)
    else:
        runners_by_name[runner_name].execute()