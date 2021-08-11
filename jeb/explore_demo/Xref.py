# -*- coding: utf-8 -*-
'''
Explore for method xref in JEB
it is very useful and basic

author = N1rv0us
email = zhangjin9@xiaomi.com

refer : https://bbs.pediy.com/thread-263012.htm
        https://github.com/acbocai/jeb_script/blob/main/samples/61%20Dex-QUERY_XREFS.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.actions import ActionXrefsData, Actions, ActionContext
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexMethod,IDexClass

# 
class Xref(IScript):
    def run(self,ctx):
        method_sign = "Loversecured/ovaa/services/InsecureLoggerService;->getDumpFile(Landroid/content/Intent;)Ljava/io/File;"
        cls_sign = "Loversecured/ovaa/services/InsecureLoggerService;"

        self.instance = ctx
        self.project = ctx.getMainProject();                             assert isinstance(self.project,IRuntimeProject)
        self.dexUnit = self.project.findUnit(IDexUnit);                  assert isinstance(self.dexUnit,IDexUnit)
        my_cls = self.dexUnit.getClass(cls_sign);                        assert isinstance(my_cls,IDexClass)
        my_method = self.dexUnit.getMethod(method_sign);                 assert isinstance(my_method,IDexMethod)

        print("#### Fist TARGeT : Search the xref table of the method")
        print("#### USAGE : (unit,actions,address,itemid)  => Context for JEB Engine Executor")
        print("---------------------------------")
        actionXrefsData = ActionXrefsData()
        actionContext = ActionContext(self.dexUnit,Actions.QUERY_XREFS,my_method.getItemId(),None)
        if self.dexUnit.prepareExecution(actionContext,actionXrefsData):
            for xref_addr in actionXrefsData.getAddresses():
                print(repr(xref_addr))

        print("#### Second TARGET : Search the xref table of the whole class")
        print("-------------------------------")
        actionXrefsData = ActionXrefsData()
        actionContext = ActionContext(self.dexUnit,Actions.QUERY_XREFS,my_cls.getItemId(),None)
        if self.dexUnit.prepareExecution(actionContext,actionXrefsData):
            for xref_address in actionXrefsData.getAddresses():
                print(repr(xref_address))