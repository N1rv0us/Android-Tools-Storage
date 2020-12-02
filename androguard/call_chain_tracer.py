#! /usr/local/bin/python3
# -*- coding:utf-8 -*-

'''
    description : Static data flow exploration scripting based on Androguard. v1.0
    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''

from androguard.misc import *

#######
# Config
#######
apk_path = "../apks/theme.apk" # Path of the APK to be analyzed
src_class = "Lcom/android/thememanager/activity/ThemeWebActivity;" # class name as a starting point
src_method = "onCreate" # method name as a staring point
max_depth = 30 # explore depth
back_trace = False # Specify the direction of explore. forward = False; back = True
counter = 0 # A global variable that keeps track of the number of paths searched. Do not modify unless you have special needs.
#######
# End Config
#######

def analyzer(a,d,dx):
    '''
    Entrance
    '''
    for meth in dx.classes[src_class].get_methods():
        if meth.name == src_method:
            my_recoder('info',"catch method : "+ src_method)
            trace_list = [meth.name]
            depth = 0
            do_trace(meth,trace_list,depth)

def do_trace(tmp_method,tracestack,depth):
    '''
    Path explorer through recursion
    '''
    global back_trace
    global max_depth
    if back_trace:
        ref = tmp_method.get_xref_from()
    else :
        ref = tmp_method.get_xref_to()

    if not ref or len(ref) == 0:
        # Leaf nodes, ending recursion
        stack_printer(tracestack)
        return 

    if depth >= max_depth:
        # Exceeds maximum exploration depth, records and exits
        my_recoder('warn',"=========== max depth explorer ===========")
        stack_printer(tracestack)
        return 

    for step_class,step_method,_ in ref:
        tmp = class_beauty(step_class.name)+":"+step_method.name
        if tmp in tracestack:
            # Explore the generated rings, record and exit
            my_recoder('warn',"=========== Ring Warning with method {0} ===========".format(tmp))
            stack_printer(tracestack)
            return
        else :
            tracestack.append(tmp)
        
        depth += 1
        do_trace(step_class.get_method_analysis(step_method),tracestack,depth)
        tracestack.pop()
        depth -= 1

    return 

def stack_printer(stack):
    '''
    Enter the contents of the current stack
    '''
    global counter
    global back_trace
    counter += 1
    my_recoder('info',"Now Printing Result {0}.".format(counter))
    if back_trace:
        arrows = "<-"
    else:
        arrows = "->"
    outer = arrows.join(stack)
    my_recoder('data',outer)

def class_beauty(class_name):
    '''
    Beauty the class name
    '''
    tmp = class_name
    tmp = tmp[1:-1]
    tmp = tmp.replace("/",".")
    return tmp

def my_recoder(tag,format_str):
    '''
    Unified data export, welcome to override as you wish!
    '''
    print(format_str)

if __name__ == "__main__":
    a,d,dx = AnalyzeAPK(apk_path)
    analyzer(a,d,dx)