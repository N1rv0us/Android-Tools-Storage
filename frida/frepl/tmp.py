import os
import frida
import codecs

'''config'''
app_name = "com.android.settings"
user_script_path = os.getcwd() + "/tmp.js"
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

test_json_str = '''
{
    "package_name" : "com.android.settings",
    "activity_name" : "com.abd.ctcp",
    "action"  : "android.intent.action.SEND",
    "flags" : [
        "FLAG_ACTIVITY_NEW_TASK",
        "GRANT_WRITE_URI_PERMISSION"
    ],
    "extra": [
        {
            "type":"string",
            "key":"key",
            "value":"value"
        }
    ]
}
'''

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
    _api.launchactivity(test_json_str)





if __name__ == "__main__":
    start()
    input()