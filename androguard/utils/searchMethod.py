'''
    descirption : To make it easier to get the EncodedMethod from the Androguard Analysis object
    author : N1rv0us
    mail : zhangjin9@xiaomi.com
'''
from androguard.core.analysis.analysis import Analysis
from androguard.core.bytecodes.dvm import EncodedMethod
from androguard.misc import AnalyzeAPK
from analysis_logger import *

def get_method_via_name(dx:Analysis,cls_name=None,method_name=None,description_name=None):
    if dx == None or cls_name == None or cls_name == ""\
        or method_name == None or method_name == "":
            errlog("GETMETHOD","Params Fault")
            return []

    if description_name != None:
        method = dx.get_method_by_name(cls_name,method_name,description_name)
        if method == None:
            errlog("GETMETHOD","target Method doesn't exist")
            return []
        return [method]

    ret = []
    my_cls = dx.classes[cls_name]
    if my_cls == None:
        errlog("GETMETHOD","couldn't find target class")
        return []

    for method in my_cls.get_methods():
        if method_name in method.name:
            ret.append(method)

    return ret

def get_method_analysis(dx:Analysis,method:EncodedMethod):
    return dx.get_method_analysis(method)




if __name__ == "__main__":
    a,d,dx = AnalyzeAPK("/Users/listennter/DailyWorking/2021-06-21/pdd-self-launch/weixin.apk")
    cls_name = "Lcom/tencent/mm/booter/d;"
    method_name = "d"
    print(repr(get_method_via_name(dx,cls_name,method_name)))