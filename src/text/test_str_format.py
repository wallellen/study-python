# coding=utf-8
import string

from unittest import TestCase


class TestStringFormat(TestCase):
    def test_builtin_format(self):
        """
        format_string % (arg1, arg2, ...) 是python格式化字符串的基本方式（语法支持）
        类似于 C 语言，'format_string'中可以包含如'%s', '%d', '%f', '%.2f' 等占位符
        """
        result = '%s, %s, %s' % ('a', 'b', 'c')
        self.assertEqual(result, 'a, b, c')

    def test_by_list_arguments(self):
        """
        format_string.format(arg1, arg2, ...) 通过诸如‘{1}, {2}’等占位符来格式化字符串，其中：
        1. ‘{n}’中的‘n’表示该占位符会被后续的第‘n’个参数取代
        2. 如果不考虑占位符的次序问题，也可以使用‘{}’来表示占位符，每个‘{}’占位符会按顺序被后续参数取代
        """
        result = '{0}, {1}, {2}'.format('a', 'b', 'c')
        self.assertEqual(result, 'a, b, c')

        result = '{}, {}, {}'.format('a', 'b', 'c')
        self.assertEqual(result, 'a, b, c')

        result = '{2}, {1}, {0}'.format('a', 'b', 'c')
        self.assertEqual(result, 'c, b, a')

        result = '{2}, {1}, {0}'.format(*'abc')
        self.assertEqual(result, 'c, b, a')

        result = '{0}{1}{0}'.format('abra', 'cad')
        self.assertEqual(result, 'abracadabra')

    def test_by_dict_arguments(self):
        """
        format_string.format(name1=value1, name2=value2, ...) 可以使用如下形式的占位符：
        1. ‘name1’，‘name2’等可以是任意名称，也是后续参数所必要的参数名；
        2. ‘{name1}’，‘{name2}’等占位符会被后续参数中对应的值取代
        """
        result = '{latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
        self.assertEqual(result, '37.24N, -115.81W')

        coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
        result = '{latitude}, {longitude}'.format(**coord)
        self.assertEqual(result, '37.24N, -115.81W')

    def test_by_complex_number(self):
        """
        format_string.format(n=complex_number) 中，如果参数‘n’的值是一个复数，则：
            {n.real} 表示复数的实部，{n.imaginary} 表示复数的虚部
        """
        c = 3 - 5j
        result = 'complex {c}. real part {c.real}. imaginary part {c.imag}.'.format(c=c)
        self.assertEqual(result, 'complex (3-5j). real part 3.0. imaginary part -5.0.')

    def test_by_object(self):
        """
        format_string.format(a=object1, b=object2, ...) 中，如果'a', 'b'参数对应对象，则：
            占位符‘{a.attrib}’表示使用‘a’参数对应对象的‘attrib’属性进行占位
        """

        class Point():
            def __init__(self, x, y):
                self.x, self.y = x, y

            def __str__(self):
                return 'Point({obj.x}, {obj.y})'.format(obj=self)

        self.assertEqual(str(Point(4, 2)), 'Point(4, 2)')

    def test_by_multi_list(self):
        """
        format_string.format(a=object1, b=object2, ...) 中，如果'a', 'b'参数对应对象，则：
            占位符‘{a.attrib}’表示使用‘a’参数对应对象的‘attrib’属性进行占位
        """
        coord = ((3, 5), (6, 8))
        result = 'X1:{0[0]};Y1:{0[1]};X2:{1[0]},Y2:{1[1]}'.format(*coord)
        self.assertEqual(result, 'X1:3;Y1:5;X2:6,Y2:8')

    def test_by_use_repr_or_str(self):
        """
        对于占位符，‘{!r}’表示使用参数的‘repr()’方法讲参数转为字符串，‘{!s}’表示使用参数的‘str()’方法
        """
        result = "{!r},{!s}".format('test1', 'test2')
        self.assertEqual(result, "'test1',test2")

    def test_control_format(self):
        """
        ‘{:c<n}’一共输出‘n’个字符，不足部分使用‘c’表示的字符在占位符右边补齐；
        ‘{:c>n}’一共输出‘n’个字符，不足部分使用‘c’表示的字符在占位符左边补齐；
        ‘{:c^n}’一共输出‘n’个字符，不足部分使用‘c’表示的字符在占位符两边补齐；
        """
        result = '{:<30}'.format('A')
        self.assertEqual(result, 'A                             ')

        result = '{:>30}'.format('A')
        self.assertEqual(result, '                             A')

        result = '{:^30}'.format('A')
        self.assertEqual(result, '              A               ')

        result = '{:*^30}'.format('A')
        self.assertEqual(result, '**************A***************')

    def test_number_sign(self):
        """
        ‘{:d}’表示占位符将会被一个整数取代（调用参数对象的__int__方法转化）；
        ‘{:f}’表示占位符将会被一个浮点数取代（调用参数对象的__float__方法转化）；
        ‘{:+d}, {:+f}’表示要输出数字的正负号；
        ‘{:-d}, {:-f}’表示要输出数字的负号，正号无需输出；
        ‘{:.nf}’表示保留‘n’位小数；
        """
        result = '{:+f};{:+f}'.format(3.14, -3.14)  # show it always
        self.assertEqual(result, '+3.140000;-3.140000')

        result = '{: f};{: f}'.format(3.14, -3.14)  # show a space for positive numbers
        self.assertEqual(result, ' 3.140000;-3.140000')

        result = '{: .3f};{: .1f}'.format(3.14, -3.14)  # show a space for positive numbers
        self.assertEqual(result, ' 3.140;-3.1')

        result = '{:-f};{:-f}'.format(3.14, -3.14)  # show only the minus -- same as '{:f}; {:f}'
        self.assertEqual(result, '3.140000;-3.140000')

    def test_integer_radix(self):
        """
        ‘{0:d}’表示十进制数字；
        ‘{0:x}’表示十六进制数字；'{0:#x}’表示加上‘0x’前缀；
        ‘{0:o}’表示八进制数字；'{0:#o}’表示加上‘0o’前缀；
        ‘{0:b}’表示二进制数字；'{0:#b}’表示加上‘0b’前缀；
        """
        result = 'int:{0:d};hex:{0:x};oct:{0:o};bin:{0:b}'.format(42)
        self.assertEqual(result, 'int:42;hex:2a;oct:52;bin:101010')

        result = 'int:{0:d};hex:{0:#x};oct:{0:#o};bin:{0:#b}'.format(42)
        self.assertEqual(result, 'int:42;hex:0x2a;oct:0o52;bin:0b101010')

    def test_number_format(self):
        """
        ‘{:,}’表示以三位+逗号的格式输出数字；
        """
        result = '{:,}'.format(1234567890)
        self.assertEqual(result, '1,234,567,890')

    def test_number_percent(self):
        """
        ‘{:.n%}’表示以百分数形式输出数字，‘n’表示小数点后保留的位数；
        """
        result = '{:.2%}'.format(19.5 / 22)
        self.assertEqual(result, '88.64%')

    def test_datetime(self):
        """
        '{:%Y-%m-%d %H:%M:%S}'用于格式化日期型对象
            %Y 四位年份
            %m 两位月份
            %d 两位日期
            %H 两位小时
            %M 两位分钟
            %S 两位秒钟
        """
        import datetime

        d = datetime.datetime(2010, 7, 4, 12, 15, 58)
        result = '{:%Y-%m-%d %H:%M:%S}'.format(d)
        self.assertEqual(result, '2010-07-04 12:15:58')

    def test_format(self):
        expected = ('left************', '*****center*****', '***********right')
        n = 0
        # zip方法将两个集合合并为‘(<, left), (^, center), (>, right)’结果
        # 迭代过程中将集合的每项赋予‘align’以及‘text’变量
        for align, text in zip('<^>', ['left', 'center', 'right']):
            # {text:{fill}{align}16} 占位符表示：
            #   1. 输出‘text’参数的值；
            #   2. 每次输出‘16’个字符，不足使用‘fill’参数对应的字符填充；
            #   3. 填充字符的位置对应‘align’参数；
            result = '{text:{fill}{align}16}'.format(text=text, fill='*', align=align)
            self.assertEqual(result, expected[n])
            n += 1

        expected = (
            ('    5', '    5', '    5', '  101'),
            ('    6', '    6', '    6', '  110'),
            ('    7', '    7', '    7', '  111'),
            ('    8', '    8', '   10', ' 1000'),
            ('    9', '    9', '   11', ' 1001'),
            ('   10', '    A', '   12', ' 1010'),
            ('   11', '    B', '   13', ' 1011')
        )
        actual = []
        width = 5
        # 迭代‘5~11’这一系列数字
        for num in range(5, 12):
            row = []
            # 迭代四个字符
            for base in 'dXob':
                # 输出‘num’参数，通过‘width’参数指定宽度，‘base’参数指定进制
                row.append('{0:{width}{base}}'.format(num, base=base, width=width))
            actual.append(tuple(row))
        self.assertEqual(tuple(actual), expected)

    def test_string_template(self):
        """
        string::Template(str) 返回‘Template’类的对象，其中，‘str’参数是一个含有形如‘$param’参数的字符串
        string::Template::substitute 方法可以通过设置‘参数:值’对应关系来格式化字符串
        """
        template = string.Template('This is $str')

        s = template.substitute({'str': 'Hello'})
        self.assertEqual(s, 'This is Hello')

        s = template.substitute({'str': 123})
        self.assertEqual(s, 'This is 123')