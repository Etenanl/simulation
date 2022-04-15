import Utility.MD5
import Utility.SHA256
# 工具类，存放hash方法

"""
单例模式，只存在一个对象，对外抛出Call（）函数，第一次调用时产生对象，

类中包含两个产生hash方法的对象，md5与sha256，对应相应的hash方法，也可以使用别的hash方法

不需要任何参数初始化，提供两个方法Call（）返回一个对象，Hash_Function()，调用hash方法

"""



class _Hash:
    # 可以写个单例模式实现，
    def __init__(self):
        self.md5 = Utility.MD5._MD5()
        self.sha256=Utility.SHA256._SHA256()

    # 调用返回这个类的对象
    def Call(self):
        pass

    # hash方法,value是输入的值，size是hash表大小，type输入hash方法，如”MD5“，”SHA256“
    def Hash_Function(self,value,size,type=""):
        pass