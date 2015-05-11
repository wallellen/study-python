# coding=utf-8
from abc import ABCMeta, abstractmethod
from unittest import TestCase, skip


class TestClass(TestCase):
    def test_class(self):
        """
        Python 是面向对象的，所以具有创建类、对象的功能
        利用:
                class Name(Supper):
                    ...
        或
                class Name:
                    ...
        声明一个Python类，前者显式声明了超类，后者则是从object类继承

        """

        class A:
            def __init__(self, value):  # 构造器方法
                self.value = value

            def __str__(self):  # 对象转字符串
                return str(self.value)

            def __add__(self, other):  # 对象的加号运算符
                if isinstance(other, A):
                    return A(self.value + other.value)
                elif isinstance(other, int) or isinstance(other, float):
                    return A(self.value + other)
                raise TypeError()

            def __sub__(self, other):  # 对象的减号运算符
                if isinstance(other, A):
                    return A(self.value - other.value)
                elif isinstance(other, int) or isinstance(other, float):
                    return A(self.value - other)
                raise TypeError()

            def __int__(self):  # int(obj) 相关运算符
                return int(self.value)

            def __float__(self):  # float(obj) 相关运算符
                return float(self.value)

            def __cmp__(self, other):  # 比较两个对象
                if isinstance(other, A):
                    return self.value - other.value
                elif isinstance(other, int) or isinstance(other, float):
                    return self.value - other
                raise TypeError()

            def __le__(self, other):  # 小于等于运算符
                return self.__cmp__(other) <= 0

            def __lt__(self, other):  # 小于运算符
                return self.__cmp__(other) < 0

            def __ge__(self, other):  # 大于等于运算符
                return not self.__lt__()

            def __gt__(self, other):  # 大于运算符
                return not self.__le__(other)

            def __eq__(self, other):  # 等于运算符
                return self.__cmp__(other) == 0

            def get_value(self):  # 类方法
                return self.value

        a = A(100)
        self.assertEqual(str(a), '100')

        a = a + A(50)
        self.assertEqual(str(a), '150')

        a -= 20
        self.assertEqual(str(a), '130')
        self.assertEqual(int(a), 130)
        self.assertEqual(float(a), 130.0)

        b = A(140)
        self.assertTrue(b > a)
        self.assertTrue(a <= b)
        self.assertFalse(a == b)

        self.assertEqual(a.get_value(), a.value)


    def test_inherit(self):
        """
        class B(A): 表示类B继承自类A，其中：
        1. __开头的变量或方法表示private，其余命名表示public
        2. 可以用_开头来表示protected，但这并不是标准语法
        3. 子类的同类型方法覆盖超类方法
        4. 通过super().可以在子类中访问到超类成员
        """

        class A:
            def __init__(self):
                self.__val1 = 100
                self.__val2 = 200

            @property
            def value1(self):
                return self.__val1

            @property
            def value2(self):
                return self.__val2

        class B(A):
            @property
            def value2(self):
                return super().value1 + super().value2

        self.assertTrue(issubclass(B, A))

        b = B()
        self.assertTrue(isinstance(b, A))
        self.assertTrue(issubclass(type(b), A))

        a = A()
        self.assertEqual(b.value1, a.value1)
        self.assertEqual(b.value2, a.value1 + a.value2)

    def test_metaclass(self):
        def metaclass(name, parents, attrs):
            print(name)
            print(parents)
            print(attrs)
            return "metaclass"

        class A(metaclass=metaclass):
            pass

        self.assertEqual(type(A), str)

    @skip('only for python 2.x')
    def test_abstract_for_2(self):
        """
        抽象方法和抽象类
            在Python中声明抽象超类的方式有几种，较为官方的方式是采用'abc'包中的‘ABCMeta’类和'@abstractmethod'注解
            对于Python 2.x来说，声明一个抽象类格式如下：

            class ClassName(SuperClass):
                __metaclass__=abc.ABCMeta
                ...

                @abstractmethod
                def method(args):
                    ...
        """

        class A:  # 定义抽象类
            __metaclass__ = ABCMeta  # 指定ABCMeta为当前类的元类

            @abstractmethod  # 定义抽象方法
            def value(self):
                pass

        class B1(A):  # 继承自抽象类但未覆盖抽象方法
            pass

        class B2(A):  # 继承自抽象类并覆盖抽象方法
            def value(self):
                return 100

        with self.assertRaises(TypeError):
            A().value()

        with self.assertRaises(TypeError):
            B1().value()

        self.assertEqual(B2().value(), 100)

    def test_abstract_for_3(self):
        """
        抽象方法和抽象类
            在Python中声明抽象超类的方式有几种，较为官方的方式是采用'abc'包中的‘ABCMeta’类和'@abstractmethod'注解
            对于Python 3.x来说，声明一个抽象类格式如下：

            class ClassName(SuperClass, metaclass=abc.ABCMeta):
                ...

                @abstractmethod
                def method(args):
                    ...
        """

        class A(metaclass=ABCMeta):  # 定义抽象类
            @abstractmethod  # 定义抽象方法
            def value(self):
                pass

        class B1(A):  # 继承自抽象类但未覆盖抽象方法
            pass

        class B2(A):  # 继承自抽象类并覆盖抽象方法
            def value(self):
                return 100

        with self.assertRaises(TypeError):
            A().value()

        with self.assertRaises(TypeError):
            B1().value()

        self.assertEqual(B2().value(), 100)

    def test_slots_and_attributes(self):
        """
        类的 __slots__ 成员表示类中可以包含的成员变量名称
        """

        class A1:
            pass

        class A2:
            __slots__ = ['age', 'name']

        a = A1()
        a.age = 10
        a.name = 'Alvin'
        a.gender = 'M'

        a = A2()
        a.age = 10
        a.name = 'Alvin'
        with self.assertRaises(AttributeError):
            a.gender = 'M'
