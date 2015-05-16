# coding=utf-8

from unittest import TestCase, skip


class TestBasicIO(TestCase):

    @skip('no need for testing')
    def test_standard_output_py2(self):
        print "Hello"
        print '%d + %d = %d' % (10, 20, 10 + 20)
        print 10, 20, 30

        print 'First', 'Second'

    '''
    @skip('only for py3')
    def test_standard_output_py3(self):
        print("Hello")
        print('%d + %d = %d' % (10, 20, 10 + 20))
        print(10, 20, 30)

        print('First', end=' ')
        print('Second')
    '''

    @skip('no need for testing')
    def test_standard_input(self):
        name = raw_input('Please input your name: ')
        print('Hello %s' % name)