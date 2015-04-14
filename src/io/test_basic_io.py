from unittest import TestCase


class TestBasicIO(TestCase):
    def test_standard_output(self):
        print("Hello")
        print('%d + %d = %d' % (10, 20, 10 + 20))
        print(10, 20, 30)
        print('First line', end=' ')
        print('Second line')

    def test_standard_input(self):
        uname = input('Please input your name: ')
        print('Hello %s' % uname)