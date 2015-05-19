# coding=utf-8

from unittest import TestCase
import re


class TestRegexp(TestCase):
    """
    注1: flags定义包括：
            re.I：忽略大小写
            re.L：表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
            re.M：多行模式
            re.S：'.'并且包括换行符在内的任意字符（注意：'.'不包括换行符）
            re.U：表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于Unicode字符属性数据库
    """
    def test_match(self):
        """
        re::match(pattern, str, flags=0) 根据正则表达式匹配一个字符串，返回‘True’或‘False’
        注1
        """
        pattern = r'^\(?0\d{2}[\)\-\s]?\d{8}$|^\(?0\d{3}[\)\-\s]?\d{7,8}$|^1\d{10}$'

        self.assertTrue(re.match(pattern, '(029)85556666'))
        self.assertTrue(re.match(pattern, '029-85556666'))
        self.assertTrue(re.match(pattern, '029 85556666'))
        self.assertTrue(re.match(pattern, '(0917)8556666'))
        self.assertTrue(re.match(pattern, '0917-8556666'))
        self.assertTrue(re.match(pattern, '0917 8556666'))
        self.assertTrue(re.match(pattern, '0917 85566661'))
        self.assertTrue(re.match(pattern, '13991300001'))

    def test_findall(self):
        """
        re::findall(pattern, str, flags=0) 返回一个‘list’对象, 包含正则表达式的每一个匹配结果
        注1
        """
        s = '123 456 789'
        result = re.findall(r'\d+', s)
        self.assertEqual(result, s.split(' '))

    def test_finditer(self):
        """
        re::finditer(pattern, str, flags=0) 返回一个迭代器对象, 通过迭代器对象可以得到每一个匹配的‘ Match’对象
        注1
        """
        s = '123 456 789'
        # 获取和每个匹配结果对应的‘Match’对象
        result = re.finditer(r'\d+', s)

        # zip(...) 函数的作用: 将每个‘Match’对象和字符串分割结果的每一项对应
        for m, n in zip(result, s.split(' ')):
            self.assertEqual(m.group(), n)

    def test_split(self):
        s = 'abc    def ghi\tjkl'
        re.split(r'\s+', s)

    def test_sub(self):
        """
        re::sub(pattern, repl, str, count=0, flags=0) 用于通过正则表达式分割字符串‘str’

        count 参数
        """
        s = '123a456b789c'

        lst = []

        def repl(mo):
            self.assertEqual(s[mo.span()[0]:mo.span()[1]], mo.group())
            lst.append(mo.group())

        re.sub(r'\d+', repl, s)
        self.assertEqual(lst, ['123', '456', '789'])

    def test_search(self):
        """
        re.search(pattern, string, flags=0): 在字符串中通过正则表达式进行查找，返回一个'SRE_Match'对象
        flags定义包括：
            re.I：忽略大小写
            re.L：表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
            re.M：多行模式
            re.S：'.'并且包括换行符在内的任意字符（注意：'.'不包括换行符）
            re.U：表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于Unicode字符属性数据库
        """
        s = '10,20,30,50'
        rs = re.search(r'(?P<n1>\d+),(\d+),(?P<n2>\d+),(\d+)', s)

        self.assertTupleEqual(rs.groups(), tuple(s.split(',')))  # groups() 方法，返回匹配结果的所有分组
        self.assertEqual(rs.group(1), s.split(',')[0])  # group(n) 返回第 n 个分组的结果
        self.assertEqual(rs.group(4), s.split(',')[3])

        self.assertEqual(rs.start(), 0)  # start(n) 返回第 n 个分组在源字符串中的起始位置
        self.assertEqual(rs.end(1), s.find('10') + 2)  # end(n) 返回第 n 个分组在源字符串中的结束
        self.assertEqual(rs.group(3), s[rs.start(3):rs.end(3)])

        self.assertDictEqual(rs.groupdict(), {'n1': '10', 'n2': '30'})  # 返回命名分组结果组成的dict

    def test_compile(self):
        """
        re.compile(pattern, flags=0): 把正则表达式语法转化成正则表达式对象
        """
        rx = re.compile(r'(\d{1,3}\.){3}\d')
        self.assertTrue(rx.match('192.168.0.1'))

        self.assertEqual(rx.search('ip:192.168.0.1').start(), 3)
