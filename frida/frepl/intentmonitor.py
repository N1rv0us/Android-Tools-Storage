from agent import AppAgent
import os
import json
from pprint import pprint


class IntentMonitor(AppAgent):

    def __init__(self,package_name):
        super().__init__()
        self._package_name = "system_server"
        self._user_script_path = os.getcwd() + "/inject/component.js"

        self.src = set()
        self.dst = set()

    # perfer to change
    def my_message_handler(self, message, payload):
        return super().my_message_handler(message, payload)


    # monitor package list set here
    def set_all_src(self,packages) : 
        self.src = set(packages)
        self._api.src(self.src)

    def add_src_package(self,package) : 
        self.src.add(package)
        self._api.src(self.src)

    def remove_src_package(self,package):
        try :
            self.src.remove(package)
            self._api.src(self.src)
            return True
        except:
            return False

    def get_src_list(self):
        return list(self.src)

    def set_all_dst(self,packages):
        self.dst = set(packages)
        self._api.dst(self.dst)

    def add_dst_package(self,package):
        self.dst.add(package)
        self._api.dst(self.dst)

    def remove_dst_package(self,package):
        try:
            self.dst.remove(package)
            self._api.dst(self.dst)
            return True
        except:
            return False

    def get_dst_list(self):
        return list(self.dst)

    ## monitor function launch here
    def launch_activity(self):
        self._api.activity()

    def launch_service(self):
        self._api.service()

    def launch_broadcast(self):
        self._api.broadcast()

    def launch_provider(self):
        self._api.provider()