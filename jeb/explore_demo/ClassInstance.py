# -*- coding: utf-8 -*-

'''
How to get an class instance in JEB script 
And Happy Travel in an Class Object

author : N1rv0us
email : zhangjin9@xiaomi.com

reference : https://github.com/acbocai/jeb_script/blob/main/samples/11%20IDexUnit-DEX%20Class.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject, ILiveArtifact, IEnginesContext
from com.pnfsoftware.jeb.core.units import IUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit, IDexDecompilerUnit


## IDexClass API Doc : https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/dex/IDexClass.html
## IDexField API Doc : https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/dex/IDexField.html
class ClassInstance(IScript):

    def run(self,ctx):
        # input_path = "the/path/to/your/apk/file"
        # unit = ctx.open(input_path)

        print("N1rv0us ctx >>>>>>> "+repr(ctx))

        cls_sign = "com.xiaomi.account.XiaomiOAuthResponse"

        my_project = ctx.getMainProject()
        print("N1rv0us my_project >>>>> "+repr(my_project))

        dexUnit = my_project.findUnit(IDexUnit)
        print("N1rv0us dexUnit >>>>> "+repr(dexUnit))

        my_cls = dexUnit.getClass(cls_format(cls_sign))
        print("N1rv0us my_cls >>>>> "+repr(my_cls))

        print("N1rv0us >>>>> "+my_cls.getSignature())

        #### class travel
        num = 0
        print("#### Field split")
        for field in my_cls.getFields():
            num += 1
            print("field [{0}] >>>> {1}".format(num,field.getSignature()))

        num = 0
        print("#### Method split")
        for method in my_cls.getMethods():
            num += 1
            print("method [{0}] >>> {1}".format(num,method.getSignature()))

def cls_format(mcls):
    return 'L' + mcls.replace(".","/") + ';'