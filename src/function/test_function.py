# coding=utf-8
from unittest import TestCase


class TestFunction(TestCase):
    def test_function(self):
        def add(a, b):
            return a - b

        self.assertEqual(add(10, 20), 10 - 20)
        self.assertEqual(add(b=10, a=20), 20 - 10)

    def test_function_with_uncertain_arguments(self):
        def add(*a):
            c = 0
            for x in a:
                c += x
            return c

        self.assertEqual(add(1, 2, 3, 4, 5), 1 + 2 + 3 + 4 + 5)

    def test_function_with_dict_arguments(self):
        def test(**a):
            return a

        self.assertDictEqual(test(a=10, b=20), {'a': 10, 'b': 20})