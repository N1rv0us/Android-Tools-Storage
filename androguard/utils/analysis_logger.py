'''
    description : Logger 
    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''

def see_log(tag:str,content:str,level:str):
    isLog = False
    if isLog:
        print("[{0}] #{1}}# {2}".format(tag,level,content))

def errlog(tag:str,content:str):
    see_log(tag,content,"ERROR")

def warnlog(tag:str,content:str):
    see_log(tag,content,"WARN")

def infolog(tag:str,content:str):
    see_log(tag,content,"INFO")
