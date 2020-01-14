'''程序的状态码'''

OK = 0


class LogicErr(Exception):
    code = None
    data = None

    def __init__(self, data=None):
        self.data = data or self.__class__.__name__  # 如果 data 为 None, 使用类的名字作为 data 值


def gen_logic_err(name, code):
    '''生成一个新的 LogicErr 的子类 (LogicErr 的工厂函数)'''
    return type(name, (LogicErr,), {'code': code})


SmsErr = gen_logic_err('SmsErr', 1000)                  # 短信发送失败
VcodeErr = gen_logic_err('VcodeErr', 1001)              # 验证码错误
LoginRequired = gen_logic_err('LoginRequired', 1002)    # 用户未登录
UserFormErr = gen_logic_err('UserFormErr', 1003)        # 用户表单数据错误
ProfileFormErr = gen_logic_err('ProfileFormErr', 1004)  # 用户资料表单错误
RepeatSwipeErr = gen_logic_err('RepeatSwipeErr', 1005)  # 重复滑动的错误
AreadyFriends = gen_logic_err('AreadyFriends', 1006)    # 两者已经是好友，无需重复添加
RewindLimited = gen_logic_err('RewindLimited', 1007)    # 当天反悔次数达到上限
RewindTimeout = gen_logic_err('RewindTimeout', 1008)    # 反悔超时
