from hp_number import *
import pytest
import random

ttime=10000

def test_division():
    for i in range(ttime):
        a=random.randint(-10000,10000)
        b=random.randint(-10000,10000)
        if b==0:
            b=1
        ha=hp_number(str(a))
        hb=hp_number(str(b))
        #$print(a,b)
        str(ha.div(hb))==str(a%b)     
        assert  str(ha)==str(a//b), f'{a=} {b=} {ha=} {hb=}'

def test_abs_sub():
    for i in range(ttime):
        a=random.randint(0,10000)
        b=random.randint(0,10000)
        ha,hb=hp_number(a),hp_number(b)
        hb.abs_sub(ha)
        assert str(hb)==str(b-a)

def test_add():
    for i in range(ttime):
        a=random.randint(-10000,10000)
        b=random.randint(-10000,10000)
        ha=hp_number(str(a))
        hb=hp_number(str(b))
        #$print(a,b)
        str(ha.add(hb))==str(a+b)     
        assert  str(ha)==str(a+b), f'{a=} {b=} {ha=} {hb=}'

def test_equal():
    for i in range(ttime):
        a=random.randint(-10000,10000)
        b=random.randint(-10000,10000)
        ha=hp_number(str(a))
        hb=hp_number(str(b))
        assert (ha==hb)==(a==b)
