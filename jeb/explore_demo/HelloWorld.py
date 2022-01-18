# -*- coding: utf-8 -*-
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit, IApkUnit

"""
my happy testing JEB script LABS

author : N1rv0us
email : zhangjin9@xiaomi.com
"""
class HelloWorld(IScript):
  def run(self, ctx):
    # For non-ASCII characters, remember to specify the encoding in the script header (here, UTF-8),
    # and do not forget to prefix all Unicode strings with "u", whether they're encoded (using \u or else) or not
    print('~~~\n' + u'Hello, 안녕하세요, 你好, こんにちは!\n' + 'This line was generated by a JEB Python script\n~~~')

    my_project = ctx.getMainProject()
    my_dex = my_project.findUnit(IDexUnit)
    my_apk = my_project.findUnit(IApkUnit)

    # for m in my_dex.getMethods():
    #   print(m.getSignature())

    print("APK debug status : "+str(my_apk.isDebuggable()))