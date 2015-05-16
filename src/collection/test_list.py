# coding=utf-8

from unittest import TestCase
import functools


class TestList(TestCase):
    def test_empty_list(self):
        """
        list对象的__len__方法用于测量集合元素的数量，
        len内置函数的作用与之类似（其在内部调用了__len__方法）
        """
        l = []
        self.assertListEqual(l, [])
        self.assertEqual(l.__len__(), 0)
        self.assertEqual(len(l), l.__len__())

    def test_create_list(self):
        """
        使用[]可以创建一个list，list中可以包含任意类型元素
        通过 list对象[下标] 可以访问集合中的某个对应元素，下标可以是负数，表示从集合结尾进行计算
        """
        l = [123, 'a', None]
        self.assertEqual(len(l), 3)
        self.assertEqual(l[0], 123)
        self.assertEqual(l[-1], None)

    def test_list_range(self):
        """
        通过 list对象[起始下标:结束下标:步长] 可以获取指定范围的元素组成新的集合
        """
        l = [1, 2, 3]
        self.assertListEqual(l[:], [1, 2, 3])
        self.assertListEqual(l[1:3], [2, 3])
        self.assertListEqual(l[0:-1], [1, 2])
        self.assertListEqual(l[0:3:2], [1, 3])

    def test_add_elements(self):
        """
        + 运算符可以将两个list集合合并，得到一个新的集合
        .append方法可以在集合的末尾加入一个新元素
        .insert方法可以在集合的指定位置插入一个新元素
        """
        l = [1, 2, 3]
        self.assertListEqual(l + [4, 5, 6], [1, 2, 3, 4, 5, 6])

        l.append(4)
        l.append(5)
        self.assertListEqual(l, [1, 2, 3, 4, 5])

        l = [1, 2, 3]
        l.insert(0, -1)
        self.assertListEqual(l, [-1, 1, 2, 3])

    def test_list_multiply(self):
        """
        集合乘以任意整数n，表示将集合元素重复n次，得到一个新集合
        """
        l = [1, 2, 3]
        l *= 2
        self.assertListEqual(l, [1, 2, 3, 1, 2, 3])

    def test_stack(self):
        """
        通过 .pop方法可以从集合末尾获取并删除一个元素，配合 .append方法，可以令集合产生“栈”的效果
        """
        l = [1, 2, 3]
        self.assertEqual(l.pop(), 3)
        self.assertEqual(l.pop(), 2)
        self.assertEqual(l.pop(), 1)

        # 如果集合为空，则pop方法会抛出IndexError异常
        with self.assertRaises(IndexError):
            l.pop()

    def test_sort1(self):
        """
        .sort 方法可以对集合进行排序，默认情况下是根据元素对象的__lt__方法（小于比较）进行元素比较的
        """

        class A:
            def __init__(self, value):
                self.__value = value

            def __lt__(self, other):
                return self.__value < other.__value

            def __eq__(self, other):
                return self.__value == other.__value

        l = [A(3), A(2), A(1)]
        l.sort()
        self.assertListEqual(l, [A(1), A(2), A(3)])

    def test_sort2(self):
        """
        如果不按照元素默认的“小于”规则比较，则可以在排序时指定sort方法的key参数，
        通过functools.cmp_to_key方法指定排序的比较规则
        """
        l = [3, 2, 1]
        l.sort()
        self.assertListEqual(l, [1, 2, 3])

        l.sort(key=functools.cmp_to_key(lambda a, b: b - a))
        self.assertListEqual(l, [3, 2, 1])

    def test_sort_by_key(self):
        """
        如果集合元素未实现__lt__方法，无法进行小于比较时，可以通过sort方法的key参数指定元素对象
        用于排序的属性
        """

        class A:
            def __init__(self, value):
                self.__value = value

            def __eq__(self, other):
                return self.__value == other.__value

            @property
            def value(self):
                return self.__value

        l = [A(3), A(2), A(1)]
        l.sort(key=lambda a: a.value)
        self.assertListEqual(l, [A(1), A(2), A(3)])

    def test_reverse(self):
        """
        .reverse方法用于“翻转”一个集合，得到一个新集合，和原集合拥有相同的元素，但排列顺序相反
        """
        l = [1, 2, 3]
        l.reverse()
        self.assertListEqual(l, [3, 2, 1])

    def test_for_in(self):
        """
        语法 [exp for n in list] 产生一个新集合，整个集合通过for循环产生，每个元素的值则
        由exp表达式获得
        """
        l = [1, 2, 3]
        ls = [e * 2 for e in l]
        self.assertListEqual(ls, [2, 4, 6])

        l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        ls = [sum(row) for row in l]
        self.assertListEqual(ls, [6, 15, 24])

    def test_for_in_if(self):
        """
        语法 [exp for n in list if exp] 产生一个新集合，整个集合通过for循环产生，并且必须令
        if 之后的表达式为True，每个元素的值由exp表达式获得，
        """
        l = [1, 2, 3]
        ls = [e for e in l if e % 2 != 0]
        self.assertListEqual(ls, [1, 3])

    def test_count(self):
        """
        .count方法用于计算集合中指定元素的个数
        """
        l = [1, 2, 3, 2]
        n = l.count(2)
        self.assertEqual(n, 2)

    def test_remove(self):
        """
        .remove方法用于从集合中移除第一个指定元素
        """
        l = [1, 2, 3]
        l.remove(2)
        self.assertListEqual(l, [1, 3])

    def test_index(self):
        """
        .index方法用于查找指定元素在集合中的下标，可以指定查找的范围，即
        list.index(element, start_index, end_index)
        """
        l = [1, 2, 3]
        n = l.index(2)
        self.assertEqual(n, 1)

        with self.assertRaises(ValueError):
            l.index(2, 2)

        n = l.index(3, 2)
        self.assertEqual(n, 2)

        with self.assertRaises(ValueError):
            l.index(2, 2, 3)