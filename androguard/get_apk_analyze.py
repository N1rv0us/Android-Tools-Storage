#! /usr/bin/python3
# -*- coding:utf-8 -*-

'''
    description : Unified management of Androguard analysis APKs, with reload sessions to reduce parsing time where possible
    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''

from androguard import misc
from androguard import session
from os.path import join,getsize
import os

###############
# Config
###############
apk_storage_path = "../apks/" # APKs Storage Paths
session_storage_path = "../sessions/" # Sessions Storage Paths
max_dir_size = 1024*1024*1024 
###############
# End Config
###############

def my_apk_analyzer(pkg_name):
    '''
    Get Androguard parsing results
    '''
    apk_name = pkg_name+'.apk'
    ag_name = pkg_name+'.ag'

    ag_storage = os.listdir(session_storage_path)
    if ag_name in ag_storage:
        sess = session.Load(session_storage_path+ag_name)
        a,d,dx = sess.get_objects_apk(apk_storage_path+apk_name)
        return a,d,dx

    apk_storage = os.listdir(apk_storage_path)
    if apk_name not in apk_storage:
        return None,None,None

    sess = misc.get_default_session()
    a,d,dx = misc.AnalyzeAPK(apk_storage_path+apk_name,session=sess)

    session.Save(sess,filename=session_storage_path+ag_name)

    return a,d,dx

def auto_sessions_clean():
    '''
    Regularly clean up stored session files to avoid excessive storage usage.
    '''
    global max_dir_size
    current_dir_size = get_dir_size(session_storage_path)
    if current_dir_size > max_dir_size:
        session_clean()

def session_clean(pkg=None):
    '''
    Clean up the session directory
    '''
    if pkg == None:
        filename = pkg+'.ag'
        os.remove(session_storage_path+filename)
    else:
        ag_storage = os.listdir(session_storage_path)
        for ag_file in ag_storage:
            os.remove(session_storage_path+ag_file)


def get_dir_size(dir):
    '''
    Get Folder Size
    '''
    size = 0
    for root,dirs,files in os.walk(dir):
        size += sum([getsize(join(root,name)) for name in files])

    return size 

#print(get_dir_size('./'))