# -*- coding: utf-8 -*- 

'''
Explore in a Single Method 
Normally, What do we pay attention to?

author : N1rv0us
email : zhangjin9@xiaomi.com

refer : https://github.com/acbocai/jeb_script/blob/main/samples/13%20IDexUnit-SingleMethod.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.units import IUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexMethodData, IDexCodeItem

### IDexMethod API Doc : https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/dex/IDexMethod.html
### IDexCodeItem API Doc : https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/dex/IDexCodeItem.html

class MethodInstance(IScript):

    def run(self, ctx):
        assert isinstance(ctx,IClientContext)

        method_sign = "Lcom/xiaomi/account/XiaomiOAuthResponse;-><clinit>()V"
        ins_idx = 10

        my_project = ctx.getMainProject()
        # print("###### IClientContext")
        # print(my_project.toString())
        # print(dir(my_project))
        dexUnit = my_project.findUnit(IDexUnit)
        # print("##### IDexUnit")
        # print(dexUnit.toString())
        # print(dir(dexUnit))

        method = dexUnit.getMethod(method_sign)
        print("############# Method Config ")
        print("repr : "+repr(method))

        print "1 ClassType         >>> ",method.getClassType()
        print "2 ReturnType        >>> ",method.getReturnType()
        print "3 getName           >>> ",method.getName()
        print "4 getSignature      >>> ",method.getSignature()
        print "5 getParameterTypes >>> "
        for parm in method.getParameterTypes():
            print ">>> ",parm
        print "6 isInternal        >>> ",method.isInternal()
        print "7 isArtificial      >>> ",method.isArtificial()
        print "-----------------------------------------------"

        dexMethodData = method.getData();    assert isinstance(dexMethodData,IDexMethodData)
        dexCodeItem = dexMethodData.getCodeItem(); assert isinstance(dexCodeItem,IDexCodeItem)

        print("###### Method instruction collection :")
        print "1 RegisterCount                    >>> ", dexCodeItem.getRegisterCount()
        print "2 InputArgumentCount               >>> ", dexCodeItem.getInputArgumentCount()
        print "3 OutputArgumentCount              >>> ", dexCodeItem.getOutputArgumentCount()
        print "4 ExceptionItems                   >>> ", dexCodeItem.getExceptionItems()
        print "5 InstructionsOffset               >>> ", dexCodeItem.getInstructionsOffset()
        print "6 InstructionsSize                 >>> ", dexCodeItem.getInstructionsSize()
        print "7 isCompleteBytecode               >>> ", dexCodeItem.isCompleteBytecode() 

        