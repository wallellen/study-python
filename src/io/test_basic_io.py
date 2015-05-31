# coding=utf-8
import linecache

from unittest import TestCase
import io
import os
from os import path


class TestBasicIO(TestCase):
    """
    """
    '''
    @skip('no need for testing')
    def test_standard_output_py2(self):
        print "Hello"
        print '%d + %d = %d' % (10, 20, 10 + 20)
        print 10, 20, 30

        print 'First', 'Second'

    @skip('only for py3')
    def test_standard_output_py3(self):
        print("Hello")
        print('%d + %d = %d' % (10, 20, 10 + 20))
        print(10, 20, 30)

        print('First', end=' ')
        print('Second')

    @skip('no need for testing')
    def test_standard_input(self):
        name = raw_input('Please input your name: ')
        print('Hello %s' % name)
    '''

    def test_read_write_file_py2(self):
        """
        open(file_name, open_mode[, buffering]) -> file 方法用于打开一个文件，
            file_name 参数用于指定文件的路径和名称，
            open_mode 参数是一个字符串，表示打开文件的方式，所有的方式如下
                'r'	open for reading (default)
                'w'	open for writing, truncating the file first
                'x'	open for exclusive creation, failing if the file already exists
                'a'	open for writing, appending to the end of the file if it exists
                'b'	binary mode
                't'	text mode (default)
                '+'	open a disk file for updating (reading and writing)
                'U'	universal newlines mode (deprecated)
            buffering 用于指定读写用缓冲的大小，忽略该参数则使用默认缓冲
            对于 python2 来说，‘binary mode’和‘text mode’的区别不大，主要是在读取文件时对换行符号的处理上

        file::write(string/bytes) -> int 写入指定字符串（或字节串）
        file::read(length) -> string/bytes 读取指定数量的字符（或字节），返回字符串或字节串
        """
        try:
            with open('test.txt', 'w') as fw:
                self.assertEqual(fw.name, 'test.txt')
                fw.write('Hello World ')
                fw.writelines(['a', 'b', 'c', 'd'])

            self.assertEqual(path.getsize('test.txt'), 16)
            with open('test.txt', 'r') as fr:
                self.assertEqual(fr.name, 'test.txt')
                self.assertEqual(fr.read(11), 'Hello World')
                # ‘text mode’下支持文件指针的相对位置操作
                fr.seek(1, io.SEEK_CUR)
                self.assertEqual(fr.read(1), 'a')
                self.assertEqual(fr.read(), 'bcd')
        finally:
            os.remove('test.txt')

    '''
    @skip('only for py3')
    def test_read_write_file_py3(self):
        """
        open(file_name, open_mode[, buffering, encoding) -> file 方法用于打开一个文件
            file_name 参数用于指定文件的路径和名称，
            open_mode 参数是一个字符串，表示打开文件的方式，所有的方式如下
                'r'	open for reading (default)
                'w'	open for writing, truncating the file first
                'x'	open for exclusive creation, failing if the file already exists
                'a'	open for writing, appending to the end of the file if it exists
                'b'	binary mode
                't'	text mode (default)
                '+'	open a disk file for updating (reading and writing)
                'U'	universal newlines mode (deprecated)
            对于 python3 来说，‘binary mode’和‘text mode’的区别如下：
                1. 在读取文件时对换行符号的处理上，‘text mode’会处理换行符
                2. ‘text mode’不支持文件指针的‘相对位置’操作

        file::write(string/bytes) -> int 写入指定字符串（或字节串）
        file::read(length) -> string/bytes 读取指定数量的字符（或字节），返回字符串或字节集合
        """
        try:
            # 支持以指定的编码方式打开文件进行写或读操作
            with open('test.txt', 'w', encoding='GBK') as fw:
                self.assertEqual(fw.name, 'test.txt')
                fw.write('Hello World ')
                fw.writelines(['a', 'b', 'c', 'd'])

            self.assertEqual(path.getsize('test.txt'), 16)
            with open('test.txt', 'r', encoding='GBK') as fr:
                self.assertEqual(fr.name, 'test.txt')
                self.assertEqual(fr.read(11), 'Hello World')
                # ‘text mode’下，不支持文件指针的相对位置操作
                fr.seek(1 + fr.tell())
                self.assertEqual(fr.read(1), 'a')
                self.assertEqual(fr.read(), 'bcd')
        finally:
            os.remove('test.txt')
    '''

    def test_read_write_with_lines_py2(self):
        """
        python可以处理文件中的换行符，并根据换行符将文件内容分割成字符串
            file::writelines(iterators[string]) 可以一次写入若干行
            file::readline() -> string 一次读取一行内容（或到文件结束）
            file::readlines() -> list[string] 一次读取所有行
        """
        try:
            with open('test.txt', 'wb') as fw:
                self.assertEqual(fw.name, 'test.txt')
                fw.write('Hello World\n')
                # 写入四行内容
                fw.writelines(['a\n', 'b\n', 'c\n', 'd\n'])

            with open('test.txt', 'rb') as fr:
                # 读取一行
                self.assertEqual(fr.readline(), 'Hello World\n')
                # 读取之后的所有行
                self.assertEqual(fr.readlines(), ['a\n', 'b\n', 'c\n', 'd\n'])

                fr.seek(0)
                lines = fr.readlines()
                fr.seek(0)

                n = 0
                # 通过迭代的方法读取文件中的每一行
                for line in fr:
                    self.assertEqual(line, lines[n])
                    n += 1
        finally:
            os.remove('test.txt')

    '''
    @skip('only for py3')
    def test_read_write_with_lines_py3(self):
        """
        python可以处理文件中的换行符，并根据换行符将文件内容分割成字符串
            file::writelines(iterators[string]) 可以一次写入若干行
            file::readline() -> string 一次读取一行内容（或到文件结束）
            file::readlines() -> list[string] 一次读取所有行

        在 python3 中，数据类型更加严格，如果文件是以‘b’（二进制）方式打开，则：
            1. 写入的内容必须是‘bytes’，如果要写入字符串，则必须进行编码操作（str::encode([charset])）；
            2. 读取的结果是一个‘bytes’，如果要转为字符串，则必须进行解码操作（bytes::decode([charset])）；
        """
        try:
            with open('test.txt', 'wb') as fw:
                self.assertEqual(fw.name, 'test.txt')
                fw.write('Hello World\n'.encode())
                # 写入四行内容
                fw.writelines([s.encode() for s in ['a\n', 'b\n', 'c\n', 'd\n']])

            with open('test.txt', 'rb') as fr:
                # 读取一行
                self.assertEqual(fr.readline().decode(), 'Hello World\n')
                # 读取之后的所有行
                self.assertEqual([s.decode() for s in fr.readlines()], ['a\n', 'b\n', 'c\n', 'd\n'])

                fr.seek(0)
                lines = fr.readlines()
                fr.seek(0)

                n = 0
                # 通过迭代的方法读取文件中的每一行
                for line in fr:
                    self.assertEqual(line, lines[n])
                    n += 1
        finally:
            os.remove('test.txt')
    '''

    def test_line_cache_py2(self):
        """
        ‘linecache’包含了一些操作多行文件的API，主要是用起‘getline’函数
            linecache.getline(file_name, line_no) -> string 获取指定文件，指定行号的结果
        """
        try:
            with open('test.txt', 'wb') as fw:
                for n in xrange(1, 100):
                    fw.write(str(n))
                    fw.write('\n')

            for n in xrange(1, 100):
                self.assertEqual(linecache.getline('test.txt', n), str(n) + '\n')
        finally:
            os.remove('test.txt')

    '''
    @skip('only for py3')
    def test_line_cache_py3(self):
        """
        ‘linecache’包含了一些操作多行文件的API，主要是用起‘getline’函数
            linecache.getline(file_name, line_no) -> string 获取指定文件，指定行号的结果
        """
        try:
            with open('test.txt', 'wb') as fw:
                for n in range(1, 100):
                    fw.write(str(n).encode())
                    fw.write('\n'.encode())

            for n in range(1, 100):
                self.assertEqual(linecache.getline('test.txt', n), str(n) + '\n')
        finally:
            os.remove('test.txt')
    '''
