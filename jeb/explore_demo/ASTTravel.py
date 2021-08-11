# -*- coding: utf-8 -*-

'''
test for obtain JAVA Class AST and JAVA Method AST
try some ways to obtain an JAVA AST struct

author : N1rv0us
email : zhangjin9@xiaomi.com

refer : https://github.com/acbocai/jeb_script/blob/main/samples/32%20IJavaSourceUnit-IJavaIf.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.units.code import IDecompilerUnit, DecompilationOptions, DecompilationContext, ICodeUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit, IDexDecompilerUnit
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit, IJavaStaticField, IJavaNewArray, IJavaConstant, IJavaCall, IJavaField, IJavaMethod, IJavaClass
from com.pnfsoftware.jeb.core.util import DecompilerHelper

# Some AST Statements API Doc (Look at Interface) : https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/java/ASTUtil.html

class ASTTravel(IScript):

    def run(self,ctx):
        assert isinstance(ctx,IClientContext); 
        self.project = ctx.getMainProject();                            assert isinstance(self.project,IRuntimeProject)
        self.dexUnit = self.project.findUnit(IDexUnit);                      assert isinstance(self.dexUnit,IDexUnit)

        sign = "Loversecured/ovaa/services/InsecureLoggerService;->getDumpFile(Landroid/content/Intent;)Ljava/io/File;"
        my_java_method = self.getJavaMethod(sign)
        assert isinstance(my_java_method,IJavaMethod)
        self.displayTree(my_java_method)

        #print(repr(my_java_method))

        # self.codeUnit = self.project.findUnit(ICodeUnit)
        # for unit in self.project.findUnits(IJavaSourceUnit):
        #     print("hhehehehe : ",unit.getClassElement().getName())


    def getJavaMethod(self,method_sign):
        my_decompiler = DecompilerHelper.getDecompiler(self.dexUnit);         assert isinstance(my_decompiler,IDexDecompilerUnit)
        opt = DecompilationOptions.Builder().newInstance().flags(IDecompilerUnit.FLAG_NO_DEFERRED_DECOMPILATION).build()
        ret = my_decompiler.decompileMethod(method_sign,DecompilationContext(opt))
        print("decompiler result : ",ret)

        return my_decompiler.getMethod(method_sign,False);  

    def displayTree(self,element, level=0):
        self.dispatch(element,level)
        if element:
            elts = element.getSubElements()
            for ele in elts:
                self.displayTree(ele,level+1) 

    def dispatch(self,element,level):
        # print(level,"<",element.getElementType(),"> >>>",element)  
        print("   "*level+repr(element)+'['+repr(element.getElementType())+']')              