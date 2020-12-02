#! /usr/bin/env python3 
# -*- coding:utf-8 -*-

'''
    description : Automatically configure mobile phone proxy, upload SSL certificate

    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''
import os
import sys
import logging
import subprocess

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

def pushCert(cert = ''):
    '''
    function : Upload the local certificate and mount it to the system
    param : certificate file path
    ret : Whether the certificate is imported successfully
    '''
    if cert == '':
        logging.error('No certificate file path specified')
        return False
    
    certs = cert.split(',')
    for cert in certs:
        cert = cert.strip()
        if os.path.isfile(cert):
            out = execShell('adb push '+cert+' /data/local/tmp')
            if '1 file pushed' not in str(out):
                logging.error('push cer error : '+str(out))
        else:
            logging.error('cert file error: '+cert)
            return False 

    out = execShell('adb shell ls -Z /system/etc/security/cacerts | head -n1') 
    conn = out.get('d')
    if conn:
        conc = conn.split(' ')
        for c in conc :
            if 'u:' in c:
                conn = c

    if not conn:
        logging.error('conn error')
        logging.error(out)
        return False

    out = ''
    out += str(execShell("adb shell 'su -c umount /system/etc/security/cacerts'"))
    out += str(execShell("adb shell 'su -c cp -pR /system/etc/security/cacerts /data/local/tmp/'"))

    for cert in certs:
        certname = os.path.basename(cert)
        out += str(execShell("adb shell 'su -c cp /data/local/tmp/"+certname+" /data/local/tmp/cacerts/'"))
    out += str(execShell("adb shell 'su -c chmod -R 755 /data/local/tmp/cacerts"))
    out += str(execShell("adb shell 'su -c chcon -R "+conn+" /data/local/tmp/cacerts'"))
    out += str(execShell("adb shell 'su -c mount /data/local/tmp/cacerts /system/etc/security/cacerts'"))

    out1 = execShell("adb shell mount")
    if "/system/etc/security/cacerts" not in str(out1):
        out += str(execShell("adb shell 'umount /system/etc/security/cacerts'"))
        out += str(execShell("adb shell 'cp -pR /system/etc/security/cacerts /data/local/tmp/'"))

        for cert in certs:
            certname = os.path.basename(cert)
            out += str(execShell("adb shell 'cp /data/local/tmp/"+certname+" /data/local/tmp/cacerts/'"))
        out += str(execShell("adb shell 'chmod -R 755 /data/local/tmp/cacerts"))
        out += str(execShell("adb shell 'chcon -R "+conn+" /data/local/tmp/cacerts'"))
        out += str(execShell("adb shell 'mount /data/local/tmp/cacerts /system/etc/security/cacerts'"))

        out1 = execShell('adb shell mount')
        if "/system/etc/security/cacerts" not in str(out1):
            logging.error('Certificate import failed : '+out)
            return False
        else:
            logging.info('Certificate import success')
            return True

    else:
        logging.info('Certificate import success')
        return True

def setProxy(ipport):
    '''
    function : Set up a global proxy
    param : exp -> 192.168.1.1:8080
    ret : whether the setting is successful
    '''
    logging.info("Using Proxy : "+ipport)
    out = execShell("adb shell settings put global http_proxy" + ipport)
    if "{'d': ''}" != str(out):
        logging.error('set Proxy failed:'+str(out))
        return False
    else:
        logging.info('set Proxy Success')
        return True

def delProxy():
    '''
    function : Clear the proxy settings and restart the phone
    '''
    execShell('adb shell settings delete global http_proxy')
    execShell('adb shell settings delete global global_http_proxy_host') 
    out = execShell('adb shell settings delete global global_http_proxy_host')

    if 'Deleted' in str(out):
        logging.info('The proxy has been reset, now restart the phone')
        execShell('adb reboot')
    else:
        logging.error('delete proxy failed')
        logging.error(out)


if __name__ == "__main__":
    certs="/Users/listennter/mine-git-storage/Android-Tools-Storage/androguard/cert/9a5ba575.0,/Users/listennter/mine-git-storage/Android-Tools-Storage/androguard/cert/c8750f0d.0"
    ret = pushCert(certs)
    print(ret)