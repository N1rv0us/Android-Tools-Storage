from agent import AppAgent
import json
import os
from pprint import pprint

class PermCtrl(AppAgent):

    def __init__(self,package_name:str):
        super.__init__()
        self._package_name = package_name
        self._user_script_path = os.getcwd() + '/inject/permission.js'
        self.permission_list = set()
        self.obt_permission_list = set()

        self._ready()
        self._api.init()


    def my_message_handler(self, message, payload):
        return super().my_message_handler(message, payload)

    def get_perm_list(self) -> list:
        if len(self.permission_list) == 0:
            tmp = self._api.permlist()
            self.permission_list = set(tmp)

        return list(self.permission_list)

    def check_perm(self,permission:str) -> bool:
        return self._api.permcheck(permission)

    def authorized_permission_list(self) -> list : 
        self.obt_permission_list = set()
        if len(self.permission_list) == 0:
            self.get_perm_list()

        for idx,perm in enumerate(self.permission_list):
            tmp = self.check_perm(perm)
            if tmp == True:
                self.obt_permission_list.add(perm)

        return list(self.obt_permission_list)

    def unauthorized_permission_list(self) -> list:
        if len(self.obt_permission_list) == 0:
            self.authorized_permission_list()
        if len(self.permission_list) == 0:
            self.get_perm_list()

        return len(self.permission_list - self.obt_permission_list)

    def start_monitor(self):
        self._api.permctrl()

    
if __name__ == "__main__":
    pass