# coding=utf-8
import random
from unittest import TestCase


class TestGrammar(TestCase):
    def test_ternary_operator(self):
        """
        三元运算符：x if exp else y，当exp表达式为True时，值为x，否则为y
        """
        a = 10
        b = 20
        c = a if a > b else b
        self.assertEqual(c, max(a, b))

    def test_or_operator(self):
        """
        x or y表示：当x表示True时，值为x，否则为y（无论y是否表示True）
        """
        a = None
        b = 10
        c = a or b
        self.assertEqual(c, b)

    def test_division(self):
        """
        a / b：保留小数部分
        a // b：小数部分为0
        int(n)：将n转为整数
        float(n)：将n转为浮点数
        """
        a = 5
        b = 2.0
        self.assertEqual(a / b, 2.5)
        self.assertEqual(a // b, 2.0)
        self.assertEqual(int(a / b), 2)
        self.assertEqual(float(int(a / b)), 2.0)

    def test_branch(self):
        a = 10
        b = 20

        if a > b:
            c = a
        elif a < b:
            c = b
        else:
            c = 0

        self.assertEqual(c, 20)

    def test_while_loop(self):
        """
        while exp:
            body
        else:

        当循环正常执行完毕后（未通过break语句终止），则执行else之后的语句（如果存在else子句）
        """
        a = 10
        result = []
        while a > 0:
            if (a % 2) == 0:
                result.append(a)
            a -= 1

        self.assertListEqual(result, [10, 8, 6, 4, 2])

    def test_for_loop(self):
        """
        for n in collection:
            body
        else:

        in之后可以为：列表，元组，范围等集合对象
        """
        import random

        a = 3
        ran = random.randint(0, a)

        result = []
        for i in range(0, a):
            if i == ran:
                break
            result.append(i)
        else:
            self.assertEqual(result, list(range(0, a)))  # loop finish without break

        self.assertEqual(result, list(range(0, ran)))

    def test_string_quotation_marks(self):
        """
        用''包围的字符串中可以包含"字符，同理用""包围的字符串中可以包含'字符
        用\字符在字符串中表示转义字符，可以为\n, \t, \r, \b, \', \" 等
        用'''（或三个双引号）包围的字符串可以包含不可见字符，例如换行，制表符等，无需转义
        """
        str1 = 'Hello'
        str2 = "Hello"
        self.assertEqual(str1, str2)

        str1 = "It's OK, \"Good\""
        str2 = 'It\'s OK, "Good"'
        self.assertEqual(str1, str2)

        str1 = """Hello
World"""
        str2 = 'Hello\nWorld'
        self.assertEqual(str1, str2)

    def test_string_wrap(self):
        """
        在分别位于两行的字符串间使用\字符，可以将这两个字符串连接成一个字符串（用于长字符代码中串换行）
        """
        str1 = "Hello " \
               "World"
        str2 = 'Hello ' \
               'World'
        str3 = 'Hello World'
        self.assertEqual(str1, str2)
        self.assertEqual(str2, str3)

    def test_raw_string(self):
        """
        r（或R）表示raw字符串，即字符串中的所有字符原样表示，即使包含\n这样的转义字符
        """
        str1 = r'Hello\nWorld'
        str2 = 'Hello\nWorld'
        self.assertNotEqual(str1, str2)

    def test_unicode_string(self):
        """
        u（或U）表示字符串中包含UNICODE字符
        """
        str1 = u'测试'
        str2 = '测试'
        self.assertEqual(str1, str2)

    def test_exception(self):
        """
        try:
        except Error as e:
        else:
        finally:

        try 之后为执行代码块，这里可能会抛出异常，通过raise关键字可以抛出指定的异常
        except 之后为异常处理代码块，可以有多个，每个负责捕获一类异常
        else 当所有的except代码块都没有运行时，else之后的代码块会执行一次
        finally 当上述的代码块执行完毕后，finally之后的代码块会执行一次
        """
        throw = random.randint(0, 1) == 0
        cached = False
        regular = False
        try:
            if throw:
                raise Exception('ERROR')
        except Exception as e:
            cached = True
            self.assertEqual(e.args[0], 'ERROR')
        else:
            regular = True
        finally:
            if throw:
                self.assertTrue(cached, 'Exception raised')
            else:
                self.assertTrue(regular, 'No exception cased')

    # noinspection PyBroadException
    def test_with(self):
        """
        with obj:
            ...

        with 关键字用于在异常开始和结束后自动执行代码
        with 关键字之后为一个对象，该对象必须包含__enter__方法和__exit__方法
        当with代码块开始执行时，obj对象的__enter__方法会执行一次
        无论何种原因中断with代码块（执行完毕或抛出异常），obj对象的__exit__方法都一定会执行
        """

        class A:
            def __init__(self):
                self.enter = False
                self.exit = False
                self.__throwable = random.randint(0, 1) == 0

            def __enter__(self):
                self.enter = True

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.exit = True

            def do_something(self):
                if self.__throwable:
                    raise Exception()

        a = A()
        try:
            with a:
                a.do_something()
        except Exception:
            pass

        self.assertTrue(a.enter)
        self.assertTrue(a.exit)
