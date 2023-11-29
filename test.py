from personal_homework3 import *
import pytest
import random

a,b=hp_number('-5177'),hp_number('-7423')
#a,b=hp_number('334'),hp_number('225')
print(a.div(b),a,-5177//-7423,-5177%-7423)

def fast_test():
    a=random.randint(-10000,-1)
    b=random.randint(-10000,-1)
    if b==0:
        b==1
    ha=hp_number(str(a))
    hb=hp_number(str(b))
    
    assert  str(ha.div(hb))==str(a%b) and str(ha)==str(a//b), f'{a=} {b=} {ha=} {hb=}'
def test_func():
    for i in range(10000):
        fast_test()