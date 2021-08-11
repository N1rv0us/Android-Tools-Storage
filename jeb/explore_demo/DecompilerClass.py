# -*- coding: utf-8 -*-

''''
Try to use JEB python Script to decompile an Class

author : N1rv0us
email : zhangjin9@xiaomi.com

refer : https://github.com/acbocai/jeb_script/blob/main/samples/21%20IDexDecompilerUnit-decompile.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.units.code import DecompilationOptions, IDecompilerUnit, DecompilationContext
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit, IDexDecompilerUnit
from com.pnfsoftware.jeb.core.util import DecompilerHelper


# IDecompilerUnit API Doc :https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/IDecompilerUnit.html
# Something about UIContext(IGraphicalClientContext) : https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/client/api/IGraphicalClientContext.html
# this is very useful
class DecompilerClass(IScript):

    def run(self,ctx):
        assert isinstance(ctx,IClientContext)
        cls_sign = "Lcom/anythink/basead/ui/web/WebLandPageActivity;"
        method_sign = "Lcom/anythink/basead/ui/web/WebLandPageActivity;->c()V"

        my_project = ctx.getMainProject();                         assert isinstance(my_project,IRuntimeProject)
        dexUnit = my_project.findUnit(IDexUnit);                   assert isinstance(dexUnit,IDexUnit)
        my_decompiler = DecompilerHelper.getDecompiler(dexUnit);   assert isinstance(my_decompiler,IDecompilerUnit)

        opt = DecompilationOptions.Builder().newInstance().flags(IDecompilerUnit.FLAG_NO_INNER_DECOMPILATION|IDecompilerUnit.FLAG_NO_DEFERRED_DECOMPILATION).maxTimePerMethod(30000).build()


        # ### Decompiler an Single Class
        # ret = my_decompiler.decompileClass(cls_sign,DecompilationContext(opt))
        # print(ret)
        # text = my_decompiler.getDecompiledClassText(cls_sign)

        ### Decompiler an Single method
        ret = my_decompiler.decompileMethod(method_sign,DecompilationContext(opt))
        print("decompiler result : ",ret)
        text = my_decompiler.getDecompiledMethodText(method_sign)

        r = ctx.displayText("Decompiled N1rv0us", text, True)
        print(r)
