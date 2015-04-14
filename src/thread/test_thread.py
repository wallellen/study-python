# coding=utf-8

from unittest import TestCase
import threading
import time


class TestThread(TestCase):
    def test_start_thread_by_function(self):
        total = 0

        def runner(times):
            for x in range(times):
                nonlocal total
                total += 1

        thread = threading.Thread(target=runner, kwargs=dict(times=10))
        thread.start()
        self.assertEqual(total, 10)

    def test_start_thread_by_runner_instance(self):
        class Runner(threading.Thread):
            def __init__(self, times):
                super().__init__()
                self.__n, self.__times = 0, times

            @property
            def n(self):
                return self.__n

            def run(self):
                for x in range(self.__times):
                    self.__n += 1

        runner = Runner(10)
        runner.start()
        runner.join()
        self.assertEqual(runner.n, 10)

    def test_start_thread_by_callable_instance(self):
        class Runner():
            def __init__(self):
                self.__n = 0

            @property
            def n(self):
                return self.__n

            def __call__(self, **kwargs):
                for x in range(kwargs['times']):
                    self.__n += 1

        runner = Runner()
        thread = threading.Thread(target=runner, kwargs=dict(times=10))
        thread.start()
        self.assertEqual(runner.n, 10)

    def test_sleep(self):
        def runner(sleep_time):
            time.sleep(sleep_time)

        thread = threading.Thread(target=runner, args=(0.5,))
        thread.start()
        ts = time.time()
        thread.join()
        te = time.time()
        self.assertGreaterEqual((te - ts) * 1000, 500)

    def test_active_count(self):
        self.assertEqual(threading.active_count(), 1)

        class TestThread(threading.Thread):
            def __init__(self, condition):
                super().__init__()
                self.__condition = condition

            def run(self):
                self.__condition.acquire()
                try:        # also can use 'with self.__condition'
                    self.__condition.wait()
                finally:
                    self.__condition.release()

        condition = threading.Condition()
        thread = TestThread(condition)
        thread.start()
        self.assertEqual(threading.active_count(), 2)

        condition.acquire()
        try:        # also can use 'with self.condition'
            condition.notify()
        finally:
            condition.release()

        thread.join()
