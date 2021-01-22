#! /usr/bin/python3
# -*- coding:utf-8 -*-

'''
    description : AndroidManifest filter for your own use.
    author : N1rv0us
'''

from androguard.misc import *
from get_apk_analyze import *
import argparse

format_header = "{http://schemas.android.com/apk/res/android}"
manifest_xml_tree = None

def get_manifest_xml_tree(pkg_name):
    '''
    Get Androguard's parsing results for Manifest files.
    '''
    global manifest_xml_tree
    a,d,dx = my_apk_analyzer(pkg_name)
    manifest_xml_tree = a.get_android_manifest_xml()

def permission_checker(pkg_name,permission=[]):
    '''
    Check the status of permission requests in APK files
    '''
    global format_header,manifest_xml_tree
    permission_key = format_header+"name"
    permission_tag = ['uses-permission','permission']
    if manifest_xml_tree == None:
        manifest_xml_tree = get_manifest_xml_tree(pkg_name)
    result_list = []
    if not permission:
        for item in manifest_xml_tree:
            if item.tag in manifest_xml_tree:
                result_list.append(item.attrib[permission_key])

        return result_list

    for item in manifest_xml_tree:
        for item.tag in manifest_xml_tree and \
            item.attrib[permission_key] in permission :
            result_list.append(item.attrib[permission_key])

    return result_list

def 
