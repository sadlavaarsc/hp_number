# 最原始的基类，支持几种基本运算
# 这个类里的运算是严格限制的，例如都是要求同digit_num下进行
class hp_number_base(object):
    # 清空
    def clear(self):
        self.data.clear()
    # 粒度检验
    def same_digit_len(self,num):
        return self.digit_len==num.digit_len
    # 很常用的是否为0
    def is_zero(self):
        self.clear_zero()
        return len(self.data)==1 and self.data[0]==0

    # 基本的字符串转数字，数字转字符串
    def load_string(self,num:str):
        self.clear()
        #特判大小
        if num=='':
            self.data.append(0)
            return
        #符号判断，连用两个符号如++ --被认为是非法的
        if not num[0].isdigit():
            if len(num)==1:
                raise ValueError
            if num[0]=='+':
                self.sign=True
            if num[0]=='-':
                self.sign=False
            num=num[1:]
        if not num[0].isdigit():
            raise ValueError
        
        #取剩下的部分，这里选择按照这种划分顺序防止出现进位出现问题
        num=num[::-1]
        num_len=len(num)
        for i in range(0,len(num)//self.digit_len+1):
            try:
                self.data.append(int(num[i*self.digit_len:(i+1)*self.digit_len][::-1]))
            except ValueError:
                break
        
    def to_string(self):
        self.clear_zero()
        self.format_zero()
        tmp=self.data.copy()
        tmp.reverse()
        # 拼接并干掉前导0
        result=(''.join([str(e).zfill(self.digit_len) for e in tmp])).lstrip('0')
        if len(result)==0:
            result='0'
        return '-'+result if not self.sign and not self.is_zero() else result
    def __repr__(self):
        return self.to_string()
    # digit_len为压位高精长度，目前仍存在未知Bug
    def __init__(self,num='0',digit_len=9):
        self.digit_len=digit_len
        self.data=[]
        self.sign=True#正负号，True则正，False则负
        self.load_string(str(num))
    
    # copy，效果是返回自己的拷贝
    def copy(self):
        result=hp_number_base('0',self.digit_len)
        result.data=self.data.copy()
        result.sign=self.sign
        return result

    # 去除无效0，但是不会清理最后一个
    def clear_zero(self):
        for i in range(len(self.data)-1,0,-1):
            if self.data[i]==0:
                self.data.pop()
            else:
                break
    # 处理-0
    def format_zero(self):
        if len(self.data)==1 and not self.sign and self.data[0]==0:
            self.sign=True
    
    # 进位，参数index控制从第几位开始进位
    def up_format(self,index=0):
        digit_limit=10**(self.digit_len)
        # 如果这一位触发进位
        if self.data[index]>=digit_limit:
            cnum=self.data[index]//digit_limit
            self.data[index]%=digit_limit
            if index==len(self.data)-1:
                self.data.append(cnum)
            else:
                self.data[index+1]+=cnum
            # 触发了进位则一定要尝试进位下一位
            self.up_format(index+1)
        # 即使没有进位，不是最后一个就要尝试继续进位
        elif index<len(self.data)-1:
            self.up_format(index+1)
    # 退位，只能处理大减小
    def down_format(self,index=0):
        digit_limit=10**(self.digit_len)
        # 如果这一位触发退位
        if self.data[index]<0:
            if index==len(self.data)-1:
                self.data[index]*=-1
                self.sign^=True
            else:
                self.data[index]+=digit_limit
                self.data[index+1]-=1
                # 触发了退位则一定要尝试退位下一位
                self.down_format(index+1)
        # 即使没有退位，不是最后一个就要尝试继续退位
        elif index<len(self.data)-1:
            self.down_format(index+1)
    # 判断self是否大于等于、小于等于、等于num
    # 其中前两个只比较绝对值，为了避免反复互相调用
    def abs_greater_equal(self,num):
        if not self.same_digit_len(num):
            raise ValueError
        self.clear_zero()
        num.clear_zero()
        if len(self.data)!=len(num.data):
            return len(self.data)>len(num.data)
        for i in range(len(self.data)-1,-1,-1):
            if self.data[i]==num.data[i]:
                continue
            else:
                return self.data[i]>num.data[i]
        return True
    def abs_less_equal(self,num):
        if not self.same_digit_len(num):
            raise ValueError
        self.clear_zero()
        num.clear_zero()
        if len(self.data)!=len(num.data):
            return len(self.data)<len(num.data)
        for i in range(len(self.data)-1,-1,-1):
            if self.data[i]==num.data[i]:
                continue
            else:
                return self.data[i]<num.data[i]
        return True
    def __eq__(self,num):
        if not self.same_digit_len(num):
            raise ValueError
        self.clear_zero()
        num.clear_zero()
        # -0特判
        self.format_zero()
        num.format_zero()

        if self.sign!=num.sign or len(self.data)!=len(num.data):
            return False
        for i in range(len(self.data)-1,-1,-1):
            if self.data[i]!=num.data[i]:
                return False
        return True

    #加减数乘，类似于+= -= *= 
    #只支持绝对值加减，为了避免反复调用
    def abs_add(self,num):
        if not self.same_digit_len(num):
            raise ValueError
        # 清空前导0并对齐位数
        self.clear_zero()
        num.clear_zero()
        #只有左操作数太短需要处理
        if len(self.data)<len(num.data):
            self.data.extend([0]*(len(num.data)-len(self.data)))
        #各位相加，然后直接format
        for i in range(min(len(self.data),len(num.data))):
            self.data[i]+=num.data[i]
        self.up_format()
    
    def abs_sub(self,num):
        t1,t2=self.copy(),num.copy()
        if not t1.same_digit_len(t2):
            raise ValueError
        # 清空前导0并对齐位数
        t1.clear_zero()
        t2.clear_zero()
        #只有左操作数太短需要处理
        if len(t1.data)<len(t2.data):
            t1.data.extend([0]*(len(t2.data)-len(t1.data)))
        flag=False
        if t1.abs_less_equal(t2):
            t1,t2=t2,t1
            flag=True
        #各位相减，然后直接format
        for i in range(min(len(t1.data),len(t2.data))):
            t1.data[i]-=t2.data[i]
        t1.down_format()
        self.data=t1.data
        if flag:
            self.sign=False

    # 数乘，原则上k位数应该是小于digit_len
    # k>=1
    def nmul(self,k):
        if k<0:
            self.sign^=1
            k*=-1
        for i in range(0,len(self.data)):
            self.data[i]*=k
        self.up_format()
    # 10^n进制移位,一个提供给乘法的特别操作
    # 左移，指的是正常书写顺序的左移，也就是100变成1000这种左移
    def left_shift(self,k):
        self.data=[0]*k+self.data
    #右移
    def right_shift(self,k):
        del self.data[0:k]

# 实现业务逻辑的子类
class hp_number(hp_number_base):
    # 实现完整的业务逻辑
    # 重载copy以阻止各种基类子类冲突
    def copy(self):
        result=hp_number('0',self.digit_len)
        result.data=self.data.copy()
        result.sign=self.sign
        return result
    # 用于快速计算的*2和//2
    def mul2(self):
        #各位相加，然后直接format
        for i in range(len(self.data)):
            self.data[i]<<=2
        self.up_format()
    # 除会稍微麻烦一点，这里实现了一个类似退位的操作
    def div2(self):
        digit_limit=10**(self.digit_len)
        #这个是正数
        # 把所有奇数都进行退位
        for i in range(len(self.data)-1,0,-1):
            if self.data[i]&1:
                self.data[i-1]+=digit_limit
            self.data[i]>>=1
        if not self.sign and self.data[0]&1:
            self.data[0]>>=1
            self.data[0]+=1
        else:
            self.data[0]>>=1 
        self.up_format()

    # 支持各种复杂正负号的+-
    def add(self,num):
        #先判断符号，决定是正是负
        if self.sign==num.sign:
            self.abs_add(num)
        # 自己是正数，那就是减法
        elif self.sign:
            if num.abs_less_equal(self):
                self.sign=True
            else:
                self.sign=False
            self.abs_sub(num)
        elif num.sign:
            if num.abs_greater_equal(self):
                self.sign=True
            else:
                self.sign=False
            t=num.copy()
            t.abs_sub(self)
            self.data=t.data
    def sub(self,num):
        t=num.copy()
        t.sign^=1
        self.add(t)
    # 乘法
    def mul(self,num):
        # 先进行绝对值运算
        if not self.same_digit_len(num):
            raise ValueError
        # 这些赋值全都得用深拷贝
        t1=self.copy()
        result=hp_number_base('0',self.digit_len)
        for e in num.data:
            t2=t1.copy()
            t2.nmul(e)
            result.abs_add(t2)
            t1.left_shift(1)
        self.data=result.data
        # 计算符号
        self.sign=not (self.sign^num.sign)
    # 整除，思路类似手算，不过这里选择二分出商
    # 算出来的结果储存在self中，余数会return
    # 这里负数除法问题参考python的处理
    # raw div是只能处理同号乘除的除法（绝对值除法）
    def raw_div(self,num):
        # 特判
        if self.abs_less_equal(num) and not self==num:
            t=self.copy()
            self.clear()
            self.data.append(0)
            return t
        # 除0检验
        if num.is_zero():
            raise ZeroDivisionError
        t1,t2=num.copy(),self.copy()
        result=hp_number_base('0',self.digit_len)
        result.data=[0]*len(self.data)
        flag=False#计算完成的标志
        for i in range(len(self.data)-1,-1,-1):
            # 尝试二分寻找k使得k*num<=self
            l,r=0,10**(self.digit_len)
            m,goal=(l+r)>>1,0
            while l<=r:
                m=(l+r)>>1
                t3=t1.copy()
                t3.nmul(m)
                t3.left_shift(i)
                if t3==t2:
                    goal,flag=m,True
                    break
                if t3.abs_less_equal(t2):
                    l,goal=m+1,m
                else:
                    r=m-1
            result.data[i]=goal
            t3=t1.copy()
            t3.nmul(goal)
            t3.left_shift(i)
            t2.abs_sub(t3)
            if flag:
                break
        self.data=result.data
        self.clear_zero()
        t2.clear_zero()
        # 最后处理一下符号
        # python等语言中余数符号是取决于除数的
        t2.sign= self.sign
        self.sign=not (self.sign^num.sign)
        return t2
    # 结果符合python特点的除法，能够处理不同符号
    def div(self,num):
        if self.sign==num.sign:
            return self.raw_div(num)
        # 对不同符号进行处理，python的对负数的整除是更偏向x轴负方向的
        result=self.raw_div(num).copy()
        # 往x轴负方向修正
        if not result.is_zero():
            self.sub(hp_number_base('1',self.digit_len))
            # 这个正那另一个一定负数
            if result.sign==True:
                result.abs_sub(num)
            else:
                t=num.copy()
                t.abs_sub(result)
                result=t
        return result
    # 接下来重载一系列运算符，方便使用以及后续构造pow函数
    # 这个函数作用保护self进行运算
    def __safe_operator__(self,num,func):
        if type(num)!=hp_number:
            num=hp_number(num,self.digit_len)
        t1=self.copy()
        func(num)
        t2=self.copy()
        self.data,self.sign=t1.data.copy(),t1.sign
        return t2

    def __add__(self,num):
        return self.__safe_operator__(num,self.add)
    def __sub__(self,num):
        return self.__safe_operator__(num,self.sub)
    def __mul__(self,num):
        return self.__safe_operator__(num,self.mul)
    def __floordiv__(self,num):
        return self.__safe_operator__(num,self.div)
    def __mod__(self,num):
        if type(num)!=hp_number:
            num=hp_number(num,self.digit_len)
        return self.copy().div(num)
    def __ne__(self,num):
        if type(num)!=hp_number:
            num=hp_number(num,self.digit_len)
        return not self==num
    def __ge__(self,num):
        if type(num)!=hp_number:
            num=hp_number(num,self.digit_len)
        if self.sign==num.sign:
            return self.abs_greater_equal(num) if self.sign else self.abs_less_equal(num)
        return self.sign
    def __le__(self,num):
        if type(num)!=hp_number:
            num=hp_number(num,self.digit_len)
        if self.sign==num.sign:
            return self.abs_less_equal(num) if self.sign else self.abs_greater_equal(num)
        return not self.sign
    def __gt__(self,num):
        return self>=num and self!=num
    def __lt__(self,num):
        return self<=num and self!=num
    # 注意这两个左右移位和正常的左右移位定义是不一样的
    def __lshift__(self,k):
        if type(k)!=int:
            k=int(str(k))
        self.left_shift(k)
    def __rshift__(self,k):
        if type(k)!=int:
            k=int(str(k))
        self.right_shift(k)
    # 现在写幂运算很容易了，这里选择快速幂式的实现
    def pow(self,num):
        if not num.sign:
            raise ValueError
        a,n=self.copy(),num.copy()
        ans=hp_number(1,self.digit_len)
        while not n.is_zero():
            if n.data[0]&1:
                ans.mul(a)
            a.mul(a)
            n.div2()
        if len(num.data)>=1 and (not num.data[0]&1):
            ans.sign=True#偶数指数则特地更改正负
        self.sign,self.data=ans.sign,ans.data

    def __pow__(self,num):
        return self.__safe_operator__(num,self.pow)