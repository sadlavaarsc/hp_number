# 个人作业3说明
# 个人作业3开发文档

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

实现一个hp_number_base基类，该类使用list储存数据，提供基本的进位、加法、减法、数乘转字符串、字符串转类等功能，随后，其一个派生类hp_number具体实现各种业务逻辑

代码迭代次数较多，此处不再详细解释遇到的问题和解决的办法，主要罗列代码注释以及当时出现的bug以及成因，并且对于涉及业务核心的函数标记了依赖关系，详情迭代情况见github仓库的提交日志。

代码概要如下：

```python
class hp_number_base(object):
    # 清空data恢复符号
    def clear(self):
        pass
    
    # 粒度检验,检查自己和num是否是同一压位精度的高精度数
    def same_digit_len(self, num):
        pass
    
    # 快速检查自己是否为0
    # 其中有一步是判断data长度是否为1，之前由于没有清除前导0导致这里出现了令人啼笑皆非的bug
    def is_zero(self):
        pass

    # 从一个字符串初始化高精度数，涉及到字符串分割等操作
    # 当初由于是倒序分割，导致压位100的情况下980这种数字会储存为98 0而不是9 80，导致进位错误
    # 此bug最终靠两次倒序修复
    def load_string(self, num: str):
        pass
	# 高精度数转字符串，用于输出
    def to_string(self):
        pass
	
    def __repr__(self):
        pass

    # digit_len为压位高精长度，为1则完全不压位
    def __init__(self, num='0', digit_len=1):
        self.digit_len=digit_len 
        self.data=[]# 储存数据本身
        self.sign=True#正负号，True则正，False则负
        self.load_string(str(num))#也就是正常加载数字

    # copy，效果是返回自己的拷贝，否则直接赋值会出现类似list直接赋值的问题
    def copy(self):
        pass

    # 去除前导0，但是不会清理最后一个（清除最后一个曾经是一个Bug）
    def clear_zero(self):
        pass

    # 规范化0的正负号，防止-0导致后续一些绝对值运算的bug
    def format_zero(self):
        pass

    # 绝对值的进位
    #简单来说就是逐个检查每一位是否需要进位
    def up_format(self):
        pass

    # 绝对值退位
    # 只能处理大减小的情况下的退位（也就是在数值本身为正的情况下的绝对值退位），将其误用于小减大的退位曾是一个bug
    def down_format(self):
        pass

    # 判断self是否大于等于、小于等于、等于num
    def abs_greater_equal(self, num):
        pass
    
    def abs_less_equal(self, num):
        pass

    def __eq__(self, num):
        pass

    # 绝对值加减，类似于+= -= 
    # 依赖：up_format
    def abs_add(self, num):
        pass
    
    # 虽然说这个叫绝对值减，但是准确的说这个的逻辑是处理正整数减法的逻辑，它的结果可能小于0
    # 依赖：down_format
    def abs_sub(self, num):
        pass

    # 数乘，原则上k位数应该是小于digit_len
    # k>=1，实现数乘是为后面实现乘法提供便利
    def nmul(self, k):
        pass

    # 10^n进制移位,一个提供给乘法的特别操作，避免数乘10带来的进位开销
    def left_shift(self, k):
        pass

    #右移
    def right_shift(self, k):
        pass
```

```python
class hp_number(hp_number_base):
    # 实现完整的业务逻辑
    # 重载copy以阻止各种基类子类冲突
    # 不重载copy会出现类似于self.copy()没有派生类元素的bug
    def copy(self):
        pass

    # 用于快速计算的*2和//2，主要是为了快速幂服务
    # 依赖：up_format
    def mul2(self):
        pass

    # 除会稍微麻烦一点，这里实现了一个类似退位的操作，
    # 之前对负数的除法存在部分bug
    # 依赖：down_format
    def div2(self):
        pass

    # 支持各种复杂正负号的+-
    # 依赖：abs_add，abs_sub，abs_less_equal
    def add(self, num):
        pass
	# 减法，简单来说就是把num符号取反然后调用add
    # 依赖:add
    def sub(self, num):
        pass

    # 乘法，原理是常规的手算思路
    # 依赖：nmul，up_format，left_shift
    def mul(self, num):
        pass

    # 整除，思路类似手算，不过这里选择二分出商
    # 算出来的结果储存在self中，余数会return
    # raw div是只能处理同号乘除的除法（绝对值的除法），结果会尽量偏向0
    # 依赖:left_shift，abs_sub，nmul，abs_less_equal，is_zero，same_digit_len，copy
    def raw_div(self, num):
        pass

    # 支持不同符号
    # 这里负数除法问题参考python的处理
    # 具体而言，这里会模仿python的“整除结果是除法的向下取整”这个特点，对负数情况下的商和余数进行修正
    # 依赖：raw_div，sub，abs_sub，copy
    def div(self, num):
        pass

    # 接下来重载一系列运算符，方便使用以及后续构造pow函数
    # 这个函数作用保护self进行运算，具体用途和实现可以参考代码
    def __safe_operator__(self, num, func):
        pass

    def __add__(self, num):
        pass

    def __sub__(self, num):
        pass

    def __mul__(self, num):
        pass

    def __floordiv__(self, num):
        pass

    def __mod__(self, num):
        pass

    def __ne__(self, num):
        pass

    def __ge__(self, num):
        pass

    def __le__(self, num):
        pass

    def __gt__(self, num):
        pass

    def __lt__(self, num):
        pass

    # 注意这两个左右移位和正常的左右移位定义是不一样的，这里指的是基类中的那种移位
    def __lshift__(self, k):
        pass

    def __rshift__(self, k):
        pass

    # 现在写幂运算很容易了，这里选择快速幂式的实现
    # 曾经这里存在某些情况下is_zero未清除前导零导致快速幂死循环的bug，已解决
    # 具体实现见代码
    # 依赖：较多（所以才放在最后实现），详见代码
    def pow(self, num):
        pass

    def __pow__(self, num):
        pass
```

最后再在外界调用对应接口实现需求

## 现状

已完成：压位高精运算，超出作业要求的运算类型和支持范围，重载了大部分运算符

To do list:

1. 尝试对代码进行性能优化和部分写法的重构，尤其尝试解决类型转换导致的性能问题
2. 允许不同压位精度的hp_number进行转换和运算
3. 调整部分接口使得使用压位高精变得更加便捷
4. 尝试增加定点数支持
