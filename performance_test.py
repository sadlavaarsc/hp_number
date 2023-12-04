from hp_number import *
import time
import random
import sys


#自动的多次测试装饰器
def multi_test(test_time):
    def out_wrapper(func):
        def wrapper(*argv,**kargv):
            print(f'{func.__name__} test start')
            for i in range(test_time):
                func(*argv,**kargv)
            print(f'{test_time} tests completed')
            return func
        return wrapper
    return out_wrapper
            

def timer(func):
    def wrapper(*argv,**kargv):
        t1=time.time()
        result=func(*argv,**kargv)
        t2=time.time()
        print(f'{func.__name__} cost {t2-t1}s')
        return result
    return wrapper

# 测试字符串转数字与数字转字符串效率
@timer
@multi_test(test_time=100000)
def test_io():
    a=random.randint(-10000,10000)
    ha=hp_number(str(a))
    str(ha)
# 测试10000以内加法效率
@timer
@multi_test(test_time=100000)
def test_add():
    a=random.randint(-10000,10000)
    b=random.randint(-10000,10000)
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    ha+hb
@timer
@multi_test(test_time=100000)
def test_sub():
    a=random.randint(-10000,10000)
    b=random.randint(-10000,10000)
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    ha-hb
@timer
@multi_test(test_time=100000)
def test_mul():
    a=random.randint(-10000,10000)
    b=random.randint(-10000,10000)
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    ha*hb
@timer
@multi_test(test_time=100000)
def test_div():
    a=random.randint(-10000,10000)
    b=random.randint(-10000,10000)
    if b==0:
        b=1
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    ha//hb
@timer
@multi_test(test_time=1000000)
def test_pow():
    a=random.randint(-100,100)
    b=random.randint(1,100)
    if b==0:
        b=1
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    ha**hb


test_io()
test_add()
test_mul()
test_div()
test_pow()