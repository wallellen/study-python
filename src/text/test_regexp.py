# coding=utf-8

from unittest import TestCase
import re


class TestRegexp(TestCase):
    def test_match(self):
        """
        re::match(pattern, str) 根据正则表达式匹配一个字符串，返回‘True’或‘False’
        """
        pattern = '^\(?0\d{2}[\)\-\s]?\d{8}$|^\(?0\d{3}[\)\-\s]?\d{7,8}$|^1\d{10}$'

        self.assertTrue(re.match(pattern, '(029)85556666'))
        self.assertTrue(re.match(pattern, '029-85556666'))
        self.assertTrue(re.match(pattern, '029 85556666'))
        self.assertTrue(re.match(pattern, '(0917)8556666'))
        self.assertTrue(re.match(pattern, '0917-8556666'))
        self.assertTrue(re.match(pattern, '0917 8556666'))
        self.assertTrue(re.match(pattern, '0917 85566661'))
        self.assertTrue(re.match(pattern, '13991300001'))

    def test_sub(self):
        """
        re::sub(pattern, repl, str) 用于通过正则表达式分割字符串‘str’，每次分割回调‘repl’参数指定的函数
            def repl(mo)
        每次回调可以得到一个分割结果，‘mo.group()’得到分割结果字符串，‘mo.span()’得到分割结果字符串在源字符串中的位置
        """
        s = '123a456b789c'

        lst = []

        def repl(mo):
            self.assertEqual(s[mo.span()[0]:mo.span()[1]], mo.group())
            lst.append(mo.group())

        re.sub(r'\d+', repl, s)
        self.assertEqual(lst, ['123', '456', '789'])
