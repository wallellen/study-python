# coding=utf-8
import os
from random import Random
from unittest import TestCase
import functools

TEST_GLOBAL_VAR = 100
TEST_VAR = 'GLOBAL'


class TestBuildInFunctions(TestCase):
    def assertListContains(self, list_res, list_to):
        """
        检测一个list集合是否完全包含另一个list集合
        :param list_res: 假定包含另一个list集合的集合
        :param list_to: 假定被包含的list集合
        :return: 如果条件成立则返回True，否则引发断言
        """
        for a in list_res:
            if a not in list_to:
                self.fail('{0} is not in {1}'.format(a, list_to))
        return True

    def test_abs(self):
        """
        测试取绝对值函数

        abs(num)
        """
        a = -10
        b = 10
        self.assertEqual(abs(a), b)

    def test_all(self):
        """
        测试集合中是否所有元素都能表达True

        all(iterator)
        """
        _list = (1, 0, 1, 2, 3)  # 集合中包含False值的情况
        self.assertFalse(all(_list))

        _list = (1, 2, 3, 4, 5)  # 集合中只包含True值的情况
        self.assertTrue(all(_list))

        self.assertTrue(all([]))  # 集合为空集的情况

    def test_any(self):
        """
        测试集合中是否有任意值可表示True

        any(iterator)
        """
        _list = (1, 0, 1, 2, 3)  # 有某个值表示True的情况
        self.assertTrue(any(_list))

        _list = (0, 0, 0, 0, 0)  # 全部值都表示False的情况
        self.assertFalse(any(_list))

    def test_ascii(self):
        """
        字符串字符转为ASCII编码，结果中以\\u开头表示UNICODE编码

        ascii(str)->string  this string contain
        """
        print(ascii('测试'))
        self.assertEqual(ascii('测试'), "'\\u6d4b\\u8bd5'")

    def test_bin(self):
        """
        数字转为二进制字符串（结果中以0b开头）

        bin(num)->string
        """
        self.assertEqual(bin(3), '0b11')

    def test_bool(self):
        """
        依照转换规则，将任意类型转换为boolean类型
        """
        self.assertEqual(bool(0), False)
        self.assertEqual(bool('x'), True)

    def test_byte_and_bytearray(self):
        """
        通过bytearray函数，将字符串按照制定编码转换为byte集合
        通过bytes函数，将数字集合转为byte集合
        通过str函数将比特集合转为制定编码的字符串
        通过bytearray::decode方法，可以将bytearray对象转为特定编码的字符串
        """
        expected_bytes = (72, 101, 108, 108, 111, 32, 112, 121, 116, 104, 111, 110)
        ba = bytearray('Hello python', 'utf-8')
        self.assertTupleEqual(tuple(ba), expected_bytes)

        print(bytes(expected_bytes))
        # compare the result
        self.assertEqual(str(bytes(expected_bytes), 'utf-8'), ba.decode('utf-8'))

    def test_callable(self):
        """
        如果一个类中包含__call__方法，则该类的对象可以以类似于函数方式使用
        callable函数可以检测一个对象是否包含__call__方法
        """

        class NotCallable:
            pass

        class Callable:
            def __call__(self, *args, **kwargs):
                return 'callable,' + str(args[0]) + ',' + kwargs['name']

        a = NotCallable()
        self.assertFalse(callable(a))  # 不包含__call__方法的对象

        a = Callable()
        self.assertTrue(callable(a))  # 包含__call__方法的对象

        # 通过对象调用__call__方法，就如同对象是一个方法
        self.assertEqual(a(100, name='alvin'), 'callable,100,alvin')

    def test_chr(self):
        """
        chr方法可以将一个ASCII编码值（数字）转为对应的字符串（包含一个字符）
        """
        self.assertEqual(chr(97), 'a')

    def test_classmethod(self):
        """
        classmethod注解表示一个方法的归属是类，而非对象，具体区别在于：
            方法的第一个参数指向所属的类，而非一个对象实例
        """

        class ClassMethod:
            value = 0

            @classmethod
            def method(cls, num):  # 类方法、对象方法和静态方法的区别就在于第一个参数
                return str(num) + ' ' + str(cls.value)

        ClassMethod.value = 100
        self.assertEqual("123 100", ClassMethod.method(123))  # 访问类方法，无需借助对象

    def test_compile(self):
        """
        compile方法可以将字符串表示的python代码进行编译，从而执行
        """
        code = '1 + 1'  # 待编译的表达式（字符串表示）
        compile_code = compile(code, '', 'eval')  # 将表达式进行编译，返回值指向编译结果
        self.assertEqual(eval(compile_code), 2)  # 执行编译结果，得到返回值

        code = 'x = 1 + 1'  # 待编译的语句（字符串表示）
        compile_code = compile(code, '', 'exec')  # 将语句进行编译，返回值指向编译结果
        exec(compile_code)  # 执行编译结果
        print(eval('x'), 2)  # 执行表达式，获取x变量的值

    def test_delattr(self):
        """
        delattr函数可以从对象中删除一个属性，注意：这个属性必须是“成员变量”，而不是“属性方法”

        delattr(obj, 'property name')
        """

        class Test:
            def __init__(self):
                self.x = 100
                self.y = 200
                self.__v = 300

            @property
            def v(self):
                """
                定义属性方法，通过签名'v'获取self.__v的值
                """
                return self.__v

            @v.setter
            def v(self, val):
                """
                为属性方法定义对应的set方法，通过签名'v'设置self.__v的值
                """
                self.__v = val

            @v.deleter
            def v(self):
                """
                为属性方法定义对应的delete方法，通过签名'v'删除self.__v的值
                可以通过'del obj.v'或delattr(obj, 'v')来删除self.__v属性
                """
                del self.__v

        t = Test()
        with self.assertRaises(AttributeError):  # 'AttributeError' exception expected
            delattr(t, 'x')  # delete attribute 'x' from 't' object， or use del t.x instead
            print(t.x)  # no attribute 'x' in 't', exception caused

        with self.assertRaises(AttributeError):
            del t.v  # delete attribute 'v' from 't' object, or use del t.v instead
            print(t.v)  # no attribute 'x' in 't', exception caused

    def test_dict(self):
        """
        dict函数的作用是
        :return:
        """
        expected_dict = {'a': 1, 'b': 2, 'c': 3}

        # make dictionary by arguments
        _dict = dict(a=1, b=2, c=3)
        self.assertDictEqual(_dict, expected_dict)

        # make dictionary by mapped values and arguments
        _dict = dict(zip(('a', 'b'), (1, 2)), c=3)
        self.assertDictEqual(_dict, expected_dict)

        # make dictionary by mapped arrays and arguments
        _dict = dict([('a', 1), ('b', 2)], c=3)
        self.assertDictEqual(_dict, expected_dict)

        # make dictionary by other dictionary and arguments
        _dict = dict({'a': 1, 'b': 2}, c=3)
        self.assertDictEqual(_dict, expected_dict)

    def test_dir(self):
        class Test1:
            def __dir__(self):
                return ['a', 'b', 'c']

        class Test2:
            def __init__(self):
                self.a = 'a'
                self.b = 'b'
                self.c = 'c'

        t = Test1()
        self.assertListEqual(['a', 'b', 'c'], dir(t))

        t = Test2()
        self.assertListContains(['a', 'b', 'c'], dir(t))

    def test_divmod(self):
        a = 3
        b = 2
        # Result is a list
        self.assertEqual(divmod(a, b), (a // b, a % b))

    def test_enumerate(self):
        nums = ['one', 'two', 'three', 'four']
        self.assertTupleEqual(tuple(enumerate(nums)), ((0, 'one'), (1, 'two'), (2, 'three'), (3, 'four')))

        i = 0
        for num in enumerate(nums):
            self.assertEqual(num, (i, nums[i]))
            i += 1

    def test_eval(self):
        exec('x = 1')
        self.assertEqual(eval('x + 1'), 2)  # execute the express by string

    def test_exec(self):
        exec('''x = 0
for i in range(0, 10):
    x += 1
print(x)''')
        self.assertEqual(eval('x'), 10)

    def test_filter(self):
        a = [1, 2, 3, 4, 5]
        self.assertTupleEqual(tuple(filter(lambda it: it % 2 == 0, a)), (2, 4))

    def test_float(self):
        a = 10
        self.assertEqual(type(a), int)
        self.assertEqual(type(float(a)), float)

    def test_format(self):
        self.assertEqual(format(123, '.2f'), '123.00')

        class Test:
            def __format__(self, format_spec):
                return {
                    'm': lambda: 'format by \'m\'',
                    'n': lambda: 'format by \'n\''
                }[format_spec]()

        t = Test()
        self.assertEqual(format(t, 'm'), 'format by \'m\'')

    def test_getattr(self):
        class Test:
            TEST_VAL = 10

            def __init__(self):
                self.x = 100

        t = Test
        self.assertEqual(getattr(t, 'TEST_VAL'), 10)

        t = Test()
        self.assertEqual(getattr(t, 'x'), 100)

    def test_globals(self):
        global_dict = globals()
        self.assertTrue('TEST_GLOBAL_VAR' in global_dict.keys())
        self.assertEqual(global_dict['TEST_GLOBAL_VAR'], TEST_GLOBAL_VAR)

    def test_hasattr(self):
        class Test:
            TEST_VAL = 10

            def __init__(self):
                self.x = 100

        t = Test
        self.assertTrue(hasattr(t, 'TEST_VAL'))
        t = Test()
        self.assertTrue(hasattr(t, 'x'))

    def test_hash(self):
        class Test:
            def __hash__(self):
                return 1234567

        t = Test()
        self.assertEqual(hash(t), 1234567)

    def test_hex(self):
        # convert number to hex string
        self.assertEqual(hex(255), '0xff')

    def test_int(self):
        val = int(0xFF)
        self.assertEqual(val, 255)

        class Test:
            def __init__(self, num):
                self.__num = num

            def __int__(self):
                return self.__num * 10

            @property
            def number(self):
                return self.__num

        t = Test(10)
        self.assertEqual(t.number, 10)
        self.assertEqual(int(t), 100)

    def test_isinstance(self):
        s = 'Hello'
        self.assertTrue(isinstance(s, str))

        s = None
        self.assertFalse(isinstance(s, str))
        self.assertTrue(isinstance(s, object))

    def test_issubclass(self):
        self.assertTrue(issubclass(str, object))

        class Base:
            pass

        class Child(Base):
            pass

        self.assertTrue(issubclass(Child, Base))

    def test_iter(self):
        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                self.__cur = self.__min
                return self

            def __next__(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                _cur = self.__cur
                self.__cur += 1
                return _cur

        t = Test(1, 10)
        it = iter(t)
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)

        val = 0
        with self.assertRaises(StopIteration):
            while True:
                val = next(it)
        self.assertEqual(val, 9)

        val = 1
        for n in t:
            self.assertEqual(n, val)
            val += 1

    def test_len(self):
        s = '12345'
        self.assertEqual(len(s), 5)

        class Test:
            def __init__(self, _len):
                self.__len = _len

            def __len__(self):
                return self.__len

        t = Test(10)
        self.assertEqual(len(t), 10)

    def test_list(self):
        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                self.__cur = self.__min
                return self

            def __next__(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                _cur = self.__cur
                self.__cur += 1
                return _cur

        t = Test(1, 6)
        self.assertListEqual(list(t), [1, 2, 3, 4, 5])

    def test_locals(self):
        x = 100
        _dict = locals()
        self.assertTrue('x' in _dict.keys())
        self.assertEqual(_dict['x'], 100)

    def test_map(self):
        res = map(lambda x: x % 2 == 0, range(1, 5))
        self.assertTupleEqual(tuple(res), (False, True, False, True))

    def test_max(self):
        lst = (1, 2, 3, 4, 5)
        res = max(lst)
        self.assertEqual(res, 5)

        res = max(lst, key=lambda x: x % 2)
        self.assertEqual(res, 1)  # 1 % 2 = 2

        res = max(1, -2, 3, 4, -5, key=lambda x: -x if x % 2 == 0 else x)
        self.assertEqual(res, 3)  # 3 % 2 = 1 => 3

    def test_memoryview(self):
        memv = memoryview(b'abcde')
        self.assertTupleEqual(tuple(memv), (97, 98, 99, 100, 101))

    def test_min(self):
        lst = (1, 2, 3, 4, 5)
        res = min(lst)
        self.assertEqual(res, 1)

        res = min(lst, key=lambda x: x % 2)
        self.assertEqual(res, 2)  # 2 % 2 = 0

        res = min(1, -2, 3, 4, -5, key=lambda x: -x if x % 2 == 0 else x)
        self.assertEqual(res, -5)  # -5 % 2 = -1 => -5

    def test_next(self):
        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                self.__cur = self.__min
                return self

            def __next__(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                _cur = self.__cur
                self.__cur += 1
                return _cur

        it = iter(Test(1, 5))
        index = 1
        while index < 5:
            self.assertEqual(next(it), index)
            index += 1

    def test_oct(self):
        o = oct(8)
        self.assertEqual(o, '0o10')

    def test_open(self):
        f = None
        try:
            # 'r'	open for reading (default)
            # 'w'	open for writing, truncating the file first
            # 'x'	open for exclusive creation, failing if the file already exists
            # 'a'	open for writing, appending to the end of the file if it exists
            # 'b'	binary mode
            # 't'	text mode (default)
            # '+'	open a disk file for updating (reading and writing)
            # 'U'	universal newlines mode (deprecated)
            f = open('test.txt', 'w', encoding='gbk')
            self.assertTrue(f.writable())
            f.writelines(('line 1\n', 'line 2\n', 'line 3'))
            f.seek(0)
            f.write('LINE')
            f.close()

            f = open('test.txt', 'r', encoding='gbk')
            self.assertEqual(f.readline(), 'LINE 1\n')
            self.assertEqual(f.readline(), 'line 2\n')
            self.assertEqual(f.readline(), 'line 3')
            self.assertEqual(f.readline(), '')  # at the end of line

            f.seek(0)
            s = 'LINE 1\nline 2\nline 3'
            self.assertEqual(f.read(len(s)), s)
            f.seek(0)

            for c in s:
                self.assertEqual(f.read(1), c)
            self.assertEqual('', f.read(1))  # at the end of line
        finally:
            f.close()
            self.assertTrue(f.closed)
            os.remove('test.txt')

    def test_ord(self):
        n = ord('a')
        self.assertEqual('a', chr(n))

    def test_pow(self):
        n = pow(2, 2)
        self.assertEqual(n, 2 ** 2)

        n = pow(2, 2, 2)
        self.assertEqual(n, 2 ** 2 % 2)

    def test_property(self):
        class Test:
            def __init__(self, val):
                self.__value = val

            @property
            def value(self):
                return self.__value

            @value.setter
            def value(self, val):
                self.__value = val

            @value.deleter
            def value(self):
                del self.__value

        t = Test(100)
        self.assertEqual(t.value, 100)

        t.value = 200
        self.assertEqual(t.value, 200)

        del t.value
        with self.assertRaises(AttributeError):
            print(t.value)

    def test_range(self):
        r = range(5)
        self.assertEqual(tuple(r), (0, 1, 2, 3, 4))

        r = range(2, 5)
        self.assertEqual(tuple(r), (2, 3, 4))

        r = range(1, 5, 2)
        self.assertEqual(tuple(r), (1, 3))

    def test_repr(self):
        s = 'test'
        self.assertEqual(s, str(s))
        self.assertEqual(s, eval(repr(s)))

        class Test:
            def __init__(self, val):
                self.__val = val

            def __repr__(self):
                return '{name}:{value}'.format(name=self.class_name, value=self.__val)

            @property
            def class_name(self):
                return self.__class__.__name__

        t = Test(100)
        self.assertEqual(repr(t), 'Test:100')

    def test_reversed(self):
        s = [1, 2, 3]
        self.assertEqual(tuple(reversed(s)), (3, 2, 1))

        class Test:
            def __init__(self, _min, _max, _step=1):
                self.__min, self.__max = _min, _max
                self.__step = _step

            def __iter__(self):
                self.__cur = self.__min
                return self

            def __next__(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                cur = self.__cur
                self.__cur += self.__step
                return cur

            def __reversed__(self):
                return Test(self.__max - 1, self.__min - 1, -self.__step)

        t = Test(1, 5)
        self.assertEqual(tuple(reversed(t)), (4, 3, 2, 1))

    def test_round(self):
        n = round(123.456, 2)
        self.assertEqual(n, 123.46)

        class Test:
            def __init__(self, n):
                self.__n = n

            def __round__(self, digits=None):
                return round(self.__n, digits)

            @property
            def n(self):
                return self.__n

        t = Test(123.456)
        self.assertEqual(round(t, 2), 123.46)

    def test_set(self):
        _set = {1, 1, 2, 2, 3, 3, 4, 4}  # define a set
        self.assertSetEqual(_set, {1, 2, 3, 4})

        _tuple = (1, 1, 2, 2, 3, 3, 4, 4)
        _set = set(_tuple)
        self.assertEqual(_set, {1, 2, 3, 4})

    def test_setattr(self):
        class Test:
            pass

        t = Test()
        setattr(t, 'a', 100)

        self.assertEqual(t.a, 100)
        self.assertEqual(getattr(t, 'a'), 100)

    def test_slice(self):
        _list = (1, 2, 3, 4, 5)
        s = slice(2)
        self.assertEqual(_list[s], _list[:2])

        s = slice(2, 5)
        self.assertEqual(_list[s], _list[2:5])

        s = slice(2, 5, 2)
        self.assertEqual(_list[s], _list[2:5:2])

    def test_sorted(self):
        rand = Random()
        expected_list = [1, 2, 3, 4, 5]
        shuffle_list = expected_list.copy()
        rand.shuffle(shuffle_list)
        self.assertNotEqual(expected_list, shuffle_list)

        shuffle_list = sorted(shuffle_list)
        self.assertEqual(shuffle_list, expected_list)

        shuffle_list = sorted(shuffle_list, key=functools.cmp_to_key(lambda a, b: b - a))
        self.assertEqual(shuffle_list, list(reversed(expected_list)))

        class Test:
            def __init__(self, name, value):
                self.__name, self.__value = name, value

            @property
            def name(self):
                return self.__name

            @property
            def value(self):
                return self.__value

            def __repr__(self):
                return '{0}:{1}'.format(self.__name, self.__value)

        expected_list = [Test('a', 400), Test('b', 300), Test('c', 200), Test('d', 100)]
        shuffle_list = sorted(expected_list, key=lambda t: t.name)
        self.assertEqual(shuffle_list, expected_list)

        expected_list = [Test('a', 400), Test('b', 300), Test('c', 200), Test('d', 100)]
        shuffle_list = sorted(expected_list, key=lambda t: t.value)
        self.assertEqual(shuffle_list, list(reversed(expected_list)))

    def test_sum(self):
        _list = [1, 2, 3, 4, 5]
        expected = 0
        for n in _list:
            expected += n

        self.assertEqual(sum(_list), expected)
        self.assertEqual(sum(_list, 100), expected + 100)

    def test_super(self):
        class Base:
            @property
            def mark(self):
                return 'Base'

        class Child(Base):
            @property
            def mark(self):
                return 'Child'

        class Grand(Child):
            @property
            def mark(self):
                return super().mark

        o = Base()
        self.assertEqual(o.mark, 'Base')

        o = Child()
        self.assertEqual(o.mark, 'Child')
        self.assertEqual(super(Child, o).mark, 'Base')

        o = Grand()
        self.assertEqual(o.mark, 'Child')

    def test_type(self):
        self.assertEqual(type(123), int)
        self.assertEqual(type('Hello'), str)

        # Create a type named 'Test'
        t = type('Test', (object,), dict(VAL=100))
        self.assertEqual(t.VAL, 100)

    def test_vars(self):
        class Test:
            def __init__(self, a, b):
                self.__a, self.__b = a, b

        t = Test(1, 2)

        # Get all variables from an object
        var = vars(t)
        for key in var:
            self.assertEqual(getattr(t, key), var[key])

    def test_zip(self):
        expected_list1 = [1, 2, 3]
        expected_list2 = [4, 5, 6]
        expected_zipped = []
        for n in range(3):
            expected_zipped.append((expected_list1[n], expected_list2[n]))

        actual_zipped = list(zip(expected_list1, expected_list2))
        self.assertEqual(actual_zipped, expected_zipped)

        actual_list1, actual_list2 = zip(*actual_zipped)
        self.assertEqual(list(actual_list1), expected_list1)
        self.assertEqual(list(actual_list2), expected_list2)

    def test_new(self):
        class Singleton:
            def __new__(cls, *args, **kwargs):
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
                return cls._instance

            def __init__(self, value):
                self.__value = value

            @property
            def value(self):
                return self.__value

        singleton1 = Singleton(100)
        singleton2 = Singleton(200)
        self.assertEqual(singleton2.value, 200)
        self.assertEqual(singleton1, singleton2)

    def test_yield(self):
        def xrange(start, stop, step):
            while start < stop:
                yield start
                start += step

        t = tuple(x for x in xrange(1, 10, 2))
        self.assertEqual(t, tuple(range(1, 10, 2)))

    def test_list_args(self):
        def tuple_args(*args):
            return args

        expected_list = (1, 2, 3, 4, 5)
        self.assertEqual(tuple_args(1, 2, 3, 4, 5), expected_list)
        self.assertEqual(tuple_args(*expected_list), expected_list)

    def test_map_args(self):
        def dict_args(**kwargs):
            return kwargs

        def list_dict_args(**kwargs):
            return sorted(kwargs.keys()), sorted(kwargs.values())

        expected_map = {'a': 1, 'b': 2, 'c': 3}
        actual_map = dict_args(a=1, b=2, c=3)
        self.assertDictEqual(expected_map, actual_map)

        list_key, list_value = list_dict_args(**expected_map)
        self.assertEqual(list_key, ['a', 'b', 'c'])
        self.assertEqual(list_value, [1, 2, 3])

    def test_global_var(self):
        global TEST_VAR
        self.assertEqual(TEST_VAR, 'GLOBAL')

        TEST_VAR = 'LOCAL'
        self.assertEqual(TEST_VAR, 'LOCAL')
        self.assertEqual(TEST_VAR, 'LOCAL')

    @staticmethod
    def outside(x):
        def inside(y):
            nonlocal x
            return x, y

        return inside

    def test_nested_function(self):
        func = TestBuildInFunctions.outside(10)
        x, y = func(20)
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)

    def test_with(self):
        class Test:
            def __init__(self):
                self.__count = 0

            @property
            def count(self):
                return self.__count

            def __enter__(self):
                self.__count += 1

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.__count -= 1
                self.__exception_type = exc_type
                self.__exception = exc_val
                self.__traceback = exc_tb
                # return True if not raise the Exception

            @property
            def exception_type(self):
                return self.__exception_type

            @property
            def exception(self):
                return self.__exception

            @property
            def traceback(self):
                return self.__traceback

        t = Test()
        self.assertEqual(t.count, 0)
        with t:
            self.assertEqual(t.count, 1)
        self.assertEqual(t.count, 0)
        self.assertEqual(t.exception, None)
        self.assertEqual(t.exception_type, None)
        self.assertEqual(t.traceback, None)

        t = Test()
        exception = None
        self.assertEqual(t.count, 0)
        try:
            with t:
                self.assertEqual(t.count, 1)
                raise Exception
        except Exception as e:
            exception = e
        finally:
            self.assertEqual(t.count, 0)
            self.assertEqual(t.exception, exception)
            self.assertEqual(t.exception_type, Exception)
            self.assertIsNotNone(t.traceback)