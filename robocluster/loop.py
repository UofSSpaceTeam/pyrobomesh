import asyncio
import contextlib
from abc import ABC, abstractmethod
from concurrent.futures import Future
from threading import Thread


class LoopThread(Thread):
    """A class that runs an event loop in a separate thread."""

    def __init__(self, name=None, loop=None, cancel_remaining_tasks=True):
        """
        Construct a thread responsible for running an asyncio event loop.

        Arguments are:
        *name* is the thread name. As per threading.Thread.

        *loop* is the event loop to run. By default this is created as per
        asyncio.new_event_loop().

        *cancel_remaining_tasks* is a boolean that states whether to cancel
        unfinished tasks in the event loop on stop.
        """
        super().__init__(name=name)
        self.loop = loop if loop else asyncio.new_event_loop()
        self.cancel_remaining_tasks = cancel_remaining_tasks

    def run(self):
        """Run the event loop."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

        if not self.cancel_remaining_tasks:
            return

        for task in asyncio.Task.all_tasks(loop=self.loop):
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                self.loop.run_until_complete(task)

    def create_task(self, coro):
        """
        Create a task in the event loop from the given coroutine.
        """
        loop = asyncio.get_event_loop()
        if loop is self.loop:
            return loop.create_task(coro)

        if not self.loop.is_running():
            msg = 'Event loop must be running to create from different thread.'
            raise RuntimeError(msg)

        future = Future()
        def _create_task():
            task = self.loop.create_task(coro)
            future.set_result(task)
        self.loop.call_soon_threadsafe(_create_task)
        # blocks until task has been created by the loop
        return future.result()

    def cancel_task(self, task):
        """Cancel a task in the event loop."""
        self.loop.call_soon_threadsafe(task.cancel)

    def stop(self):
        """Stop event loop and thread."""
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join()


class Looper:
    def __init__(self, loop=None):
        self._loop = loop if loop else asyncio.get_event_loop()
        self._coros = []
        self._tasks = None

    def create_task(self, coro):
        return self._loop.create_task(coro)

    def add_daemon_task(self, coro, *args, **kwargs):
        self._coros.append((coro, args, kwargs))
        if self._tasks is not None:
            self.create_task(coro(*args, **kwargs))

    def sleep(self, seconds):
        return asyncio.sleep(seconds, loop=self._loop)

    def start(self):
        if self._tasks is not None:
            raise RuntimeError('Already running')

        self._tasks = []
        for coro, args, kwargs in self._coros:
            task = self._loop.create_task(coro(*args, **kwargs))
            self._tasks.append(task)

    def stop(self):
        if self._tasks is None:
            return
        for task in self._tasks:
            task.cancel()
        self._tasks = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.stop()
