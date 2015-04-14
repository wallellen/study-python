# coding=utf-8

from unittest import TestCase
import io


class TestStringOpt(TestCase):
    def test_length_of_string(self):
        s = '123456'
        self.assertEqual(s.__len__(), 6)
        self.assertEqual(len(s), s.__len__())  # len function will call __len__ method in str class

    def test_string_index(self):
        value = 'ABCDEFG'
        self.assertEqual(value[0], 'A')
        self.assertEqual(value[-1], 'G')

    def test_string_range_index(self):
        value = 'ABCDEFG'
        self.assertEqual(value[1:4], 'BCD')
        self.assertEqual(value[2:], 'CDEFG')
        self.assertEqual(value[:3], 'ABC')
        self.assertEqual(value[-4:], 'DEFG')
        self.assertEqual(value[1:-1:2], 'BDF')

    def test_string_iterator(self):
        value = 'ABCDEFG'
        n = 0
        for c in value:
            self.assertEqual(c, value[n])
            n += 1

    def test_string_to_list(self):
        value = 'ABCDEFG'

        list1 = list(value)
        list2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        self.assertListEqual(list1, list2)

    def test_string_to_tuple(self):
        value = 'ABCDEFG'

        tuple1 = tuple(value)
        tuple2 = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

        self.assertTupleEqual(tuple1, tuple2)

    def test_string_connect(self):
        str1 = 'Hello '
        str2 = 'World'
        str3 = 'Hello World'
        self.assertEqual(str3, str1 + str2)

        str1 = 'xo'
        str2 = 'xoxoxoxo'
        self.assertEqual(str1 * 4, str2)

    def test_string_isdigit(self):
        str1 = '123456'
        str2 = 'a1b2c3'
        self.assertTrue(str1.isdigit())
        self.assertFalse(str2.isdigit())

    def test_string_isalpha(self):
        str1 = '123456'
        str2 = 'abcdef'
        self.assertFalse(str1.isalpha())
        self.assertTrue(str2.isalpha())

    def test_string_isalnum(self):
        s = 'a1b2c3'
        self.assertFalse(s.isdigit())
        self.assertFalse(s.isalpha())
        self.assertTrue(s.isalnum())

        s += '!'
        self.assertFalse(s.isalnum())

    def test_string_upper_lower(self):
        str1 = 'abc'
        str2 = 'ABC'
        self.assertEqual(str1.upper(), str2)
        self.assertEqual(str2.lower(), str1)

    def test_string_substring_count(self):
        str1 = 'abcdabcdabc'
        self.assertEqual(str1.count('bc'), 3)
        self.assertEqual(str1.count('bcd'), 2)
        self.assertEqual(str1.count('bc', 2, -1), 1)

    def test_string_split(self):
        val = '''a
b
c
d
e'''
        lst = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(lst, val.split('\n'))
        self.assertEqual(lst, val.splitlines())
        self.assertEqual(val, '\n'.join(lst))

    def test_character_to_string(self):
        letters = "abcdefg"
        code = 97
        for c in letters:
            self.assertEqual(chr(code), c)
            self.assertEqual(code, ord(c))
            code += 1

    def test_repeat_string(self):
        s = 'a'
        s *= 3
        self.assertEqual(s, 'aaa')

    def test_find_substring(self):
        s = 'xyzxyzxyz'
        n = s.find('xyz')
        self.assertEqual(n, 0)
        n = s.find('xyz', 1)
        self.assertEqual(n, 3)

    def test_replace(self):
        s = 'xyzxyzxyz'
        sr = s.replace('xyz', 'abc')
        self.assertEqual(sr, 'abcabcabc')
        sr = s.replace('xyz', 'abc', 2)
        self.assertEqual(sr, 'abcabcxyz')

    def test_stringio(self):
        with io.StringIO() as sio:
            sio.write('Hello')
            sio.writelines(('1', '2', '3'))
            sio.seek(0)
            s = sio.read()

        self.assertEqual(s, 'Hello123')


