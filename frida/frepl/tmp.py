import os
import frida
import codecs

'''config'''
app_name = "system_server"
user_script_path = os.getcwd() + "/agent.js"
connect_type = "usb"
_device = None
_session = None
_script = None
_api = None
'''end config'''

def change_user_script(path):
    global user_script_path
    user_script_path = path

def obtain_user_script():
    f = codecs.open(user_script_path,"rb","utf-8")
    return f.read().rstrip("\r\n")

def my_message_handler(message,payload):
    if message["type"] == "send":
        print(message['payload'])

def start():
    global _device

    if connect_type == "remote":
        _device = frida.get_remote_device()
    elif connect_type == "usb":
        _device = frida.get_usb_device()

    pid = _device.get_process(app_name).pid
    _session = _device.attach(pid)
    _script = _session.create_script(obtain_user_script())

    _script.on("message",my_message_handler)
    _script.load()

    _api = _script.exports
    #_api.test("com.qiyi.video")
    _api.setpackage("com.miui.gallery")
    print(_api.appinfo("abd"))
    print(_api.packageinfo("requestedPermissions"))





if __name__ == "__main__":
    start()
    input()