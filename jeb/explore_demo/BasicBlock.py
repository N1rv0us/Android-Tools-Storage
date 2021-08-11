# -*- coding: utf-8 -*- 

'''
Explore in a Basic Block;
Explore what we care about 

author : N1rv0us
email : zhangjin9@xiaomi.com

refer : https://github.com/acbocai/jeb_script/blob/main/samples/15%20IDexUnit-BasicBlock.py
'''

from com.pnfsoftware.jeb.client.api import IScript, IClientContext
from com.pnfsoftware.jeb.core import IRuntimeProject
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.controlflow import BasicBlock
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexMethodData, IDexCodeItem, IDalvikInstruction, IDexMethod


# CFG API Doc HERE : https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/core/units/code/android/controlflow/CFG.html
class BasicBlock(IScript):

    def run(self, ctx):
        assert isinstance(ctx,IClientContext)
        method_sign = "Lcom/anythink/basead/ui/web/WebLandPageActivity;->c()V"
        block_idx = 0

        my_project = ctx.getMainProject();                   assert isinstance(my_project,IRuntimeProject)
        dexUnit = my_project.findUnit(IDexUnit);             assert isinstance(dexUnit,IDexUnit)
        method = dexUnit.getMethod(method_sign);             assert isinstance(method,IDexMethod)
        methodData = method.getData();                       assert isinstance(methodData,IDexMethodData)
        methodCodeItem = methodData.getCodeItem();           assert isinstance(methodCodeItem,IDexCodeItem)

        print("<------------- Method Control Flow Graph HERE -------------------->")
        cfg = methodCodeItem.getControlFlowGraph()
        print("cfg class name : "+type(cfg).__name__)
        print("CFG functions list : ",dir(cfg))
        print("content : "+repr(cfg))

        print("")
        print("<------------- CFG Functions Call HERE --------------------------->")
        print("01 Block               >>> ",cfg.getBlocks())             # 基本快列表
        print("02 size                >>> ",cfg.size())                  # 块个数
        print("03 hasExit             >>> ",cfg.hasExit())               # 是否有出口
        print("04 getEntryBlock       >>> ",cfg.getEntryBlock())         # 入口块
        print("05 getExitBlocks       >>> ",cfg.getExitBlocks())         # 出口块(不唯一)
        print("06 getLast             >>> ",cfg.getLast())               # 最后一个块
        print("07 getAddressBlockMap  >>> ",cfg.getAddressBlockMap())    # map<偏移地址,块>
        print("08 getEndAddress       >>> ",hex(cfg.getEndAddress()))    # 结尾指令地址
        print("09 formatEdges         >>> ",cfg.formatEdges())           # 输出边(字符串)

        blockList = cfg.getBlocks()
        block = blockList[block_idx]
        print("")
        print("<  ----------------- Travel ing in an Block ------------------> ")
        print(type(block).__name__)
        
        print "01 getFirstAddress           >>> ", hex(block.getFirstAddress())      # 入口指令偏移
        print "02 getEndAddress             >>> ", hex(block.getEndAddress())        # 出口指令偏移
        print "03 getLast                   >>> ", block.getLast()                   # 最后一条指令
        print "04 getLastAddress            >>> ", hex(block.getLastAddress())       # 最后一条指令偏移
        print "05 size                      >>> ", block.size()                      # 指令条数
        print "06 getInstructions           >>> ", block.getInstructions()           # 指令序列

        print "07 allinsize                 >>> ", block.allinsize()                 # 前驱个数
        print "08 insize                    >>> ", block.insize()                    # 规则前驱个数
        print "09 irrinsize                 >>> ", block.irrinsize()                 # 不规则前驱个数

        print "10 alloutsize                >>> ", block.alloutsize()                # 后继个数
        print "11 outsize                   >>> ", block.outsize()                   # 规则后继个数
        print "12 irroutsize                >>> ", block.irroutsize()                # 不规则后继个数

        print "13 getAllInputBlocks         >>> ", block.getAllInputBlocks()         # 所有前驱块
        print "14 getInputBlocks            >>> ", block.getInputBlocks()            # 常规前驱块
        print "15 getIrregularInputBlocks   >>> ", block.getIrregularInputBlocks()   # 不规则前驱块

        print "16 getAllOutputBlocks        >>> ", block.getAllOutputBlocks()        # 所有后继块
        print "17 getOutputBlocks           >>> ", block.getOutputBlocks()           # 常规后继块
        print "18 getIrregularOutputBlocks  >>> ", block.getIrregularOutputBlocks()  # 不规则后继块