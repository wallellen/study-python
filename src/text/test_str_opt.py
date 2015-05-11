# coding=utf-8
from functools import reduce
import operator

from unittest import TestCase
import io
import re


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
        """
        字符串连接有如下方法：
        1. 利用‘+’运算符
        2. 利用 str::join(str_list) 方法
        3. 利用字符串格式化
        4. 利用其它集合操作方法（如 reduce 方法）

        字符串的‘*’运算符表示字符串重复的次数
        'abc' * 3 的结果为'abcabcabc'
        """
        str1 = 'Hello'
        str2 = 'World'
        self.assertEqual(str1 + ' ' + str2, 'Hello World')
        self.assertEqual(' '.join((str1, str2)), 'Hello World')
        self.assertEqual('%s %s' % (str1, str2), 'Hello World')
        self.assertEqual(reduce(operator.add, (str1, ' ', str2)), "Hello World")

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

    def test_trim(self):
        """
        str::strip(char)    去除字符串两端的指定字符
        str::lstrip(char)   去除字符串左边的指定字符
        str::rstrip(char)   去除字符串右边的指定字符
        """
        s = '    abcd    '
        self.assertEqual(s.strip(), 'abcd')
        self.assertEqual(s.lstrip(' '), 'abcd    ')
        self.assertEqual(s.rstrip(), '    abcd')

    def test_reverse(self):
        """
        翻转字符串：
        1. 对于任何序列对象（包括字符串），seque[::-1]表示翻转序列，所以 'abc'[::-1] 为 'cba'
        2. 对于任何 list 集合，可以使用 reversed(list) 翻转集合
        """
        s = 'abcdef'
        l = s[::-1]
        self.assertEqual(l, 'fedcba')

        l = ''.join(reversed(s))
        self.assertEqual(l, 'fedcba')

        s = 'abc def'
        l = ' '.join([e[::-1] for e in re.split(r'\s+', s)])
        self.assertEqual(l, 'cba fed')

    def test_translate(self):
        """
        str::translate(dict) 方法根据一个字符编码对应表，将字符串中指定的编码替换为目标编码
        str::maketrans(str1, str2) 方法返回一个dict对象，即str1中的每个字符对应str2的每个字符，用于translate方法
        """

        def to_lower1(s):
            # 字符编码对应表，将大写字母的编码对应到小写字母编码上
            tab = {ord('A'): ord('a'), ord('B'): ord('b'), ord('C'): ord('c')}
            # 执行转换，相当于将大写字母转为小写字母
            return s.translate(tab)

        s = 'ABC'
        self.assertEqual(to_lower1(s), 'abc')

        def to_lower2(s):
            # 字符编码对应表，将大写字母的编码对应到小写字母编码上
            tab = str.maketrans('ABCD', 'abcd')
            # 执行转换，相当于将大写字母转为小写字母
            return s.translate(tab)

        s = 'ABC'
        self.assertEqual(to_lower2(s), 'abc')

    def test_substring(self):
        """
        求子字符串，分割字符串
        1. list 方法可以将字符串分割为每字符串一个字符的子字符串集合
        2. 切片方法可以获取指定范围的子字符串
        3. LC切片法可以获取更复杂的子字符串集合
        """
        s = '一二三四五六七八九零'

        # 将字符串转为每字符串一个字符的集合
        chars = list(s)
        self.assertEqual(len(chars), len(s))
        self.assertEqual(chars[0], s[0])
        self.assertEqual(chars[-1], s[-1])

        self.assertEqual(s[1:5], '二三四五')  # 利用切片法获取指定范围的子字符串

        fivers = [s[k:k + 2] for k in range(0, len(s), 2)]  # 利用LC切片发获取每字符串两个字符的集合
        self.assertEqual(fivers[0], '一二')
        self.assertEqual(fivers[1], '三四')
        self.assertEqual(fivers[2], '五六')
        self.assertEqual(fivers[3], '七八')
        self.assertEqual(fivers[4], '九零')

        cuts = [2, 5, 9]
        zipped = list(zip([0] + cuts, cuts + [len(s)]))
        self.assertListEqual(zipped, [(0, 2), (2, 5), (5, 9), (9, 10)])
        fivers = [s[i:j] for i, j in zipped]
        self.assertEqual(fivers[0], '一二')
        self.assertEqual(fivers[1], '三四五')
        self.assertEqual(fivers[2], '六七八九')
        self.assertEqual(fivers[3], '零')
