# coding=utf-8

from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = ['main']

setup(name='module',  # file name of current package
      version='1.0',
      description='Test package module',
      author='Alvin.Qu',
      author_email='mousebaby8080@gmail.com',
      url='http://www.alvin.edu',
      packages=find_packages('.', EXCLUDE_FROM_PACKAGES), requires=['module'])  # module name to package

# package:
# use command line 'python setup.py sdist' to package, the package file would be in 'dist' folder

# unpack and install:
# use command line 'tar -xvf basic_module-1.0.tar.gz' to unpack
# use command line 'python setup.py install' to install the package
# use command line 'pip freeze' to show custom packages
# use command line 'pip uninstall <package-name>' to uninstall package
# or
# use command line 'python setup.py install --record files.txt' to install the package
# use command line 'cat files.txt | xargs rm -rf' to delete the package