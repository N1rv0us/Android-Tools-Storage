from flare_emu import *
from keystone import *
import flare_emu

eh = flare_emu.EmuHelper()
ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)

def patch(ea, reg, target, nop):
    nop_str = ''
    if nop:
        nop_str = ';nop'
    buf, count = ks.asm('add {}, pc, #{} {}'.format(reg, target - ea + 2, nop_str))
    for i in range(len(buf)):
        idaapi.patch_byte(ea + i, buf[i])
    # idaapi.patch_bytes(ea, buf)


# reg = 'R2'
def get_target(start, end, count, reg):
    eh.emulateRange(start, endAddr=end, count=count)
    return eh.getRegVal(reg)


def find_jump(ea):
    jump_ea = 0
    n = ea
    count = 0
    patch_addr = None
    nop = False
    while True:
        count += 1
        if idc.print_insn_mnem(n) == 'BX':
            reg = idc.get_operand_value(n, 0)
            jump_ea = n
            break
        n = idc.next_head(n)



    # 寻找一个修改点，需要4位长度
    n = ea
    set_target_addr = None
    while True:
        # LOAD:0000DD66                 ADDS.W          R4, R4, R12
        # LOAD:0000DD6A                 ADDS            R3, R3, R4
        # LOAD:0000DD6C                 MOVS            R0, #0xBE
        # LOAD:0000DD6E                 BX              R3
        # 找到最后一个修改跳转寄存器的地址

        if idc.print_insn_mnem(n).startswith('ADDS') and idc.get_operand_value(n, 0) == reg:
            set_target_addr = n
        # u = n
        n = idc.next_head(n)
        if n == jump_ea:
            break

        # if n - u == 4:
        #     patch_addr = u

    print('set_target_addr 0x{:x}'.format(set_target_addr))
    if set_target_addr:
            u = set_target_addr
            n = idc.next_head(u)
            # 4个字节长度，可以直接修改
            if n - u == 4:
                patch_addr = u
            else:
                # 需要从上一条指令找空间修复，上一条指令也是add, 并且是修改目标地址的

                # 一种情况
                # LOAD:0000E02C                 EORS            R0, R3
                # LOAD:0000E02E                 ADDS            R4, R4, R0
                # LOAD:0000E030                 MOVS.W          R10, #0xCC
                # LOAD:0000E034                 STR.W           R10, [R6]
                # LOAD:0000E038                 BX              R4

                reg_2 = idc.get_operand_value(u, 2)
                p = idc.prev_head(u)
                print('p 0x{:x} reg_2 {}'.format(p, reg_2))
                # if idc.print_insn_mnem(p).startswith('ADDS') and idc.get_operand_value(p, 0) == reg_2:
                if idc.get_operand_value(p, 0) == reg_2:
                    # 两个字节长度，加上之前的2个字节可以直接修改
                    if u - p == 2:
                        patch_addr = u - 2
                    elif u - p == 4:
                        # 4个字节长度的话，需要完全从上一个地址修改，后面的指令需要nop掉
                        patch_addr = p
                        nop = True
                    
    
    if not patch_addr:
        raise Exception('not found patch_addr {}'.format(patch_addr))

    return jump_ea, 'R{}'.format(reg), count, patch_addr, nop


if __name__ == '__main__':
    ea = idc.get_screen_ea()
    n, reg, count, patch_addr, nop = find_jump(ea)
    print('from 0x{:x} found jump call 0x{:x}, reg is {}, count {}, patch_addr 0x{:x} nop {}'.format(ea, n, reg, count, patch_addr, nop))
    target = get_target(ea + 1, n, count, reg)
    print('target 0x{:x}'.format(target))
    idaapi.auto_make_code(target - 1)
    patch(patch_addr, reg, target, nop)


# idc.add_func(here(), 0xDD2B)
