# -*- coding: UTF-8 -*-

import subprocess

from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
import base64
import urllib2

from com.pnfsoftware.jeb.core.units.code.android.dex import DexPoolType, IDexMethod, IDexAddress
from com.pnfsoftware.jeb.core.units.code.java import IJavaCall, IJavaConstant, IJavaClass, IJavaField, IJavaMethod, \
    IJavaSourceUnit
from com.pnfsoftware.jeb.core.util import DecompilerHelper

"""
Script for JEB Decompiler. (Save as 'pdd.py')
"""


def exec_cmd(cmdline, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    # print(cmdline)
    try:
        subp = subprocess.Popen(cmdline, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        return None, None, None
    out, err = subp.communicate()
    normal = None
    error = None
    if out:
        normal = out.decode(errors='ignore')
    if err:
        error = err.decode(errors='ignore')
    return subp.returncode, normal, error


debug = False


def msg(msg):
    if debug:
        print(msg)


decrypt_methods = [
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/c;->a(Ljava/lang/String;)Ljava/lang/String;',
         'enc_args': [0]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->a(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->b(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->c(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->d(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->e(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->f(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->h(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->g(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         },
        {'name': 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/a;->i(Ljava/lang/String;Ljava/lang/String;)V',
         'enc_args': [0, 1]
         }
]



class pdd(IScript):

    # ctx: IClientContext or IGraphicalClientContext
    def run(self, ctx):
        print('\n\nstart found')
        self.file = open('pdd_enc_str_list.txt', 'wt')
        self.dec_str_index_list = set()
        self.mname_decrypt = 'Lcom/xunmeng/pinduoduo/lifecycle/proguard/c;->a(Ljava/lang/String;)Ljava/lang/String;'
        prj = ctx.getMainProject()
        dex = prj.findUnits(IDexUnit)[0]
        self.dex = dex
        # self.cstbuilder = prj.findUnits(IJavaSourceUnit)[0].getFactories().getConstantFactory()

        self.decomp = DecompilerHelper.getDecompiler(dex)
        self.cstbuilder = self.decomp.getASTFactories().getConstantFactory()

        for dec_method in decrypt_methods:
            self.dec_method(dex, dec_method['name'], dec_method['enc_args'])

        # referenceManager = dex.getReferenceManager()
        # print(ctx.getFocusedFragment().getActiveAddress())

        # if isinstance(dex, IDexUnit):
        #     # Lam_okdownload/DownloadTask$a;->a(I)Lam_okdownload/DownloadTask$a;
        #     # print(dex.getMethod('Lam_okdownload/DownloadTask$a;->a(I)Lam_okdownload/DownloadTask$a;'))
        #     decMethod = dex.getMethod(self.mname_decrypt)
        #     msg(decMethod)
        #     sum = 0
        #     dec_count = 0
        #     references = set()
        #     for addr in dex.getCrossReferences(DexPoolType.METHOD, decMethod.getIndex()):
        #         if isinstance(addr, IDexAddress):
        #             sum += 1
        #             r_method = str(addr).split('+')[0]
        #             if r_method in references:
        #                 continue
        #             references.add(r_method)
        #
        #             # javaMethod = decomp.decompileMethod(r_method)
        #
        #
        #             javaMethod = self.getDecompiledMethod(dex, r_method)
        #             if not javaMethod:
        #                 # print('The method was not found or was not decompiled')
        #                 continue
        #
        #             dec_count += 1
        #             self.decryptMethodStrings(javaMethod)
        #             # if dec_count == 100:
        #             #     break
        #
        #     print('sum {} dec count {}'.format(sum, dec_count))

        # referenceManager = dex.getReferenceManager()
        # for i in range(dex.getStringCount()):
        #     # print('string {}'.format(i))
        #     origStr = dex.getString(i)
        #     try:
        #         # print('string {} {} '.format(i, origStr))
        #         # base64.b64decode(str(origStr), validate=True)
        #         if is_base64_code(str(origStr)):
        #             print('string {} is base64 str'.format(origStr))
        #     except Exception as e:
        #         continue

        print('end found\n\n')

    def dec_method(self, dex, method_sig, enc_args):
        decMethod = dex.getMethod(method_sig)
        msg(decMethod)
        sum = 0
        dec_count = 0
        references = set()
        for addr in dex.getCrossReferences(DexPoolType.METHOD, decMethod.getIndex()):
            if isinstance(addr, IDexAddress):
                sum += 1
                r_method = str(addr).split('+')[0]
                if r_method in references:
                    continue
                references.add(r_method)

                javaMethod = self.getDecompiledMethod(dex, r_method)
                if javaMethod is None:
                    print('The method was not found or was not decompiled')
                    continue

                dec_count += 1
                self.decryptMethodStrings(javaMethod, method_sig, enc_args)
                # if dec_count == 10:
                #     break

        print('sum {} dec count {}'.format(sum, dec_count))

    def decryptMethodStrings(self, javaMethod, dec_method_sig, enc_args):
        block = javaMethod.getBody()

        msg('decryptMethodStrings {} {}'.format(javaMethod.getSignature(),block.size()))
        i = 0
        while i < block.size():
            stm = block.get(i)
            self.checkElement(block, stm, dec_method_sig, enc_args)
            i += 1

    def checkElement(self, parent, e, dec_method_sig, enc_args):
        if isinstance(e, IJavaCall):
            if e.getMethod() is None:
                print('error method is none')
                return
            mname = e.getMethod().getSignature()
            msg('checkElement call ' + mname)
            if mname == dec_method_sig:
                args = e.getArguments()
                for n in enc_args:
                    arg = args[n]
                    if isinstance(arg, IJavaConstant):
                        enc_str = arg.getString()
                        index = self.dex.findStringIndex(enc_str)
                        if index == -1 or index in self.dec_str_index_list:
                            continue
                        decrypted_string = self.decrypt(enc_str)
                        if decrypted_string is not None and decrypted_string != '':
                            # parent.replaceSubElement(e, self.cstbuilder.createString(decrypted_string))
                            # e.removeArgument(n)
                            # e.insertArgument(n, self.cstbuilder.createString(decrypted_string))
                            self.dec_str_index_list.add(index)
                            # 重新设值， 并且增加字符，防止和原来的一些常量字符串冲突
                            self.dex.getString(index).setValue('{} _-_'.format(decrypted_string))
                            msg('Decrypted string: %s' % repr(decrypted_string))

                        self.file.write('{} -----> {}\n'.format(decrypted_string, enc_str))


                    else:
                        msg('{} {} is not java constant'.format(dec_method_sig, n))

                # v = []
                # for arg in e.getArguments():
                #     if isinstance(arg, IJavaConstant):
                #         v.append(arg.getString())
                # if len(v) == 1:
                #     decrypted_string = self.decrypt(v[0])
                #     if decrypted_string is not None and decrypted_string != v[0]:
                #         # parent.replaceSubElement(e, self.cstbuilder.createString(decrypted_string))
                #         e.removeArgument(0)
                #         e.addArgument(self.cstbuilder.createString(decrypted_string))
                #         msg('Decrypted string: %s' % repr(decrypted_string))

        for subelt in e.getSubElements():
            if isinstance(subelt, IJavaClass) or isinstance(subelt, IJavaField) or isinstance(subelt, IJavaMethod):
                continue
            self.checkElement(e, subelt, dec_method_sig, enc_args)

    def getDecompiledMethod(self, dex, msig):
        msg('Decompiled method sig ' + msig)
        # m = self.decomp.getMethod(msig, False)
        # if m is not None:
        #     return m

        m = dex.getMethod(msig)
        if not m:
            return None

        c = m.getClassType()
        if not c:
            return None

        decomp = DecompilerHelper.getDecompiler(dex)
        if not decomp:
            return None

        csig = c.getSignature(False)
        javaUnit = decomp.decompile(csig)
        if not javaUnit:
            return None

        m = self.decomp.getMethod(msig, False)
        if m is not None:
            msg('found method {}'.format(msig))
            return m
        # msig0 = m.getSignature(False)
        # java_class = javaUnit.getClassElement()
        #
        #
        # m = self.find_method(java_class, msig0)

        # for m in javaUnit.getClassElement().getMethods():
        #     if m.getSignature() == msig0:
        #         return m
        return None



    def find_method(self, java_class, msig0):
        for m in java_class.getMethods():
            if m.getSignature() == msig0:
                return m

    def findEncStr(self, method):
        pass
        # if isinstance(method, IDexUnit):

    def decrypt(self, param):
        # print('found enc str ' + param)
        # print('"{}",'.format(param))
        rets = exec_cmd('curl http://127.0.0.1:8888/' + param)
        if rets[0] != 0:
            return None
        dec = rets[1]
        # response = urllib2.urlopen('http://127.0.0.1:8888/'+param)
        # dec = response.read()
        msg('{} dec {}'.format(param, dec))
        return dec
