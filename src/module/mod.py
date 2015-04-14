# coding=utf-8

version = '1.0'


def get_version():
    return version


class Mod:
    def __init__(self, a):
        self.__a = a

    @property
    def a(self):
        return self.__a


count = count + 1 if 'count' in dir() else 0