# 个人作业3说明
## 需求明确
使用字符串非压位形式实现整数的 + - * // ** 五种计算

其中指数只要求非负整数，整除带余数

接口明确：
```python
def add(str1, str2): -> str
def sub(str1, str2): -> str
def mul(str1, str2): -> str
def div(str1, str2): -> (str, str) (商，余数)
def pow(str1, n): -> return str   #n为普通非负整数，不需要用list表示
```

## 架构设计
预计将会实现一个hp_number_base类，该类使用list储存数据，提供基本的进位、加法、减法、数乘转字符串、字符串转类等功能。

其中，数字倒序储存。

随后实现一个继承自hp_number_base的hp_number类，该类实现需求的全部功能并对外提供接口。

伪代码如下：
```python
class hp_number_base(object):
    # 清空
    def clear(self):
        ...
    # 基本的字符串转数字，数字转字符串
    def load_string(self,num:str):
        ...
    def to_string(self):
        ...
    # digit_len为压位高精长度
    def __init__(self,num='0',digit_len=1):
        self.digit_len=digit_len
        self.data=[]
        self.load_string(num)
    # 规范数字本身，如进位
    def format(self):
        ...
    #加减数乘，类似于+= -= *= 
    def add(self,num):
        ...
    def sub(self,num):
        ...
    def nmul(self,k):
        ...
```
```python
class hp_number(hp_number_base):
    #*=
    def mul(self,num):
        ...
    #比较值得注意的是这个会返回两个值，这个数字除了//=，还会return余数
    def div(self,num):
        ...
    def pow(self,num):
        ...
```
最后再在外界调用对应接口实现需求
