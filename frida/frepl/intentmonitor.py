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

