#! /usr/bin/python3
# -*- coding:utf-8 -*-

'''
    description : Extract information from the manifest file to find components that are protected with normal permissions
    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''
import json

from androguard.misc import *

from get_apk_analyze import my_apk_analyzer

PKG_EXIST = True
NS_ANDROID = "{http://schemas.android.com/apk/res/android}"
protect_level_list = {
    1 : "dangerous",
    20 : "development",
    0 : "normal",
    400 : "preinstalled",
    2 : "signature",
    3 : "signatureOrSystem",
    10 : "system"
}

def define_permission_collecter():
    '''
    collect infomation about app self-define permission
    '''
    ret = []

    for item in manifest.findall("permission"):
        tmp = {}
        name = item.get(NS_ANDROID + "name")
        level = item.get(NS_ANDROID + "protectionLevel") if None else "0"
        group = item.get(NS_ANDROID + "permissionGroup")

        tmp["name"] = name
        tmp["protect_level"] = protect_level_list[int(level,16)]
        tmp["permission_group"] = group

        ret.append(tmp)

    return ret

def component_collecter(tag):
    '''
    collect infomation about app's component
    '''
    ret = []
    find_tags = ["activity", "activity-alias", "service", "receiver", "provider"]
    if tag not in find_tags:
        return "TAG_NOT_SUPPORT"

    for item in application.findall(tag):
        tmp = {}
        name = item.get(NS_ANDROID + "name")
        exported = item.get(NS_ANDROID + "exported")
        permission = item.get(NS_ANDROID + "permission")

        if exported == None:
            sitem = item.find("intent-filter")
            if sitem == None:
                exported = "false"
            else:
                exported = "true"

        tmp["name"] = name
        tmp["exported"] = exported
        tmp["permission"] = permission
        if tag == "provider":
            # for providers
            write_permission = item.get(NS_ANDROID + "writePermission")
            read_permission = item.get(NS_ANDROID + "readPermission")

            tmp["read_permission"] = read_permission
            tmp["write_permission"] = write_permission

        ret.append(tmp)

    return ret

def verify():
    '''
    Determine the component protection security level
    '''
    define_permission_list = define_permission_collecter()
    activity_list = component_collecter("activity")
    activity_list += component_collecter("activity-alias")
    broadcast_list = component_collecter("receiver")
    service_list = component_collecter("service")
    provider_list = component_collecter("provider")

    vuln_list = []
    for activity in activity_list:
        if activity['exported'].lower() == "false":
            continue
        if activity['permission'] == None:
            continue

        for permission in define_permission_list:
            if permission['name'] == activity['permission'] and permission['protect_level'] == "normal":
                tmp = {}
                tmp['name'] = activity['name']
                tmp['permision'] = permission['name']
                tmp['tag'] = "ACTIVITY"

                vuln_list.append(tmp)

    for broadcast in broadcast_list:
        if broadcast['exported'].lower() == "false":
            continue
        if broadcast['permission'] == None:
            continue

        for permission in define_permission_list:
            if permission['name'] == broadcast['permission'] and permission['protect_level'] == "normal":
                tmp = {}
                tmp['name'] = broadcast['name']
                tmp['permission'] = permission['name']
                tmp['tag'] = "BROADCAST"

                vuln_list.append(tmp)

    for service in service_list:
        if service['exported'].lower() == "false":
            continue
        if service['permission'] == None:
            continue

        for permission in define_permission_list:
            if permission['name'] == service['permission'] and permission['protect_level'] == "normal":
                tmp = {}
                tmp['name'] = service['name']
                tmp['permission'] = permission['name']
                tmp['tag'] = 'SERVICE'

                vuln_list.append(tmp)

    for provider in provider_list:
        if provider['exported'].lower() == 'false':
            continue

        for permission in define_permission_list:
            if (permission['name'] == provider['read_permission'] or permission['name'] == provider['write_permission']) and permission['protect_level'] == "normal":
                tmp = {}
                tmp['name'] = service['name']
                tmp['permission'] = permission['name']
                tmp['tag'] = 'PROVIDER'

                vuln_list.append(tmp)

    return vuln_list

if __name__ == "__main__":
    global manifest,application
    target = "com.miui.home"
    a,d,dx = AnalyzeAPK("./apks/com.miui.home.apk")
    print(a)
    if a == None:
        PKG_EXIST = False
    else :
        manifest = a.get_android_manifest_xml()
        application = manifest.find("application")
    ret = verify()
    print(ret)