# coding=utf-8

import sys
from unittest import TestCase


class TestSystem(TestCase):
    def test_platform(self):
        print(sys.platform)