#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
    description: It is very important for static analysis to be able to extract APK file from the mobile phone
                 The script function includes obtaining the APK list in the mobile phone, and the function of downloading the APK according to the list
                 Functions are mainly extracted from feng's appstarter

    author: N1rv0us
    email: zhangjin9@xiaomi.com
'''
import os
import sys
import logging
import subprocess
import zipfile

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s [%(filename)s:%(lineno)d]: %(message)s')

def execShell(cmd,t=120):
    '''
    function : Run shell commands in the foreground
    param : cmd commond string
    ret : success -> {'d': DATA}; failed -> {'e':DATA}
    '''
    ret = {}
    try:
        r = subprocess.run(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True,encoding='utf-8',timeout=t)
        if r.returncode == 0:
            ret['d'] = r.stdout
        else:
            ret['e'] = r.stderr
    except subprocess.TimeoutExpired:
        ret['e'] = 'time out'
    
    return ret

def get_pkg_list(mfilter=''):
    '''
    function : Get a list of apps installed in the phone, Could set parameters to filter
    param : filter of package
    ret : pkg list
    '''
    list_cmd = 'adb shell pm list packages'
    grep_cmd = ' | grep '
    if mfilter != "":
        cmd = list_cmd+grep_cmd+mfilter
    else:
        cmd = list_cmd

    exec_ret = execShell(cmd)
    if 'e' in exec_ret.keys():
        logging.error(exec_ret['e'])
        return []
    else:
        ret_split = exec_ret['d'].split('\n')

    fp = open('result.txt','w')
    for pkg in ret_split:
        fp.write("{}\n".format(pkg[8:]))
    fp.close()

    return ret_split

def tool_pusher():
    '''
    function: Upload dex format conversion tool to /data/local/tmp directory.
    '''
    cdextool = 'cdex_converter64'
    vdextool = 'vdexExtractor64'
    push_path = '/data/local/tmp/'
    check_cmd = 'adb shell ls '+push_path
    dex_tmp_path = push_path+'apkpuller/'

    cmd = 'adb shell ls '+dex_tmp_path
    ret = execShell(cmd)
    if "No such file or directory" in str(ret):
        cmd = 'adb shell mkdir '+dex_tmp_path
        ret = execShell(cmd)
        if 'd' in ret.keys():
            logging.info('directory '+dex_tmp_path+" created success")
    else:
        logging.info(dex_tmp_path+" is already exists")

    ret = execShell(check_cmd+vdextool)
    logging.info(ret)
    if "No such file or directory" in str(ret):
        cmd = 'adb push ./tools/'+vdextool+" "+push_path
        ret = execShell(cmd)
        logging.info(ret)
        if 'd' in ret.keys():
            logging.info('push vdexExtractor success')
        cmd = 'adb shell "su -c \' chmod +x /data/local/tmp/'+vdextool+' \' " '
        ret = execShell(cmd)
        logging.info(ret)
    else:
        logging.info('vdexExtractor is already exist')

    ret = execShell(check_cmd+cdextool)
    logging.info(ret)
    if 'No such file or directory' in str(ret):
        cmd = 'adb push ./tools/'+cdextool+' '+push_path
        ret = execShell(cmd)
        logging.info(ret)
        if 'd' in ret.keys():
            logging.info('push cdex_converter64 success')
        cmd = 'adb shell "su -c \' chmod +x /data/local/tmp/'+cdextool+' \' " '
        ret = execShell(cmd)
        logging.info(ret)
    else:
        logging.info('cdex_converter64 is already exist')

def isDexExist(apk):
    '''
    funciton : Used to determine if there is dex in the APK file.
    '''
    zipf = zipfile.ZipFile(apk)
    if 'classes.dex' in zipf.namelist():
        return True
    else:
        return False

def isFileExist(file_path):
    '''
    function: Used to determine whether the target file exists
    '''
    cmd = "ls -l "+file_path
    ret = execShell(cmd)
    if "没有那个文件或目录" in str(ret):
        return False
    elif "No such file or directory" in str(ret):
        return False
    else:
        return True

def pull_apk(pkgName):
    '''
    function:Download the APK file from the phone according to the package name. If the dex is separated, the dex will be automatically merged into the APK file
    '''
    normal_app_path = "/data/data/"
    sys_app_path = "/system/app/"
    sys_app_path_ext = "/oat/arm64/"
    tool_path = '/data/local/tmp/'
    dex_tmp_path = tool_path+'apkpuller/'
    cdextool = 'cdex_converter64'
    vdextool = 'vdexExtractor64'

    tmp_path = './'
    out_path = tmp_path + 'apks/'+pkgName+'.apk'
    print(out_path)
    if isFileExist(out_path):
        logging.info("pkg "+pkgName+" is Exist")
        return
    
    cmd = "adb shell pm path "+pkgName
    ret = execShell(cmd)
    if ret['d'] == '':
        logging.info("Mobile phone does not contain APP named "+pkgName)
        return
    else:
        apk_path = ret['d'][8:-1]
   
    cmd = 'adb pull '+apk_path+' '+out_path
    ret = execShell(cmd)
    logging.info(cmd)
    if 'd' in ret.keys():
        logging.info("APK "+pkgName+" download success")
    else:
        logging.warning("APK "+pkgName+" download failed")
        return 
    
    if not isDexExist(out_path):
        if sys_app_path not in apk_path:
            logging.info("this APK "+pkgName+" does not contain dex files")
        else:
            tool_pusher()
            vdex_path = os.path.dirname(apk_path)+sys_app_path_ext+os.path.basename(apk_path)[:-4]+'.vdex'
            cmd = 'adb shell '+tool_path+vdextool+'  -f -i '+vdex_path+' -o '+dex_tmp_path
            ret = execShell(cmd)

            cmd = 'adb shell "ls '+dex_tmp_path+os.path.basename(apk_path)[:-4]+'_classes*.cdex | wc"'
            ret = execShell(cmd)
            count = 0
            cdex = False
            if 'd' in ret.keys():
                count = int(ret.get('d').rstrip('\n').split()[0])
            for i in range(0,count):
                cdex = True
                num = str(i+1)
                if num == '1':
                    num = ''
                cmd = 'adb shell '+tool_path+cdextool+' '+dex_tmp_path+os.path.basename(apk_path)[:-4]+'_classes'+num+'.cdex'
                ret = execShell(cmd)

            if count == 0:
                cmd = "adb shell ls "+dex_tmp_path+os.path.basename(apk_path)[:-4]+'_classes*.dex'
                execShell(cmd)
                if 'No such file' in str(ret):
                    logging.error('vdex to dex/cdex error')

            cmd = 'adb pull '+dex_tmp_path+' ./apks/tmp/'
            ret = execShell(cmd)
            cmd = 'adb shell rm -rf '+dex_tmp_path
            ret = execShell(cmd)

            zipf = zipfile.ZipFile(out_path,'a')
            ndex = False
            for f in os.listdir('./apks/tmp'):
                logging.info("analyze file : "+f)
                if cdex and 'new' in f and os.path.basename(apk_path)[:-4]+'_classes' in f:
                    zipf.write(os.path.join('./apks/tmp', f),f.split('_')[1].split('.')[0]+'.dex')
                    ndex = True
                elif not cdex and '.dex' in f and os.path.basename(apk_path)[:-4]+'_classes' in f:
                    zipf.write(os.path.join('./apks/tmp', f), f.split('_')[1])
            
            zipf.close()
            if not ndex and cdex:
                logging.error('cdex to dex error')
            
            cmd = 'rm -rf ./apks/tmp/*'
            execShell(cmd)

            return

if __name__ == "__main__":
    #print(get_pkg_list(mfilter='android'))
    #tool_pusher()
    #pull_apk('com.miui.powerkeeper')
    #pull_apk('com.android.provision')
    pull_apk('com.miui.analytics')
    #pull_apk('com.miui.cloudbackup')
    #pull_apk('com.miui.securitycore')
    #pull_apk('com.miui.securitycenter')