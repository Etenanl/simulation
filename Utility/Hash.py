import Utility.MD5
import Utility.SHA256
# 工具类，存放hash方法

"""
单例模式，只存在一个对象，对外抛出Call（）函数，第一次调用时产生对象，

类中包含两个产生hash方法的对象，md5与sha256，对应相应的hash方法，也可以使用别的hash方法

不需要任何参数初始化，提供两个方法Call（）返回一个对象，Hash_Function()，调用hash方法

"""

class _Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class _Hash(_Singleton):
    # 可以写个单例模式实现，
    def __init__(self): 
        self.md5 = Utility.MD5._MD5()
        self.sha256 = Utility.SHA256._SHA256()

    # 调用返回这个类的对象
    def Call(self):
        return _Hash()
        #return self

    # hash方法, value是输入的值，size是hash表大小，type输入hash方法，如”MD5“，”SHA256“
    # value: (srcIP, dstIP, srcport, dstport, protocol) --> str
    def Hash_Function(self, value, size, type=""):
        value_str = ""
        for ele in value:
            value_str += str(ele)
        if type == "MD5":
            result_10 = int(self.md5.MD5_Hash(value_str), 16)           
        elif type == "SHA256":
            result_10 = int(self.sha256.SHA256_Hash(value_str), 16)

        result = result_10 % size
        return result

