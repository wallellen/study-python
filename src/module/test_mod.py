# coding=utf-8
import os

from unittest import TestCase

# for py3
from module import mod


class TestModule(TestCase):
    def test_import_module_variables(self):
        from module.mod import version

        self.assertEqual(mod.version, version)

    def test_import_module_functions(self):
        from module.mod import get_version

        mod.version = '2.0'
        self.assertEqual(mod.get_version(), get_version())

    def test_import_module_class(self):
        from module.mod import Mod

        mod1 = Mod(100)
        self.assertEqual(mod1.a, 100)

        mod2 = mod.Mod(200)
        self.assertEqual(mod2.a, 200)

    def test_reload_module_py2(self):
        self.assertEqual(mod.count, 0)

        reload(mod)
        self.assertEqual(mod.count, 1)

    '''
    @skip('only for py3')
    def test_reload_module_py3(self):
        self.assertEqual(mod.count, 0)

        importlib.reload(mod)
        self.assertEqual(mod.count, 1)
    '''

    def test_exec_module(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        exec open(os.path.join(path, 'mod.py')).read()  # load module