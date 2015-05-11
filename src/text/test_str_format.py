# coding=utf-8

from unittest import TestCase


class TestStringFormat(TestCase):

    def test_builtin_format(self):
        result = '%s, %s, %s' % ('a', 'b', 'c')
        self.assertEqual(result, 'a, b, c')

    def test_by_list_arguments(self):
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
        result = '{latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
        self.assertEqual(result, '37.24N, -115.81W')

        coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
        result = '{latitude}, {longitude}'.format(**coord)
        self.assertEqual(result, '37.24N, -115.81W')

    def test_by_complex_number(self):
        c = 3 - 5j
        result = 'complex {0}. real part {0.real}. imaginary part {0.imag}.'.format(c)
        self.assertEqual(result, 'complex (3-5j). real part 3.0. imaginary part -5.0.')

    def test_by_object(self):
        class Point():
            def __init__(self, x, y):
                self.x, self.y = x, y

            def __str__(self):
                return 'Point({this.x}, {this.y})'.format(this=self)

        self.assertEqual(str(Point(4, 2)), 'Point(4, 2)')

    def test_by_multi_list(self):
        coord = ((3, 5), (6, 8))
        result = 'X1:{0[0]};Y1:{0[1]};X2:{1[0]},Y2:{1[1]}'.format(*coord)
        self.assertEqual(result, 'X1:3;Y1:5;X2:6,Y2:8')

    def test_by_use_repr_or_str(self):
        # '!r' means use repr() to convert string, '!s' means use str()
        result = "{!r},{!s}".format('test1', 'test2')
        self.assertEqual(result, "'test1',test2")

    def test_control_format(self):
        result = '{:<30}'.format('A')
        self.assertEqual(result, 'A                             ')

        result = '{:>30}'.format('A')
        self.assertEqual(result, '                             A')

        result = '{:^30}'.format('A')
        self.assertEqual(result, '              A               ')

        result = '{:*^30}'.format('A')
        self.assertEqual(result, '**************A***************')

    def test_number_sign(self):
        result = '{:+f};{:+f}'.format(3.14, -3.14)  # show it always
        self.assertEqual(result, '+3.140000;-3.140000')

        result = '{: f};{: f}'.format(3.14, -3.14)  # show a space for positive numbers
        self.assertEqual(result, ' 3.140000;-3.140000')

        result = '{:-f};{:-f}'.format(3.14, -3.14)  # show only the minus -- same as '{:f}; {:f}'
        self.assertEqual(result, '3.140000;-3.140000')

    def test_integer_radix(self):
        # format also supports binary numbers
        result = 'int:{0:d};hex:{0:x};oct:{0:o};bin:{0:b}'.format(42)
        self.assertEqual(result, 'int:42;hex:2a;oct:52;bin:101010')

        # with 0x, 0o, or 0b as prefix:
        result = 'int:{0:d};hex:{0:#x};oct:{0:#o};bin:{0:#b}'.format(42)
        self.assertEqual(result, 'int:42;hex:0x2a;oct:0o52;bin:0b101010')

    def test_number_format(self):
        result = '{:,}'.format(1234567890)
        self.assertEqual(result, '1,234,567,890')

    def test_number_percent(self):
        result = '{:.2%}'.format(19.5 / 22)
        self.assertEqual(result, '88.64%')

    def test_datetime(self):
        import datetime

        d = datetime.datetime(2010, 7, 4, 12, 15, 58)
        result = '{:%Y-%m-%d %H:%M:%S}'.format(d)
        self.assertEqual(result, '2010-07-04 12:15:58')

    def test_format(self):
        expected = ('left<<<<<<<<<<<<', '^^^^^center^^^^^', '>>>>>>>>>>>right')
        n = 0
        for align, text in zip('<^>', ['left', 'center', 'right']):
            result = '{0:{fill}{align}16}'.format(text, fill=align, align=align)
            self.assertEqual(result, expected[n])
            n += 1

        octets = [192, 168, 0, 1]
        result = '{:02X}{:02X}{:02X}{:02X}'.format(*octets)
        self.assertEqual(result, 'C0A80001')

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
        for num in range(5, 12):
            row = []
            for base in 'dXob':
                row.append('{0:{width}{base}}'.format(num, base=base, width=width))
            actual.append(tuple(row))
        self.assertEqual(tuple(actual), expected)