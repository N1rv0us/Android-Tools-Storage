import os
import codecs
import frida

class AppAgent():

    def __init__(self):
        self._package_name = ""
        self._user_script_path = ""
        self._connect_type = "usb"
        self.mode = "attach"
        self.pid = None
        self._device = None
        self._session = None
        self._script = None
        self._api = None

    def setTarget(self,package_name):
        self._package_name = package_name
        self.reload()

    def change_user_script(self,path):
        self._user_script_path = path

    def change_connect_type(self,type):
        self._connect_type = type

    def reload(self):
        self._clear()
        self._ready()

    def _clear(self):
        try:
            self._session.detach()
        except frida.OperationCancelledError:
            pass
        self.pid = None
        self._session = None
        self._script = None
        self._api = None

    def _obtain_user_script(self):
        f = codecs.open(self._user_script_path,"rb","utf-8")
        return f.read().rstrip("\r\n")

    def my_message_handler(self,message,payload):
        if message["type"] == "send":
            print(message["payload"])

    def _ready(self):
        if self._connect_type == "usb":
            self._device = frida.get_usb_device()
        elif self._connect_type == "remote":
            self._device = frida.get_remote_device()
        else:
            raise Exception("Connect Type is undefined")

        if self.mode == "attach":
            self.pid = self._device.get_process(self._package_name).pid
            self._session = self._device.attach(self.pid)
            self._script = self._session.create_script(self._obtain_user_script())
            
            self._script.on("message",lambda message,payload: self.my_message_handler(message,payload))
            self._script.load()
        elif self.mode == "spawn":
            self.pid = self._device.spawn(self._package_name)
            self._session = self._device.attach(self.pid)
            self._script = self._session.create_script(self._obtain_user_script())

            self._script.on("message",lambda message,payload: self.my_message_handler(message,payload))
            self._script.load()

            self._device.resume(self.pid)

        self._api = self._script.exports

