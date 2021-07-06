'''
    description : Here we record some of the more common operations in the process of generating and handling ASTs, and each method has a corresponding description!
    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''
from androguard.decompiler.dad.decompile import DvMethod
from androguard.core.analysis.analysis import Analysis
from androguard.core.bytecodes.dvm import EncodedMethod

from androguard.misc import AnalyzeAPK
from pprint import pprint

###
# description : Gets the ast of the specified method 
#
###
def get_method_ast(dx:Analysis,method:EncodedMethod):
    method_analysis = dx.get_method(method)
    dv = DvMethod(method_analysis)
    dv.process(doAST=True)

    return dv.get_ast()

if __name__ == "__main__":
    a,d,dx = AnalyzeAPK("/Users/listennter/DailyWorking/apks/CloudService.apk")
#     ('com/miui/cloudservice/ui/ja$b',
#   'handleMessage',
#   '(Landroid/os/Message;)V')

    method = dx.get_method_by_name('Lcom/miui/cloudservice/ui/MiCloudHybridActivity$a;','shouldOverrideUrlLoading','(Lmiui/hybrid/HybridView; Ljava/lang/String;)Z')
    method = dx.get_method_by_name('Lcom/miui/cloudservice/ui/MiCloudHybridActivity;','b','(Lmiui/hybrid/HybridView; Ljava/lang/String;)Z')

    print(method)

    my_ast = get_method_ast(dx,method)
    pprint(my_ast)


