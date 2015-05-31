# coding=utf-8
from unittest import TestCase
import itertools


class TestIterator(TestCase):
    def test_yield_py2(self):
        """
        yield 相当于一个‘迭代值’发生器：
        1. ‘yield’语句包含在一个函数（方法）中，且位于一个循环内；
        2. 包含‘yield’语句的函数（方法）返回一个迭代器对象（iterator）；
        3. 每次通过‘next’访问迭代器，则会从‘yield’语句得到一个值；
        """
        keep = [False]

        def _range(min, max, step=1):
            while min < max:
                yield min  # 执行到此后暂停，等待通过迭代器取值
                min += step

                # 这里‘keep’值必须为‘True’，从中可以看到‘yield’语句是在其它代码访问一次迭代器后才会执行一次
                self.assertTrue(keep[0])
                keep[0] = False

        with self.assertRaises(StopIteration):
            it = iter(_range(1, 10))
            n = 1
            while True:
                self.assertEqual(next(it), n)
                n += 1
                keep[0] = True

        n = 1
        for v in _range(1, 10, 2):
            self.assertEqual(v, n)
            n += 2
            keep[0] = True

    '''
    @skip('only for py3')
    def test_yield_py3(self):
        """
        yield 相当于一个‘迭代值’发生器：
        1. ‘yield’语句包含在一个函数（方法）中，且位于一个循环内；
        2. 包含‘yield’语句的函数（方法）返回一个迭代器对象（iterator）；
        3. 每次通过‘next’访问迭代器，则会从‘yield’语句得到一个值；
        """
        keep = False

        def xrange(min, max, step=1):
            nonlocal keep

            while min < max:
                yield min  # 执行到此后暂停，等待通过迭代器取值
                min += step

                # 这里‘keep’值必须为‘True’，从中可以看到‘yield’语句是在其它代码访问一次迭代器后才会执行一次
                self.assertTrue(keep)
                keep = False

        with self.assertRaises(StopIteration):
            it = iter(xrange(1, 10))
            n = 1
            while True:
                self.assertEqual(next(it), n)
                n += 1
                keep = True

        n = 1
        for v in xrange(1, 10, 2):
            self.assertEqual(v, n)
            n += 2
            keep = True
    '''

    def test_iterator_py2(self):
        """
        ‘迭代器’即一个包含‘__next__’方法类的对象，通过‘__next__’方法可以迭代所需的每一个值
        可以通过对象的‘__iter__’方法来获取一个迭代器对象

        iter(obj) 调用一个对象的‘__iter__’方法，返回一个迭代器对象
        next(iterator) 调用迭代器对象的‘__next__’方法，返回一个值
        """

        class List:
            """
            包含‘__iter__’方法的类可以获取迭代器对象，‘__iter__’方法返回迭代器对象
            """

            def __init__(self):
                self.__list = []

            def append(self, o):
                self.__list.append(o)

            def __iter__(self):
                return Iterator(self.__list)

        class Iterator:
            """
            包含‘__next__’方法的类作为迭代器对象，‘__next__’方法每调用一次返回下一个值
            """

            def __init__(self, l):
                self.__list = l
                self.__index = 0

            def next(self):
                if self.__index == len(self.__list):
                    raise StopIteration()
                o = self.__list[self.__index]
                self.__index += 1
                return o

        lst = List()
        lst.append(1)
        lst.append(2)
        lst.append(3)

        n = 1
        it = iter(lst)
        with self.assertRaises(StopIteration):
            while True:
                self.assertEqual(next(it), n)
                n += 1

        n = 1
        for x in lst:
            self.assertEqual(x, n)
            n += 1

    '''
    @skip('only for py3')
    def test_iterator_py3(self):
        """
        ‘迭代器’即一个包含‘__next__’方法类的对象，通过‘__next__’方法可以迭代所需的每一个值
        可以通过对象的‘__iter__’方法来获取一个迭代器对象

        iter(obj) 调用一个对象的‘__iter__’方法，返回一个迭代器对象
        next(iterator) 调用迭代器对象的‘__next__’方法，返回一个值
        """

        class List:
            """
            包含‘__iter__’方法的类可以获取迭代器对象，‘__iter__’方法返回迭代器对象
            """

            def __init__(self):
                self.__list = []

            def append(self, o):
                self.__list.append(o)

            def __iter__(self):
                return Iterator(self.__list)

        class Iterator:
            """
            包含‘__next__’方法的类作为迭代器对象，‘__next__’方法每调用一次返回下一个值
            """

            def __init__(self, l):
                self.__list = l
                self.__index = 0

            def __next__(self):
                if self.__index == len(self.__list):
                    raise StopIteration()
                o = self.__list[self.__index]
                self.__index += 1
                return o

        lst = List()
        lst.append(1)
        lst.append(2)
        lst.append(3)

        n = 1
        it = iter(lst)
        with self.assertRaises(StopIteration):
            while True:
                self.assertEqual(next(it), n)
                n += 1

        n = 1
        for x in lst:
            self.assertEqual(x, n)
            n += 1
    '''

    def test_iterator_imap(self):
        """
        itertools.imap(function, sequence) -> iterator
        用于以‘sequence’对象指定的集合作为参数，依次调用‘function’参数指定的函数/方法，返回每次调用结果组成的集合
        """
        s = 'test.jpg'
        # 重复调用‘s.endswith’方法，并依次传入 '.jpg', '.bmp', '.png' 做为参数
        results = list(itertools.imap(s.endswith, ['.jpg', '.bmp', '.png']))
        self.assertTrue(results[0])
        self.assertFalse(results[1])
        self.assertFalse(results[2])

        # 范例，判断文件名的扩展名
        def end_with(s, *endings):
            return True in itertools.imap(s.endswith, endings)

        file_names = 'test.jpg,test.png,test.bmp,test.txt'
        file_exts = ['.jpg', '.bmp', '.png']
        expected_results = [True, True, True, False]

        for name, ok in zip(file_names.split(','), expected_results):
            self.assertEqual(end_with(name, *file_exts), ok)
