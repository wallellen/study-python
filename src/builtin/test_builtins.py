# coding=utf-8
import os
from random import Random
from unittest import TestCase
import functools

TEST_GLOBAL_VAR = 100


def test():
    pass


class TestBuildInFunctions(TestCase):
    def assertListContains(self, list_res, list_to):
        """
        检测一个list集合是否完全包含另一个list集合
        :type list_res: list
        :type list_to: list
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

    ''' only for py3
    @skip('only for py3')
    def test_ascii(self):
        """
        字符串字符转为ASCII编码，结果中以\\u开头表示UNICODE编码

        ascii(str)->string  this string contain
        """
        self.assertEqual(ascii('测试'), "'\\u6d4b\\u8bd5'")
    '''

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

    def test_byte_and_bytearray_py2(self):
        """
        通过bytearray函数，将字符串按照制定编码转换为byte集合
        通过bytes函数，将数字集合转为byte集合
        通过str函数将比特集合转为制定编码的字符串
        通过bytearray::decode方法，可以将bytearray对象转为特定编码的字符串
        """
        expected_bytes = (72, 101, 108, 108, 111, 32, 112, 121, 116, 104, 111, 110)
        ba = bytearray(u'Hello python', 'utf-8')
        self.assertTupleEqual(tuple(ba), expected_bytes)

        # compare the result
        self.assertEqual(bytearray(expected_bytes).decode('utf-8'), ba.decode('utf-8'))

    '''
    @skip('only for py3')
    def test_byte_and_bytearray_py3(self):
        """
        通过bytearray函数，将字符串按照制定编码转换为byte集合
        通过bytes函数，将数字集合转为byte集合
        通过str函数将比特集合转为制定编码的字符串
        通过bytearray::decode方法，可以将bytearray对象转为特定编码的字符串
        """
        expected_bytes = (72, 101, 108, 108, 111, 32, 112, 121, 116, 104, 111, 110)
        ba = bytearray(u'Hello python', 'utf-8')
        self.assertTupleEqual(tuple(ba), expected_bytes)

        # compare the result
        self.assertEqual(str(bytes(expected_bytes), 'utf-8'), ba.decode('utf-8'))
    '''

    def test_callable_py2(self):
        """
        如果一个类中包含__call__方法，则该类的对象可以以类似于函数方式使用
        callable函数可以检测一个对象是否包含__call__方法
        """

        class NotCallable(object):
            pass

        class Callable(object):
            def __call__(self, *args, **kwargs):
                return 'callable,' + str(args[0]) + ',' + kwargs['name']

        a = NotCallable()
        self.assertFalse(callable(a))  # 不包含__call__方法的对象

        a = Callable()
        self.assertTrue(callable(a))  # 包含__call__方法的对象

        # 通过对象调用__call__方法，就如同对象是一个方法
        self.assertEqual(a(100, name='alvin'), 'callable,100,alvin')

    '''
    @skip('only for py3')
    def test_callable_py3(self):
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
    '''

    def test_chr(self):
        """
        chr方法可以将一个ASCII编码值（数字）转为对应的字符串（包含一个字符）
        """
        self.assertEqual(chr(97), 'a')

    def test_classmethod_py2(self):
        """
        classmethod注解表示一个方法的归属是类，而非对象，具体区别在于：
            方法的第一个参数指向所属的类，而非一个对象实例
        """

        class ClassMethod(object):
            value = 0

            @classmethod
            def method(cls, num):  # 类方法、对象方法和静态方法的区别就在于第一个参数
                return str(num) + ' ' + str(cls.value)

        ClassMethod.value = 100
        self.assertEqual("123 100", ClassMethod.method(123))  # 访问类方法，无需借助对象

    '''
    @skip('only for py3')
    def test_classmethod_py3(self):
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
    '''

    def test_compile_py2(self):
        """
        compile方法可以将字符串表示的python代码进行编译，从而执行
        """
        code = '1 + 1'  # 待编译的表达式（字符串表示）
        compile_code = compile(code, '', 'eval')  # 将表达式进行编译，返回值指向编译结果
        self.assertEqual(eval(compile_code), 2)  # 执行编译结果，得到返回值

        code = 'x = 1 + 1'  # 待编译的语句（字符串表示）
        compile_code = compile(code, '', 'exec')  # 将语句进行编译，返回值指向编译结果

        exec compile_code  # 执行编译结果
        self.assertEqual(eval('x'), 2)  # 执行表达式，获取x变量的值

    '''
    @skip('only for py3')
    def test_compile_py3(self):
        """
        compile方法可以将字符串表示的python代码进行编译，从而执行
        """
        code = '1 + 1'  # 待编译的表达式（字符串表示）
        compile_code = compile(code, '', 'eval')  # 将表达式进行编译，返回值指向编译结果
        self.assertEqual(eval(compile_code), 2)  # 执行编译结果，得到返回值

        code = 'x = 1 + 1'  # 待编译的语句（字符串表示）
        compile_code = compile(code, '', 'exec')  # 将语句进行编译，返回值指向编译结果
        exec(compile_code)  # 执行编译结果

        self.assertEqual(eval('x'), 2)  # 执行表达式，获取x变量的值
    '''

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
            self.assertEqual(t.x, 100)

        with self.assertRaises(AttributeError):
            del t.v  # delete attribute 'v' from 't' object, or use del t.v instead
            self.assertEqual(t.v, 300)  # no attribute 'x' in 't', exception caused

    def test_dict(self):
        """
        dict用于产生一个字典对象，该函数具备任意数量参数，参数名为字典项的key，参数值为字典项的value
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

    def test_dir_py2(self):
        """
        dir函数用于列举一个包、模块或对象中包含的名称（变量名，属性名，方法名等）
        """

        class Test1(object):
            @staticmethod
            def __dir__():
                return ['a', 'b', 'c']

        class Test2(object):
            def __init__(self):
                self.a = 'a'
                self.b = 'b'
                self.c = 'c'

        t = Test1()
        self.assertListEqual(['a', 'b', 'c'], dir(t))

        t = Test2()
        self.assertListContains(['a', 'b', 'c'], dir(t))

    '''
    @skip('only for py3')
    def test_dir_py3(self):
        """
        dir函数用于列举一个包、模块或对象中包含的名称（变量名，属性名，方法名等）
        """

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
    '''

    def test_divmod(self):
        """
        divmod(a, b) 返回一个tuple, 相当于 (a // b, a % b)
        """
        a = 3
        b = 2

        # Result is a list
        self.assertEqual(divmod(a, b), (a // b, a % b))

    def test_enumerate(self):
        """
        enumerate(iterator) 方法返回一个迭代器，迭代的每一项是一个tuple，包含索引和值
        """
        nums = ['one', 'two', 'three', 'four']
        self.assertTupleEqual(tuple(enumerate(nums)), ((0, 'one'), (1, 'two'), (2, 'three'), (3, 'four')))

        # 迭代的每一项是一个‘tuple’对象，依次为‘(0, 'one')’，‘(1, 'two')’，...
        for num in enumerate(nums):
            self.assertEqual((nums.index(num[1]), num[1]), num)

        # 获取迭代每一项的两项内容
        for i, num in enumerate(nums):
            self.assertEqual(i, nums.index(num))
            self.assertEqual(num, nums[i])

    def test_eval_py2(self):
        """
        exec(str) 执行一个字符串表示的python表达式，并得到执行的结果
        """
        exec 'x = 1'
        self.assertEqual(eval('x + 1'), 2)  # execute the express by string

    '''
    @skip('only for py3')
    def test_eval_py3(self):
        """
        exec(str) 执行一个字符串表示的python表达式，并得到执行的结果
        """
        exec('x = 1')
        self.assertEqual(eval('x + 1'), 2)  # execute the express by string
    '''

    def test_exec(self):
        """
        exec(str) 执行一段字符串表示的python代码
        """
        exec ('''x = 0
for i in range(0, 10):
    x += 1
y = x''')
        self.assertEqual(eval('x'), 10)
        self.assertEqual(eval('y'), eval('x'))

    def test_filter(self):
        """
        filter(lambda, iterator) 方法，根据lambda表达式设定的规则，从集合中过滤所需的元素
        """
        a = [1, 2, 3, 4, 5]
        self.assertTupleEqual(tuple(filter(lambda it: it % 2 == 0, a)), (2, 4))

    def test_float(self):
        """
        float(num) 通过对象的__float__方法将对象转为浮点数
        """

        # 整数转为浮点数
        a = 10
        self.assertEqual(type(a), int)
        self.assertEqual(type(float(a)), float)

        # 字符串转为浮点数
        a = "123.123"
        self.assertEqual(type(a), str)
        self.assertEqual(float(a), 123.123)

        class A:
            def __init__(self, value):
                self.__value = value

            def __float__(self):
                return float(self.__value)

        # 其它类型转为浮点数
        a = A(123.123)
        self.assertTrue(isinstance(a, A))
        self.assertEqual(type(float(a)), float)
        self.assertEqual(float(a), 123.123)

    def test_format(self):
        """
        format(obj, str) 用于将第一个参数根据第二个参数规定的格式进行格式化，格式化依据第一个参数对象的__format__方法
        """
        self.assertEqual(format(123, '.2f'), '123.00')

        class Test:
            def __init__(self, val):
                self.__val = val

            def __format__(self, format_spec):
                return {
                    '%m': lambda: 'm' + str(self.__val),
                    '%n': lambda: 'n' + str(self.__val)
                }[format_spec]()

        t = Test(123)
        self.assertEqual(format(t, '%m'), 'm123')

    def test_getattr(self):
        """
        getattr(obj, 'attr_name') 方法用于获取指定对象的指定属性值
        """

        class Test:
            TEST_VAL = 10

            def __init__(self):
                self.x = 100

        t = Test
        self.assertEqual(getattr(t, 'TEST_VAL'), 10)

        t = Test()
        self.assertEqual(getattr(t, 'x'), 100)

    def test_globals(self):
        """
        globals() 方法返回一个Dict对象，包括当前模块的所有全局量（包括函数，变量，包等）
        """
        global_dict = globals()
        self.assertTrue('TEST_GLOBAL_VAR' in global_dict.keys())
        self.assertEqual(global_dict['TEST_GLOBAL_VAR'], TEST_GLOBAL_VAR)

    def test_hasattr(self):
        """
        hasattr(obj, 'attr_name') 判断指定对象是否拥有指定属性
        """

        class Test:
            TEST_VAL = 10

            def __init__(self):
                self.x = 100

        t = Test
        self.assertTrue(hasattr(t, 'TEST_VAL'))
        t = Test()
        self.assertTrue(hasattr(t, 'x'))

    def test_hash_py2(self):
        """
        hash(obj) 通过对象的__hash__方法返回对象的hash值
        """

        class Test(object):
            def __hash__(self):
                return 1234567

        t = Test()
        self.assertEqual(hash(t), 1234567)

    '''
    @skip('only for py3')
    def test_hash_py3(self):
        """
        hash(obj) 通过对象的__hash__方法返回对象的hash值
        """

        class Test:
            def __hash__(self):
                return 1234567

        t = Test()
        self.assertEqual(hash(t), 1234567)
    '''

    def test_hex(self):
        """
        hex(number) 返回字符串，表示指定数值的16进制值
        """
        # convert number to hex string
        self.assertEqual(hex(255), '0xff')

    def test_int(self):
        """
        int(str, base=10) 方法将字符串转为整数，第二个参数表示数值的进制
        int(obj) 方法根据指定对象的__int__方法将对象转为整数
        """
        val = int(0xFF)
        self.assertEqual(val, 255)

        val = int('0xFF', 16)
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
        """
        isinstance(obj, type) 用于判断一个对象是否是指定类型的对象
        """
        s = 'Hello'
        self.assertTrue(isinstance(s, str))

        s = None
        self.assertFalse(isinstance(s, str))
        self.assertTrue(isinstance(s, object))

    def test_issubclass_py2(self):
        """
        issubclass(obj, type) 用于判断一个类是否是指定类型的子类
        """
        self.assertTrue(issubclass(str, object))

        class Base(object):
            pass

        class Child(Base):
            pass

        self.assertTrue(issubclass(Base, object))
        self.assertTrue(issubclass(Child, Base))

    '''
    @skip('only for py3')
    def test_issubclass(self):
        """
        issubclass(obj, type) 用于判断一个类是否是指定类型的子类
        """
        self.assertTrue(issubclass(str, object))

        class Base:
            pass

        class Child(Base):
            pass

        self.assertTrue(issubclass(Base, object))
        self.assertTrue(issubclass(Child, Base))
    '''

    def test_iter_py2(self):
        """
        iter(obj) 方法通过指定对象的__iter__方法返回迭代器对象
        next(iter) 方法获取一个迭代器指向的当前元素，并令迭代器指向下一个元素
        """

        class TestIterator:
            """
            迭代器类
            """

            def __init__(self, _cur, _max):
                self.__cur = _cur
                self.__max = _max

            def next(self):
                if self.__cur == self.__max:
                    raise StopIteration()  # 如果迭代器没有下一个元素，则抛出该异常
                _cur = self.__cur
                self.__cur += 1
                return _cur

        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                return TestIterator(self.__min, self.__max)

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

    '''
    @skip('only for py3')
    def test_iter_py3(self):
        """
        iter(obj) 方法通过指定对象的__iter__方法返回迭代器对象
        next(iter) 方法获取一个迭代器指向的当前元素，并令迭代器指向下一个元素
        """

        class TestIterator:
            """
            迭代器类
            """

            def __init__(self, _cur, _max):
                self.__cur = _cur
                self.__max = _max

            def __next__(self):
                if self.__cur == self.__max:
                    raise StopIteration()  # 如果迭代器没有下一个元素，则抛出该异常
                _cur = self.__cur
                self.__cur += 1
                return _cur

        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                return TestIterator(self.__min, self.__max)

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
    '''

    def test_len(self):
        """
        len(obj) 通过对象的__len__方法返回一个长度值
        """
        s = '12345'
        self.assertEqual(len(s), 5)

        class Test(object):
            def __init__(self, _len):
                self.__len = _len

            def __len__(self):
                return self.__len

        t = Test(10)
        self.assertEqual(len(t), 10)

    '''
    @skip('only for py3')
    def test_len_py3(self):
        """
        len(obj) 通过对象的__len__方法返回一个长度值
        """
        s = '12345'
        self.assertEqual(len(s), 5)

        class Test:
            def __init__(self, _len):
                self.__len = _len

            def __len__(self):
                return self.__len

        t = Test(10)
        self.assertEqual(len(t), 10)
    '''

    def test_list_py2(self):
        """
        list(iter) 将一个迭代器返回的所有元素组成一个list对象
        """
        self.assertListEqual(list(x if x % 2 == 0 else 0 for x in range(1, 6)), [0, 2, 0, 4, 0])

        class Iterator:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                self.__cur = self.__min
                return self

            def next(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                _cur = self.__cur
                self.__cur += 1
                return _cur

        t = Iterator(1, 6)
        self.assertListEqual(list(t), [1, 2, 3, 4, 5])

    '''
    @skip('only for py3')
    def test_list_py3(self):
        """
        list(iter) 将一个迭代器返回的所有元素组成一个list对象
        """
        self.assertListEqual(list(x if x % 2 == 0 else 0 for x in range(1, 6)), [0, 2, 0, 4, 0])

        class Iterator:
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

        t = Iterator(1, 6)
        self.assertListEqual(list(t), [1, 2, 3, 4, 5])
    '''

    def test_locals(self):
        """
        locals() 方法返回当前函数（方法）中的局部量（包括方法、变量、导入的包等）
        """
        x = 100
        _dict = locals()
        self.assertTrue('x' in _dict.keys())
        self.assertEqual(_dict['x'], 100)

    def test_map(self):
        """
        map(func, iter) 方法将迭代器返回的值通过一个函数映射为其它类型的集合对象
        """
        res = map(lambda x: x % 2 == 0, range(1, 5))
        self.assertTupleEqual(tuple(res), (False, True, False, True))

    def test_max(self):
        """
        max(iter, key) 返回迭代器中最大的元素，key参数为一个函数，表示要比较的元素
        """
        lst = (1, 2, 3, 4, 5)
        res = max(lst)
        self.assertEqual(res, 5)

        res = max(lst, key=lambda x: x % 2)
        self.assertEqual(res, 1)  # 1 % 2 = 2

        res = max(1, -2, 3, 4, -5, key=lambda x: -x if x % 2 == 0 else x)
        self.assertEqual(res, 3)  # 3 % 2 = 1 => 3

        # 通过'cmp_to_key'函数可以将一个比较函数转为key函数，修改比较逻辑会影响到max方法的返回值
        res = max(1, -2, 3, 4, -5, key=functools.cmp_to_key(lambda a, b: b - a))
        self.assertEqual(res, -5)

    def test_memoryview_py2(self):
        """
        memoryview(buffer) 返回一个迭代器，表示一个byte缓冲对象的内存视图
        """
        ''' only for 3
        memv = memoryview(b'abcde')
        self.assertTupleEqual(tuple(memv), (97, 98, 99, 100, 101))

        memv = memoryview(bytearray('abcde', 'utf-8'))
        self.assertTupleEqual(tuple(memv), (97, 98, 99, 100, 101))
        '''
        memv = memoryview(b'abcde')
        self.assertListEqual(memv.tolist(), [97, 98, 99, 100, 101])

        memv = memoryview(bytearray('abcde', 'utf-8'))
        self.assertListEqual(memv.tolist(), [97, 98, 99, 100, 101])

    '''
    @skip('only for py3')
    def test_memoryview_py3(self):
        """
        memoryview(buffer) 返回一个迭代器，表示一个byte缓冲对象的内存视图
        """
        memv = memoryview(b'abcde')
        self.assertTupleEqual(tuple(memv), (97, 98, 99, 100, 101))

        memv = memoryview(bytearray('abcde', 'utf-8'))
        self.assertTupleEqual(tuple(memv), (97, 98, 99, 100, 101))
    '''

    def test_min(self):
        """
        min(iter, key) 返回迭代器中最小的元素，key参数为一个函数，表示要比较的元素
        参考 test_max 函数
        """
        lst = (1, 2, 3, 4, 5)
        res = min(lst)
        self.assertEqual(res, 1)

        res = min(lst, key=lambda x: x % 2)
        self.assertEqual(res, 2)  # 2 % 2 = 0

        res = min(1, -2, 3, 4, -5, key=lambda x: -x if x % 2 == 0 else x)
        self.assertEqual(res, -5)  # -5 % 2 = -1 => -5

        res = min(1, -2, 3, 4, -5, key=functools.cmp_to_key(lambda a, b: b - a))
        self.assertEqual(res, 4)  # -5 % 2 = -1 => -5

    def test_next_py2(self):
        """
        next(iter) 方法返回迭代器指向的当前元素，并令迭代器指向下一个元素
        参考 test_iter 函数
        """

        class Test:
            def __init__(self, _min, _max):
                self.__min = _min
                self.__max = _max

            def __iter__(self):
                self.__cur = self.__min
                return self

            def next(self):
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

    '''
    @skip('only for py3')
    def test_next_py3(self):
        """
        next(iter) 方法返回迭代器指向的当前元素，并令迭代器指向下一个元素
        参考 test_iter 函数
        """

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
    '''

    def test_oct_py2(self):
        """
        oct(int) 返回一个字符串，表示指定整数的8进制形式
        """
        o = oct(8)
        self.assertEqual(o, '010')

    '''
    @skip('only for py3')
    def test_oct_py3(self):
        """
        oct(int) 返回一个字符串，表示指定整数的8进制形式
        """
        o = oct(8)
        self.assertEqual(o, '0o10')
    '''

    def test_open_py2(self):
        """
        file = open(file_name, mode) 函数打开一个文件用于读写访问，返回文件对象
        file.write(str/buffer) 写入文件
        file.read(size) 读取文件
        file.seek(offset) 移动文件指针
        """
        try:
            # 'r'	open for reading (default)
            # 'w'	open for writing, truncating the file first
            # 'x'	open for exclusive creation, failing if the file already exists
            # 'a'	open for writing, appending to the end of the file if it exists
            # 'b'	binary mode
            # 't'	text mode (default)
            # '+'	open a disk file for updating (reading and writing)
            # 'U'	universal newlines mode (deprecated)
            with open('test.txt', 'w') as f:
                f.writelines(('line 1\n'.decode('gbk'), 'line 2\n'.decode('gbk'), 'line 3'.decode('gbk')))
                f.seek(0)
                f.write('LINE'.decode('gbk'))

            with open('test.txt', 'r') as f:
                self.assertEqual(f.readline(), 'LINE 1\n')
                self.assertEqual(f.readline(), 'line 2\n')
                self.assertEqual(f.readline(), 'line 3')
                self.assertEqual(f.readline(), '')  # at the end of line

                f.seek(0)
                s = 'LINE 1\nline 2\nline 3'.decode('gbk')
                self.assertEqual(f.read(len(s)), s)
                f.seek(0)

                for c in s:
                    self.assertEqual(f.read(1), c)
                self.assertEqual('', f.read(1))  # at the end of line
        finally:
            os.remove('test.txt')

    '''
    @skip('only for py3')
    def test_open_py3(self):
        """
        file = open(file_name, mode, encoding) 函数打开一个文件用于读写访问，返回文件对象
        file.write(str/buffer) 写入文件
        file.read(size) 读取文件
        file.seek(offset) 移动文件指针
        """
        try:
            # 'r'	open for reading (default)
            # 'w'	open for writing, truncating the file first
            # 'x'	open for exclusive creation, failing if the file already exists
            # 'a'	open for writing, appending to the end of the file if it exists
            # 'b'	binary mode
            # 't'	text mode (default)
            # '+'	open a disk file for updating (reading and writing)
            # 'U'	universal newlines mode (deprecated)
            with open('test.txt', 'w', encoding='gbk') as f:
                self.assertTrue(f.writable())
                f.writelines(('line 1\n', 'line 2\n', 'line 3'))
                f.seek(0)
                f.write('LINE')

            with open('test.txt', 'r', encoding='gbk') as f:
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
            os.remove('test.txt')
    '''

    def test_ord(self):
        """
        ord(str) 获取一个字符的ASCII编码
        chr(code) 获取一个ASCII编码所代表的字符
        """
        n = ord('a')
        self.assertEqual('a', chr(n))

    def test_pow(self):
        """
        pow(n, x) 计算n的x次方，相当于'n ** x'
        """
        n = pow(2, 2)
        self.assertEqual(n, 2 ** 2)

        n = pow(2, 2, 2)
        self.assertEqual(n, 2 ** 2 % 2)

    def test_property_py2(self):
        """
        @property func() 注解注解一个方法，令其表示一个属性值
        @func.setter 注解表示属性的设置方法
        @func.getter 注解表示属性的获取方法
        @func.deleter 注解表示属性的删除方法
        """

        class Test(object):  # 注意，一定（或间接）要从object类继承
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
        self.assertFalse(hasattr(t, 'value'))

    '''
    @skip('only for py3')
    def test_property_py3(self):
        """
        @property func() 注解注解一个方法，令其表示一个属性值
        @func.setter 注解表示属性的设置方法
        @func.getter 注解表示属性的获取方法
        @func.deleter 注解表示属性的删除方法
        """

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
        self.assertFalse(hasattr(t, 'value'))
    '''

    def test_range(self):
        """
        range(max)
        range(min, max)
        range(min, max, step) 函数表示一个范围，返回一个从min到max - 1的迭代器
        """
        r = range(5)
        self.assertEqual(tuple(r), (0, 1, 2, 3, 4))

        r = range(2, 5)
        self.assertEqual(tuple(r), (2, 3, 4))

        r = range(1, 5, 2)
        self.assertEqual(tuple(r), (1, 3))

    def test_str_and_repr(self):
        """
        str(obj) 函数通过对象的__str__方法返回字符串
        repr(obj) 函数通过对象的__repr__方法返回字符串
        一般情况下，repr返回的字符串要比str方法返回的字符串更底层一些
        """
        s = 'test'
        self.assertEqual(s, str(s))
        self.assertEqual(s, eval(repr(s)))

        class Test:
            def __init__(self, val):
                self.__val = val

            def __str__(self):
                return str(self.__val)

            def __repr__(self):
                return '{name}:{value}'.format(name=self.__class__.__name__, value=self.__val)

        t = Test(100)
        self.assertEqual(str(t), '100')
        self.assertEqual(repr(t), 'Test:100')

    def test_reversed_py2(self):
        """
        reversed(seque) 返回一个序列的逆序序列
        reversed(iter) 通过迭代器对象的__reversed__获取一个反向迭代器
        """
        s = [1, 2, 3]
        self.assertEqual(tuple(reversed(s)), (3, 2, 1))

        class Test:
            def __init__(self, _min, _max, _step=1):
                self.__min, self.__max = _min, _max
                self.__step = _step

            def __iter__(self):
                self.__cur = self.__min
                return self

            def next(self):
                if self.__cur == self.__max:
                    raise StopIteration()
                cur = self.__cur
                self.__cur += self.__step
                return cur

            def __reversed__(self):
                return Test(self.__max - 1, self.__min - 1, -self.__step)

        t = Test(1, 5)
        self.assertEqual(tuple(reversed(t)), (4, 3, 2, 1))

    '''
    @skip('only for py3')
    def test_reversed_py3(self):
        """
        reversed(seque) 返回一个序列的逆序序列
        reversed(iter) 通过迭代器对象的__reversed__获取一个反向迭代器
        """
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
    '''

    def test_round_py2(self):
        """
        round(float) 返回指定小数位的浮点数，对多出的小数位进行四舍五入
        round(obj) 通过对象的__round__方法对指定对象进行小数位保留操作
        """
        n = round(123.456, 2)
        self.assertEqual(n, 123.46)

        class Test(object):
            def __init__(self, _n):
                self.__n = _n

            def __float__(self):
                return self.__n

            @property
            def n(self):
                return self.__n

        t = Test(123.456)
        self.assertEqual(round(t, 2), 123.46)

    '''
    @skip('only for py3')
    def test_round_py3(self):
        """
        round(float) 返回指定小数位的浮点数，对多出的小数位进行四舍五入
        round(obj) 通过对象的__round__方法对指定对象进行小数位保留操作
        """
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
    '''

    def test_set(self):
        """
        set(seque) 将一个序列转为set集合
        """
        s = {1, 1, 2, 2, 3, 3, 4, 4}  # define a set
        self.assertSetEqual(s, {1, 2, 3, 4})

        t = (1, 1, 2, 2, 3, 3, 4, 4)
        s = set(t)
        self.assertEqual(s, {1, 2, 3, 4})

    def test_setattr(self):
        """
        setattr(obj, attr_name, value) 用于向指定对象设置指定属性
        """

        ''' only for 3
        class Test:
            def __init__(self):
                self.a = 0
        '''

        class Test(object):
            def __init__(self):
                self.a = 0

        t = Test()
        setattr(t, 'a', 100)

        self.assertEqual(t.a, 100)
        self.assertEqual(getattr(t, 'a'), 100)

    def test_slice(self):
        """
        slice(start, end, step) 表示一个下标范围，可以从序列中按此返回获取子集
        """
        l = (1, 2, 3, 4, 5)
        s = slice(2)
        self.assertEqual(l[s], l[:2])

        s = slice(2, 5)
        self.assertEqual(l[s], l[2:5])

        s = slice(2, 5, 2)
        self.assertEqual(l[s], l[2:5:2])

    def test_sorted(self):
        """
        sorted(seque, key) 返回一个经过排序的新序列, key是一个函数，返回排序时要比较的值
        cmp_to_key(func) 方法用于将比较函数转换为key函数
        """
        rand = Random()
        expected_list = [1, 2, 3, 4, 5]
        shuffle_list = expected_list[::]
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
        # 通过key函数返回要比较的值
        shuffle_list = sorted(expected_list, key=lambda t: t.name)
        self.assertEqual(shuffle_list, expected_list)

        expected_list = [Test('a', 400), Test('b', 300), Test('c', 200), Test('d', 100)]
        # 通过key函数返回要比较的值
        shuffle_list = sorted(expected_list, key=lambda t: t.value)
        self.assertEqual(shuffle_list, list(reversed(expected_list)))

    def test_sum(self):
        """
        sum(seque) 返回一个序列所有元素的总和
        """
        l = [1, 2, 3, 4, 5]
        expected = 0
        for n in l:
            expected += n

        self.assertEqual(sum(l), expected)
        self.assertEqual(sum(l, 100), expected + 100)

    def test_super_py2(self):
        """
        super(type, obj) 返回指定类型对象的超类引用
        """

        class Base(object):
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
                return super(Grand, self).mark  # 访问超类中的mark属性

        o = Base()
        self.assertEqual(o.mark, 'Base')

        o = Child()
        self.assertEqual(o.mark, 'Child')
        self.assertEqual(super(Child, o).mark, 'Base')

        o = Grand()
        self.assertEqual(o.mark, 'Child')
        self.assertEqual(super(Grand, o).mark, 'Child')

    '''
    @skip('only for py3')
    def test_super_py3(self):
        """
        super() 返回当前对象的超类引用
        super(type, obj) 返回指定类型对象的超类引用
        """

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
                return super().mark  # 访问超类中的mark属性

        o = Base()
        self.assertEqual(o.mark, 'Base')

        o = Child()
        self.assertEqual(o.mark, 'Child')
        self.assertEqual(super(Child, o).mark, 'Base')

        o = Grand()
        self.assertEqual(o.mark, 'Child')
        self.assertEqual(super(Grand, o).mark, 'Child')
    '''

    def test_type(self):
        """
        type(obj) 获取对象的类型
        type(type_name, super_type, attributes) 创建一个类型为type_name的对象
        """
        self.assertEqual(type(123), int)
        self.assertEqual(type('Hello'), str)

        # Create a type named 'Test'
        t = type('Test', (object,), dict(VAL=100))
        self.assertEqual(t.VAL, 100)

    def test_vars(self):
        """
        getattr(obj, attr_name) 获取指定对象的一个属性值
        """

        class Test:
            def __init__(self, a, b):
                self.__a, self.__b = a, b

        t = Test(1, 2)

        # Get all variables from an object
        var = vars(t)
        for key in var:
            self.assertEqual(getattr(t, key), var[key])

    def test_zip(self):
        """
        zip(seque1, seque2) 合并两个序列
        [a1, a2, a3] 合并 [b1, b2, b3] => [[a1, b1], [a2, b2], [a3, b3]]

        zip(*zipped_seque) 分解合并后的序列
        """
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

    def test_frozenset(self):
        """
        frozenset 函数用于产生一个‘只读’的‘set’集合
        """
        alist = [1, 2, 3, 4, 5, 4, 3, 2, 1]
        aset = frozenset(alist)
        # 产生‘set’集合，重复的元素项被去除
        self.assertSetEqual(aset, {1, 2, 3, 4, 5})

        # frozenset 产生的‘set’集合没有‘add’等方法，只能读取，无法修改
        with self.assertRaises(AttributeError):
            aset.add(4)
