# coding=utf-8
from functools import reduce
import operator
import string

from unittest import TestCase
import io


class TestStringOpt(TestCase):
    def test_length_of_string(self):
        """
        str::__len__ 方法可以返回字符串的长度，也可以通过 str(string) 函数来调用
        """
        s = '123456'
        self.assertEqual(s.__len__(), 6)
        self.assertEqual(len(s), s.__len__())  # len function will call __len__ method in str class

    def test_string_index(self):
        """
        string[index] 可以获取指定下标的字符串（包含一个字符）
        string[-index] 表示从字符串末尾开始计算下标
        """
        value = 'ABCDEFG'
        self.assertEqual(value[0], 'A')
        self.assertEqual(value[-1], 'G')

    def test_string_range_index(self):
        """
        string[x:y:z] 可以获取字符串的‘切片’（子字符串），x为起始下标，y为终止下标（< y），z为步长
        动态的改变'x,y,z'的值可以产生所谓‘LC切片’，以获得更为复杂的切片结果
        """
        s = '一二三四五六七八九零'
        self.assertEqual(s[1:4], '二三四')  # 利用切片法获取指定范围的子字符串
        self.assertEqual(s[2:], '三四五六七八九零')
        self.assertEqual(s[:3], '一二三')
        self.assertEqual(s[-4:], '七八九零')
        self.assertEqual(s[1:-1:2], '二四六八')

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

    def test_string_iterator(self):
        """
        字符串对象包含迭代器，可以通过‘for’循环进行迭代
        """
        value = 'ABCDEFG'
        n = 0
        for c in value:
            self.assertEqual(c, value[n])
            n += 1

        with self.assertRaises(StopIteration):
            it = iter(value)
            n = 0
            while True:
                self.assertEqual(next(it), value[n])
                n += 1

    def test_string_to_list(self):
        """
        通过‘list’方法可以将字符串转为字符串列表，每项字符串包含一个字符
        """
        value = 'ABCDEFG'

        list1 = list(value)
        list2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.assertListEqual(list1, list2)

    def test_string_to_tuple(self):
        """
        通过‘tuple’方法可以将字符串转为字符串元组，每项字符串包含一个字符
        """
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
        5. 通过‘StringIO’对象连接字符串
        """
        str1 = 'Hello'
        str2 = 'World'
        self.assertEqual(str1 + ' ' + str2, 'Hello World')
        self.assertEqual(' '.join((str1, str2)), 'Hello World')
        self.assertEqual('%s %s' % (str1, str2), 'Hello World')
        self.assertEqual(reduce(operator.add, (str1, ' ', str2)), "Hello World")

        # 利用‘StringIO’开辟内存缓冲区来高效连接字符串
        with io.StringIO() as sio:
            sio.write('Hello')
            sio.writelines(('1', '2', '3'))
            sio.seek(0)
            s = sio.read()
        self.assertEqual(s, 'Hello123')

    def test_string_multi(self):
        """
        字符串的‘*’运算符表示字符串重复的次数
        'abc' * 3 的结果为'abcabcabc'
        """
        str1 = 'xo'
        str2 = 'xoxoxoxo'
        self.assertEqual(str1 * 4, str2)

    def test_string_isdigit(self):
        """
        str::isdigit() 返回字符串是否全部由数字字符组成
        """
        str1 = '123456'
        str2 = 'a1b2c3'
        self.assertTrue(str1.isdigit())
        self.assertFalse(str2.isdigit())

    def test_string_isalpha(self):
        """
        str::isalpha() 返回字符串是否全部由字母（或汉字）字符组成
        """
        str1 = '123456'
        str2 = 'abcdef'
        self.assertFalse(str1.isalpha())
        self.assertTrue(str2.isalpha())

    def test_string_isalnum(self):
        """
        str::isalnum() 结果相当于 str::isalpha() or str::isdigit()
        """
        s = 'a1b2c3'
        self.assertFalse(s.isdigit())
        self.assertFalse(s.isalpha())
        self.assertTrue(s.isalnum())

        s += '!'
        self.assertFalse(s.isalnum())

    def test_string_upper_lower(self):
        """
        str::upper() 将字符串中的小写字母转为大写字母
        str::lower() 将字符串中的大写字母转为小写字母
        """
        str1 = 'abc'
        str2 = 'ABC'
        self.assertEqual(str1.upper(), str2)
        self.assertEqual(str2.lower(), str1)

    def test_string_substring_count(self):
        """
        str::count(string, start, end) 用于计算字符串中子字符串出现的次数
        """
        str1 = 'abcdabcdabc'
        self.assertEqual(str1.count('bc'), 3)
        self.assertEqual(str1.count('bcd'), 2)
        self.assertEqual(str1.count('bc', 2, -1), 1)

    def test_string_split(self):
        """
        str::split(string) 通过指定符号分割字符串
        str::splitlines() 通过换行符号分割字符串
        """
        val = '''a
b
c
d
e'''
        lst = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(lst, val.split('\n'))
        self.assertEqual(lst, val.splitlines())

    def test_char_code_to_string(self):
        """
        chr(num) 将一个字符编码转为该字符的字符串
        ord(char) 将一个包含一个字符的字符串转为该字符对应的编码
        """
        letters = "abcdefg"
        code = 97
        for c in letters:
            self.assertEqual(chr(code), c)
            self.assertEqual(code, ord(c))
            code += 1

    def test_find_substring(self):
        """
        str::find(substr, start, end) 方法在字符串指定范围中（>=start and < end）查找子字符串的开始位置，
        返回‘-1’表示查找失败
        """
        s = 'xyzxyzxyz'

        n = s.find('xyz')
        self.assertEqual(n, 0)

        n = s.find('xyz', 1)
        self.assertEqual(n, 3)

        n = s.find('abc')
        self.assertEqual(n, -1)

    def test_replace(self):
        """
        str::replace(str1, str2, count) 将字符串中‘str1’表示的部分替换为‘str2’表示的部分
        ‘count’表示要替换的次数，默认为‘-1’，表示全部替换
        """
        s = 'xyzxyzxyz'

        sr = s.replace('xyz', 'abc')
        self.assertEqual(sr, 'abcabcabc')

        sr = s.replace('xyz', 'abc', 2)
        self.assertEqual(sr, 'abcabcxyz')

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
        l = s[::-1]  # 利用切片翻转字符串
        self.assertEqual(l, 'fedcba')

        l = ''.join(reversed(s))  # 翻转字符串后（得到翻转后的集合）重新连接字符串
        self.assertEqual(l, 'fedcba')

        s = 'abc def'
        l = ' '.join([e[::-1] for e in s.split(' ')])  # 将字符串切分为子字符串后逐一翻转
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
