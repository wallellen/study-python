# coding=utf-8

import os
from os import path
from unittest import TestCase
import struct
import zipfile


class TestZipIO(TestCase):
    def test_zip_file(self):
        """
        zipfile.ZipFile(file_name, mode[, compression, allowZip64]) -> ZipFile 方法用于创建一个Zip压缩（解压缩）对象
            file_name 压缩文件的文件名
            mode 打开方式，可以为
                r 只读方式
                w 只写方式
                a 追加方式
            compression 压缩方式，可以为
                ZIP_STORED 仅存储（不进行压缩），默认值
                ZIP_DEFLATED 压缩
            allowZip64 是否支持64位模式，默认值为False

        ZipFile::writestr(entry_name, bytes/str) 将byte数据（字符串）写入压缩文件的指定区块中
            entry_name 压缩文件的区块名称
            bytes/str 需要压缩的数据流

        ZipFile::read(entry_name[, password]) -> bytes/str 从指定区块中读取数据
            entry_name 压缩文件的区块名称
            password 压缩文件的密码
        """
        data = bytearray()
        for n in xrange(0, 1000):
            data += struct.pack('i', 0xff)

        try:
            with open('test.dat', 'wb') as nf:
                with zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
                    nf.write(data)
                    zf.writestr('test.dat', bytes(data))

            self.assertGreater(path.getsize('test.dat'), path.getsize('test.zip'))

            with open('test.dat', 'rb') as nf:
                with zipfile.ZipFile('test.zip', 'r') as zf:
                    self.assertEqual(nf.read(), zf.read('test.dat'))
        finally:
            os.remove('test.dat')
            os.remove('test.zip')
