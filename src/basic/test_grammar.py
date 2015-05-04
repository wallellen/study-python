# coding=utf-8
import random
from unittest import TestCase

TEST_VAR = 'GLOBAL'


class TestGrammar(TestCase):
    def test_batch_assign(self):
        """
        批量赋值；
            可以通过python的语言特性为变量批量赋值，有两种方式：
        1. 通过逗号表达式为若干变量批量赋值；
        2. 通过list或tuple为若干变量批量赋值
        """
        a, b, c = 12, 13, 14
        self.assertEqual(a, 12)
        self.assertEqual(b, 13)
        self.assertEqual(c, 14)

        l = [121, 131, 141]
        a, b, c = l
        self.assertEqual(a, 121)
        self.assertEqual(b, 131)
        self.assertEqual(c, 141)

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

    def test_type_conversion(self):
        a = 100.200
        self.assertEqual(a, float(a))
        self.assertNotEqual(a, int(a))

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

    def test_branch(self):
        a = 10
        b = 20

        if a > b:
            c = a
        elif a < b:
            c = b
        else:
            c = 0

        self.assertEqual(c, a if a > b else b)

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

    def test_yield(self):
        """
        yield相当于一个“迭代发生器”，
            在函数（方法）中使用yield，则该函数表示一个范围（range），可以通过迭代的方式来访问。
        但yield保证每次迭代才会生成一个值（而非生成整个序列），所以比较节省内存。
            所以一般情况下，yield关键字位于一个循环内部，通过某种规则来产生迭代中的某个值
        """

        def xrange(min, max):
            while min < max:
                yield min
                min += 1

        self.assertListEqual(list(xrange(10, 20)), list(range(10, 20)))

        it = xrange(10, 20).__iter__()
        n = 10
        try:
            while True:
                self.assertEqual(n, it.__next__())
                n += 1
        except StopIteration:
            pass

        it = iter(xrange(10, 20))
        n = 10
        try:
            while it:
                self.assertEqual(n, next(it))
                n += 1
        except StopIteration:
            pass

    def test_lambda(self):
        """
        lambda的本质就是匿名函数，但在python中有如下要求：
        1. 用lambda关键字表示表达式开始；
        2. lambda之后可以包含0到多个参数，参数用,分隔；
        3. 所有参数之后有一个:，该:左边是lambda声明，右边是lambda内容；
        4. lambda中必须且只能包含一个表达式，整个lambda的值即该表达式的值。
        """
        fn = lambda a, b: a if a > b else b
        self.assertEqual(fn(10, 20), 20)

    def test_list_args(self):
        """
        通过 *name 表示的参数项可以传入任意多个参数
        对于 func(*args)，则
            func(1, 2, 3, 4, 5) 表示传入5个不定参数，都保存在 args 这个list对象中
            func([1, 2, 3, 4, 5]) 则表示传入了一个参数，参数类型是list类型
            令 l = [1, 2, 3, 4, 5]，则 func(*l) 表示传入了5个不定参数
        """

        def tuple_args(*args):
            return args

        expected_list = (1, 2, 3, 4, 5)
        self.assertEqual(tuple_args(1, 2, 3, 4, 5), expected_list)  # 传入5个参数，相当于5项的list
        self.assertEqual(tuple_args(expected_list), (expected_list,))  # 传入1个参数，相当于1项的list
        self.assertEqual(tuple_args(*expected_list), expected_list)  # 传入5个参数，相当于5项的list

    def test_map_args(self):
        """
        通过 **name 表示参数可以为任意个数，且组成一个dict对象，此时传参必须显式传递参数名
        对于 func(**name) 则
            func(a=1, b=2) 相当于传入两个参数，组成 {'a': 1, 'b': 2} 的dict对象
            func({'a': 1, 'b': 2}) 不正确，因为只相当于传入一个参数，且没有显式设置参数名
            令 d = {'a': 1, 'b': 2}, 则 func(**d) 相当于传入两个参数，组成 {'a': 1, 'b': 2} 的dict对象
        """

        def dict_args(**kwargs):
            return kwargs

        def list_dict_args(**kwargs):
            return sorted(kwargs.keys()), sorted(kwargs.values())

        expected_map = {'a': 1, 'b': 2, 'c': 3}
        actual_map = dict_args(a=1, b=2, c=3)
        self.assertDictEqual(expected_map, actual_map)

        with self.assertRaises(TypeError):
            dict_args(expected_map)

        actual_map = dict_args(**expected_map)
        self.assertDictEqual(actual_map, expected_map)

        list_key, list_value = list_dict_args(**expected_map)
        self.assertEqual(list_key, ['a', 'b', 'c'])
        self.assertEqual(list_value, [1, 2, 3])

    def test_global_var(self):
        """
        要在方法内部使用全局变量，需要：
        1. 在模块文件中声明全局变量
        2. 使用 global 关键字在方法内部声明全局变量
        """
        global TEST_VAR
        self.assertEqual(TEST_VAR, 'GLOBAL')

        TEST_VAR = 'LOCAL'
        self.assertEqual(TEST_VAR, 'LOCAL')

    @staticmethod
    def outside(x):
        def inside(y):
            """
            nonlocal 关键字指定某个变量非当前函数（方法）的局部变量
            """
            nonlocal x
            x += 1
            return x, y

        return inside

    def test_nested_function(self):
        """
        nonlocal 关键字，参考 outside 方法
        """
        func = TestGrammar.outside(10)
        x, y = func(20)
        self.assertEqual(x, 11)
        self.assertEqual(y, 20)

        x, y = func(20)
        self.assertEqual(x, 12)
        self.assertEqual(y, 20)

    def test_with(self):
        """
        with 关键字常用于自动释放资源
        如果一个类具备 __enter__, __exit__ 方法，则这个类的对象可以被 with 引用
        1. 当进入 with 代码块时，对象的 __enter__ 方法被自动调用一次
        2. 当 with 块结束时，__exit__方法被自动调用一次

        with 的一般格式为：
            with obj:
                code

            with obj as val:    这里使用了as，将把对象__enter__方法的返回值赋予val变量
                code
        """

        class Test:
            def __init__(self, throwable=True):
                self.count = 0
                self.__throwable = throwable

            def __enter__(self):
                self.count += 1
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.count -= 1

                # 如果在 with 块中引发了异常，则下述代码生效
                self.exception_type = exc_type
                self.exception = exc_val
                self.traceback = exc_tb
                return not self.__throwable  # return True if not raise the Exception

        with Test() as t:
            self.assertEqual(t.count, 1)
        self.assertEqual(t.count, 0)
        self.assertIsNone(t.exception)
        self.assertIsNone(t.exception_type)
        self.assertIsNone(t.traceback)

        exception = None
        try:
            with Test() as t:
                self.assertEqual(t.count, 1)
                raise Exception
        except Exception as e:
            exception = e
            self.assertEqual(t.count, 0)
            self.assertEqual(t.exception, exception)
            self.assertEqual(t.exception_type, Exception)
            self.assertIsNotNone(t.traceback)
        self.assertIsNotNone(exception)

        exception = None
        try:
            with Test(False) as t:
                self.assertEqual(t.count, 1)
                raise Exception
        except Exception as e:
            exception = e
        self.assertIsNone(exception)
