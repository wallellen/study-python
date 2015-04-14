# coding=utf-8
from unittest import TestCase
import io
import functools
import time


class TestDecorators(TestCase):
    """
    python的注解是一个具有一个参数的函数
    当被注解函数（方法）被调用时，注解函数会被执行，被注解函数（方法）作为参数传入注解函数
    通过在注解函数中进行处理，从而可以影响和改变被注解函数（方法）的执行行为

    注意，注解的参数固定为被注解函数（或方法），所以使用注解时无需参数列表。如果要传入参数，则必须通过闭包
    或者callable对象

    注解的主要作用是“代理”被注解的方法，这个代理是完全的，也就是说，一旦某个函数（方法）被注解，则调用该方
    法时，该方法的实际代码有可能不会被执行，这要看代理方法的具体逻辑
    """

    def test_decorator_as_wrapper(self):
        """
        通过注解获取被注解函数（方法）的代理
        可以在注解函数中定义闭包函数并返回，此时调用被注解函数，执行的实际上是注解函数返回的闭包函数，
        该闭包函数即被注解函数的代理
        """

        # 定义注解函数
        def tag(func):
            # 返回代理函数
            def wrapper():
                return {'wrapped': True, 'result': func()}  # 调用被注解方法

            return wrapper

        @tag  # 调用注解函数，将demo函数作为参数传入注解函数，执行返回的代理方法
        def demo():
            return 'demo worked'

        self.assertEqual(demo(), {'wrapped': True, 'result': 'demo worked'})

    def test_decorator_with_arguments(self):
        """
        为注解添加参数：
            注解函数本身只能拥有一个参数，即被注解函数本身，如果要在注解时传入其它参数，则必须通过闭包的方式
        1. 定义任意参数函数A
        2. A函数返回标准注解函数B
        3. B函数中包含被注解方法的代理
        """

        # 定义带有任意参数函数
        def html_tag(tag_name, **kwargs):
            # 定义注解函数并返回该函数
            def decorator(func):
                # 定义被注解函数代理函数并返回该函数
                def wrapper():
                    sio = io.StringIO()
                    sio.write('<')
                    sio.write(tag_name)
                    for key in sorted(kwargs.keys()):
                        sio.write(' ')
                        sio.write('class' if key == 'clazz' else key)
                        value = str(kwargs[key])
                        if value.find('\"') < 0:
                            sio.write('=\"')
                            sio.write(value)
                            sio.write('\"')
                        else:
                            sio.write('=\'')
                            sio.write(value)
                            sio.write('\'')
                    nested = func()  # 调用被注解方法
                    if len(nested) == 0:
                        sio.write('/>')
                    else:
                        sio.write('>')
                        sio.write(nested)
                        sio.write('</')
                        sio.write(tag_name)
                        sio.write('>')
                    sio.seek(0)
                    return sio.read()

                return wrapper

            return decorator

        # 调用函数并传入参数，返回注解函数
        @html_tag(tag_name='div', style='display:block', clazz='col-md-2')
        def demo1():
            return 'Hello'

        self.assertEqual(demo1(), '<div class="col-md-2" style="display:block">Hello</div>')

        @html_tag(tag_name='div', click='alter(\"ok\")')
        def demo2():
            return ''

        self.assertEqual(demo2(), '<div click=\'alter("ok")\'/>')

    def test_decorator_with_callback_instance(self):
        """
        利用callable对象实现注解
            如果一个对象的类包含__call__方法，则该对象可以看作为函数使用，如果其参数为函数类型，
        则该对象可以作为注解使用
            对象作为注解的优势在于：1。可以通过构造器传递参数；2. 可以在对象中保持状态；
        """

        class HtmlTag:
            def __init__(self, tag_name, **kwargs):
                self.__kwargs = kwargs
                self.__tag_name = tag_name

            def __call__(self, callback):
                """
                    该方法可以令对象看作为一个函数，该方法返回一个代理方法
                """

                def wrapper():
                    sio = io.StringIO()
                    sio.write('<')
                    sio.write(self.__tag_name)
                    for key in sorted(self.__kwargs):
                        sio.write(' ')
                        sio.write('class' if key == 'clazz' else key)
                        value = str(self.__kwargs[key])
                        if value.find('\"') < 0:
                            sio.write('=\"')
                            sio.write(value)
                            sio.write('\"')
                        else:
                            sio.write('=\'')
                            sio.write(value)
                            sio.write('\'')
                    nested = callback()  # 调用被注解方法
                    if len(nested) == 0:
                        sio.write('/>')
                    else:
                        sio.write('>')
                        sio.write(nested)
                        sio.write('</')
                        sio.write(self.__tag_name)
                        sio.write('>')
                    sio.seek(0)
                    return sio.read()

                return wrapper

        # 调用构造器构造对象，将其__call__方法作为注解方法使用
        @HtmlTag(tag_name='div', style='display:block', clazz='col-md-2')
        def demo1():
            return 'Hello'

        self.assertEqual(demo1(), '<div class="col-md-2" style="display:block">Hello</div>')

        @HtmlTag(tag_name='div', click='alter(\"ok\")')
        def demo2():
            return ''

        self.assertEqual(demo2(), '<div click=\'alter("ok")\'/>')

    def test_decorator_modify_arguments1(self):
        """
        通过注解改变传入到被注解方法中的参数值：
            由于被注解函数（方法）是由注解产生的代理方法来处理，所以完全可以在调用被注解函数前改变传入的参数
        """

        def decorator(func):
            def wrapper(**kwargs):
                kwargs['name'] = 'Alvin'  # 改变传入被注解方法的参数
                return func(**kwargs)  # 调用被注解方法

            return wrapper

        @decorator
        def demo(**kwargs):
            return kwargs

        self.assertEqual(demo(no=1001), {'name': 'Alvin', 'no': 1001})

    def test_decorator_modify_arguments2(self):
        def decorator(func):
            def wrapper(*args):
                args += ('Alvin',)  # 改变传入被注解方法的参数
                return func(*args)  # 调用被注解方法

            return wrapper

        @decorator
        def demo(no, name):
            return [no, name]

        self.assertEqual(demo(1001), [1001, 'Alvin'])

    def test_fix_function_name(self):
        """
        一个函数（方法）一旦被注解，则意味着该函数（方法）将会被注解返回的代理函数所取代，此时
        反射被注解函数和方法时，得到的信息实际上是代理函数的。
        functools.wraps注解的作用就是为代理方法指定被代理方法的实例，以期望在反射时能够得到
        真实函数（方法）的信息
        """

        def decorator1(func):
            """
            定义不带functools.wraps注解的代理函数
            """

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)  # 调用被注解函数

            return wrapper

        def decorator2(func):
            """
            定义带functools.wraps注解的代理函数
            """

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)  # 调用被注解函数

            return wrapper

        @decorator1
        def demo1():
            pass

        @decorator2
        def demo2():
            pass

        self.assertNotEqual(demo1.__name__, 'demo1')  # demo1函数的函数名不是"demo1"，而是代理函数的名称
        self.assertEqual(demo2.__name__, 'demo2')  # demo2函数虽然也被代理，但函数名称仍是"demo2"

    def test_cache_function_call(self):
        """
            对于同一个函数，如果输入参数相同，则返回值也一定相同，利用这一点，可以根据参数值将函数的返回值
        进行缓存，以达到提高运行效率的目的
            缓存可以通过注解来完成，这样代码可以保持非侵入性
        """

        def memo(fn):
            cache = {}  # 缓存函数返回值的字典
            miss = object()  # 表示缓存未命中的标志

            @functools.wraps(fn)
            def wrapper(*args):
                result = cache.get(args, miss)  # 根据参数获取缓存的返回值
                if result == miss:  # 判断是否命中缓存
                    result = fn(*args)  # 调用被标注函数，获取返回值
                    cache[args] = result  # 通过参数缓存本次调用的返回值
                return result

            return wrapper

        @memo
        def fib(n):
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)  # 递归调用，此时缓存机制会起作用

        self.assertEqual(fib(100), 354224848179261915075)

    def test_router(self):
        """
        可以使用类方法作为注解，注解方法和注解函数类似，但可以用于保存状态
        """

        class App:
            def __init__(self):
                self.__method_map = {}  # 保存被注解函数的字典

            def register(self, url):
                def wrapper(func):
                    """
                    代理方法，将被注解方法通过指定的url存入字典，并返回被注解方法本身
                    """
                    self.__method_map[url] = func
                    return func

                return wrapper

            def execute(self, url):
                """
                根据传入的url，在字典中查找对应的被注解方法，并执行该方法
                """
                fn = self.__method_map.get(url)
                if not fn:
                    raise Exception('function {:} not register'.format(str(url)))
                return fn()

        app = App()

        @app.register('/')
        def main_page():
            return 'The main page'

        @app.register('/next')
        def next_page():
            return 'The next page'

        self.assertEqual(app.execute('/'), 'The main page')
        self.assertEqual(app.execute('/next'), 'The next page')

        with self.assertRaises(Exception):
            app.execute('/prev')

    def test_use_log(self):
        """
        利用注解，可以以非侵入式代码完成“切面”式编程
        """

        # noinspection PyShadowingNames
        class Logger:
            def __init__(self):
                self.__io = io.StringIO()

            def __call__(self, fn):
                @functools.wraps(fn)
                def wrapper(*args, **kwargs):   # 代理方法，在调用被注解方法前后产生日志
                    start_time = time.time()
                    result = fn(*args, **kwargs)
                    end_time = time.time()
                    self.__io.write('function={:}\n'.format(fn.__name__))
                    self.__io.write('arguments={:} {:}\n'.format(args, kwargs))
                    self.__io.write('return={:}\n'.format(result))
                    self.__io.write('time={:.2f} sec'.format(end_time - start_time))
                    return result

                return wrapper

            def reset(self):
                self.__io.seek(0)

            def readline(self):
                return self.__io.readline()

        logger = Logger()

        @logger
        def multiply(x, y):
            return x * y

        start_time = time.time()
        multiply(10, 20)
        end_time = time.time()

        logger.reset()
        self.assertEqual(logger.readline(), 'function=multiply\n')
        self.assertEqual(logger.readline(), 'arguments=(10, 20) {}\n')
        self.assertEqual(logger.readline(), 'return=200\n')
        self.assertEqual(logger.readline(), 'time={:.2f} sec'.format(end_time - start_time))

    def test_wrapper_class_method(self):
        """
        如果要为类的方法设计注解函数，只需注意：
            被注解方法的第一个参数一定是其当前对象实例；
        """

        def not_empty(func):
            def wrapper(this, *args):
                """
                代理函数的第一个参数固定为被注解方法的当前对象实例，通过这个参数可以访问到被注解方法所属的对象
                """
                for arg in args:
                    if isinstance(arg, str):
                        if arg is None or len(arg) == 0:
                            raise Exception()
                return func(this, *args)

            return wrapper

        class A:
            @not_empty
            def test(self, name):
                return True

        a = A()
        self.assertTrue(a.test('Alvin'))
        self.assertTrue(a.test(None))

        with self.assertRaises(Exception):
            a.test('')





