# coding=utf-8

import os
import unittest
import sys


def list_packages():
    dirs = []
    base_path = os.path.split(os.path.abspath(__file__))[0]
    for item in os.listdir(base_path):
        path = os.path.join(base_path, item)
        if os.path.isdir(path):
            dirs.append(path)
    return dirs


def main():
    success = True
    for test_dir in list_packages():
        test_suite = unittest.TestLoader().discover(test_dir)
        result = unittest.TextTestRunner(verbosity=1).run(test_suite)
        if len(result.failures) > 0:
            success = False
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

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
