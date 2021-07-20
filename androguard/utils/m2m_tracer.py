#! usr/bin/python3
# -*- coding:utf-8 -*-

'''
   description : Path tracing from method to method based on androguard's xref implementation, 
                 similar to part of the functionality provided by Jandroid, 
                 supporting forward and reverse tracing

    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''

from androguard.core.analysis.analysis import Analysis, MethodClassAnalysis
from androguard.core.bytecodes.dvm import EncodedMethod
from androguard.misc import AnalyzeAPK
from enum import Enum

from pprint import pprint

class Xref(Enum):
    FROM = 0
    TO = 1

class M2MTracer:
    
    def __init__(self,dx:Analysis):
        # basic fileld
        self.dx = dx
        self.max_depth = 10
        self.xref = Xref.TO

        # config field
        self.isLog = False
        self.isRecord = False

        # start point field
        self.st_class_name = None
        self.st_method_name = None
        self.st_descriptor = None
        self.st_method_analysis = None

        # intercept point field
        self.intercept_methods = []

        # run cache field 
        self.traceback = []
        self.result = []
        self.full_recorder = []
        self.depth = 0

    def set_start_method(self,cls_name,method_name,descriptor):
        self.st_class_name = cls_name
        self.st_method_name = method_name 
        self.st_descriptor = descriptor

        try :
            enc_method = self.dx.get_method_by_name(self.st_class_name,self.st_method_name,self.st_descriptor)
            cls_analysis = self.dx.get_class_analysis(self.st_class_name)
            self.st_method_analysis = cls_analysis.get_method_analysis(enc_method)

            if self.st_method_analysis == None:
                raise Exception("MethodClassAnalysis Object is None")

            return True

        except :
            self.st_class_name = None
            self.st_method_name = None
            self.st_descriptor = None
            self.st_method_analysis = None

            self.printF("Error","Got MethodClassAnalysis Object Error")
            self.printF("Error","Method Message as follow : {class : "+ cls_name + "  method : "+method_name)

            return False

    def set_start_method_via_analysis(self,method_analysis:MethodClassAnalysis):
        self.st_method_analysis = method_analysis
        self.st_class_name = self.st_method_analysis.get_method().get_class_name()
        self.st_method_name = self.st_method_analysis.get_method().get_name()
        self.st_descriptor = self.st_method_analysis.get_method().get_descriptor()

        return True

    def set_xref(self,ref:Xref):
        self.xref = ref

    def set_depth(self,depth):
        self.max_depth = depth

    def enable_log(self,enable:bool):
        self.isLog = enable
    
    def enable_full_record(self,enable:bool):
        self.isRecord = enable

    def add_intercept_method(self,method:EncodedMethod):
        self.intercept_methods.append(method)

    def add_intercept_method_via_name(self,cls_name,method_name,descriptor):
        enc_method = self.dx.get_method_by_name(cls_name,method_name,descriptor)
        if enc_method == None:
            self.printF("ERROR","Got Method Failed")
        self.intercept_methods.append(enc_method)

    def remove_intercept_method(self,method:EncodedMethod):
        if len(self.intercept_methods) == 0:
            return False

        if method in self.intercept_methods:
            self.intercept_methods.remove(method)
            return True
        else:
            return False

    def remove_intercept_method_via_name(self,cls_name,method_name,descriptor):
        enc_method = self.dx.get_method_by_name(cls_name,method_name,descriptor)
        self.remove_intercept_method(enc_method)

    def get_result(self):
        if len(self.intercept_methods) == 0:
            return self.get_full_recorder()

        return self.result

    def get_full_recorder(self):
        if self.isRecord:
            return self.full_recorder
        else:
            return None

    def run(self):
        if not self._selfcheck():
            return False

        self._do_trace(self.st_method_analysis)

        return True

    def _selfcheck(self):
        if self.dx == None or self.st_method_analysis == None:
            # self.printF("Error","dx : "+repr(self.dx))
            # self.printF("Error","method analysis : "+repr(self.st_method_analysis))
            self.printF("Error","You have not completed the initialization")
            return False

        if len(self.intercept_methods) == 0:
            self.isRecord = True
            #self.printF("NOTICE","the intercept method list is null")

        if self.st_class_name == None or self.st_method_name == None:
            self.set_start_method_via_analysis(self.st_method_analysis)

        self.traceback = []
        self.result = []
        self.full_recorder = []
        self.depth = 0
        self.traceback.append(self.st_class_name+"->"+self.st_method_name)

        return True

    def _do_trace(self,method:MethodClassAnalysis):
        if self.xref == Xref.FROM:
            ref = method.get_xref_from()
        elif self.xref == Xref.TO:
            ref = method.get_xref_to()
        else:
            self.printF("Error","Error set in xref")
            return 

        if not ref or len(ref) == 0:
            self._pre_exit_trace()
            return 
        
        if self.depth > self.max_depth:
            self.printF("WARN","===== MAX DEPTH EXPLORE =====")
            self._pre_exit_trace()
            return

        for step_class,step_method,_ in ref:
            tmp = step_class.name + "->" + step_method.name
            if tmp in self.traceback:
                self.printF("WARN","===== RING WRAN WITH METHOD {0} =====".format(tmp))
                self._pre_exit_trace()
                return 
            else:
                self.traceback.append(tmp)

            flag = self._is_intercept(tmp)
            if flag:
                tmp_stack = list(self.traceback)
                pprint("[HERE]:"+str(tmp_stack))
                self.result.append(tmp_stack)
                if not self.isRecord:
                    self._pre_exit_trace()
                    return 

            self.depth += 1
            self._do_trace(step_class.get_method_analysis(step_method))
            self.traceback.pop()
            self.depth -= 1

        return          

    def _pre_exit_trace(self):
        self.printF("Info",str(self.traceback))
        if self.isRecord:
            tmp_stack = list(self.traceback)
            self.full_recorder.append(tmp_stack)

    def _is_intercept(self,target):
        if len(self.intercept_methods) == 0:
            return False
            
        tmp_cls,tmp_method = target.split("->")
        for item_method in self.intercept_methods:
            if item_method.get_class_name() == tmp_cls and \
                item_method.get_name() == tmp_method:
                return True

        return False



    def printF(self,tag,str):
        if self.isLog :
            pprint("[{0}] : {1}".format(tag,str))


if __name__ == "__main__":
    a,d,dx = AnalyzeAPK("/Users/listennter/DailyWorking/2021-07-04/shop_stealean_deeplink/fanqie.apk")
    my_tracer = M2MTracer(dx)
    st_cls = "Lcom/bytedance/sdk/openadsdk/downloadnew/a/b;"
    st_method = "q"
    st_descriptor = "()V"

    ed_cls = "Landroid/content/Context;"
    ed_method = "startActivity"
    ed_descriptor = "(Landroid/content/Intent;)V"
    my_tracer.set_start_method(st_cls,st_method,st_descriptor)

    my_tracer.add_intercept_method_via_name(ed_cls,ed_method,ed_descriptor)
    #my_tracer.set_xref(Xref.FROM)
    # pprint(my_tracer.intercept_methods)
    
    if my_tracer.run() == True:
        print("===== result here =====")
        pprint(my_tracer.get_result())
    else:
        print("Failed to Run. PLS Check The Log")

    #pprint(my_tracer.isRecord)