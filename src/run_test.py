# coding=utf-8

import os
import unittest


def list_packages():
    dirs = []
    for item in os.listdir(os.path.abspath('.')):
        if os.path.isdir(item):
            dirs.append(item)
    return dirs


def main():
    for test_dir in list_packages():
        test_suite = unittest.TestLoader().discover(test_dir)
        unittest.TextTestRunner(verbosity=1).run(test_suite)


if __name__ == '__main__':
    main()

'''
def main(*args):
    suite = unittest.TestSuite()
    for t in args:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main('test.test_module',
         'test.test_builtins',
         'test.test_string',
         'test.test_thread',
         'test.test_decorators')
'''