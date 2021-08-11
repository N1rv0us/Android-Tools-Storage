# -*- coding: utf-8 -*- 

'''
Explore what is in a DVM Instruction Object

author : N1rv0us
email : zhangjin9@xiaomi.com

refer : https://github.com/acbocai/jeb_script/blob/main/samples/14%20IDexUnit-Insn.py
'''

from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.units.code import IFlowInformation, IEntryPointDescription
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexMethod, IDexMethodData, IDexCodeItem, IDalvikInstruction 



# IDalvikInstruction API Doc : https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/dex/IDalvikInstruction.html
# IFlowInformation API Doc :  https://pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/IFlowInformation.html
# IInstructions API Doc HERE : https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/IInstruction.html
class DVMIns(IScript):

    def run(self, ctx):
        method_sign = "Lcom/anythink/basead/ui/web/WebLandPageActivity;->c()V"
        ins_idx = 61

        my_project = ctx.getMainProject();         assert isinstance(my_project,IRuntimeProject)
        dexUnit = my_project.findUnit(IDexUnit);   assert isinstance(dexUnit,IDexUnit)
        method = dexUnit.getMethod(method_sign);   assert isinstance(method,IDexMethod)
        methodData = method.getData();             assert isinstance(methodData,IDexMethodData)
        methodCodeItem = methodData.getCodeItem(); assert isinstance(methodCodeItem,IDexCodeItem)

        print("<------------ Travel in all opcode of CodeItem ------------>")
        for idx,insn in enumerate(methodCodeItem.getInstructions()):
            assert isinstance(insn,IDalvikInstruction)
            print(idx,hex(insn.getOffset()),insn.getMnemonic())


        insn = methodCodeItem.getInstructions()[ins_idx];     assert isinstance(insn,IDalvikInstruction)

        print("")
        print("<------------ Method in an IDexCodeItem Object --------->")
        # IDalvikInstruction  <-- ILocatedInstruction <-- IInstruction
        print(insn.__class__.__name__)
        print(dir(insn))


        print("")
        print("<------------ Hello Here is something about the instruction ------------>")
        print insn
        print "(01) getCode                      >>> ",insn.getCode()               # 二进制
        print "(02) getOpcode                    >>> ",insn.getOpcode()             # 操作码
        print "(03) getParameters:"                                                 # 指令操作数
        for a,b in enumerate(insn.getParameters()):
            print "<",a,">",b.getType(),b.getValue()
        print "(04) getParameterFirstIndexType   >>> ",insn.getParameterFirstIndexType()# 指令索引参数 池类型
        print "(05) getParameterSecondIndexType  >>> ",insn.getParameterSecondIndexType()
        print "(06) isPseudoInstruction          >>> ",insn.isPseudoInstruction()   # 伪指令
        print "(07) isSwitch                     >>> ",insn.isSwitch()
        print "(08) isArray                      >>> ",insn.isArray()
        print "(99) getSwitchData                >>> ",insn.getSwitchData()
        print "(10) getArrayData                 >>> ",insn.getArrayData()

        print "(11) getProcessorMode             >>> ",insn.getProcessorMode()          # 处理模式
        print "(12) getSize                      >>> ",insn.getSize()                   # 指令size
        print "(13) getPrefix                    >>> ",insn.getPrefix()                 # 指令可选前缀
        print "(14) getMnemonic                  >>> ",insn.getMnemonic()               # 助记符
        print "(15) getOperands                  >>> ",insn.getOperands()               # 操作数列表
        print "(16) canThrow                     >>> ",insn.canThrow()                  # 指令是否可以引发异常
        print "(17) isConditional                >>> ",insn.isConditional()             # 条件执行
        print("")


        # # 指令是否中断了执行流
        # print "(18) getBreakingFlow:"
        # iflowInformation = insn.getBreakingFlow();  assert isinstance(iflowInformation,IFlowInformation)


        
        # 指令是否分支(或调用)到子例程(和18一样的代码)
        print "(19) getRoutineCall:"
        iflowInformation = insn.getRoutineCall();  assert isinstance(iflowInformation,IFlowInformation)
        '''
        # 确定一条指令,是否间接分支(调用)子例程(和18一样的代码)
        print "(20) getIndirectRoutineCall:"
        iflowInformation = insn.getIndirectRoutineCall();  assert isinstance(iflowInformation,IFlowInformation)
        '''
        print "BreakingFlow.isBroken                >>> ",iflowInformation.isBroken()                       # 确定此对象是否包含流信息
        print "BreakingFlow.isBrokenUnknown         >>> ",iflowInformation.isBrokenUnknown()                # 确定此对象是否包含流信息，但没有已知的目标
        print "BreakingFlow.isBrokenKnown           >>> ",iflowInformation.isBrokenKnown()                  # 确定此对象是否包含流信息，目标已知
        print "BreakingFlow.mustComputeFallThrough  >>> ",iflowInformation.mustComputeFallThrough()         # 指示流信息是否包含一个直达地址
        print "BreakingFlow.getDelaySlotCount       >>> ",iflowInformation.getDelaySlotCount()              # 获取延迟槽中的指令数
        print "BreakingFlow.getTargets:"
        if iflowInformation.getTargets() is not None:
            for a,b in enumerate(iflowInformation.getTargets()):
                assert isinstance(b,IEntryPointDescription)
                print "<",a,">","BreakingFlow.getMode             >>> ",b.getMode()
                print "<",a,">","BreakingFlow.isUnknownAddress    >>> ",b.isUnknownAddress()
                print "<",a,">","BreakingFlow.getAddress          >>> ",b.getAddress()
        print("")