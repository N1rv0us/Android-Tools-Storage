from agent import AppAgent
import os 
import json 
from pprint import pprint

Debug = False
def printF(tag,content):
    global Debug
    if Debug:
        pprint('['+tag+']  : '+ content)

class AppStarter(AppAgent):
    def __init__(self,package_name=None):
        super().__init__()
        if package_name == None:
            printF("WARN","Initialization without setting the startup package name, Intent will start as system_server")
            self._package_name = "system_server"
        else:
            self._package_name = package_name

        self.result = None
        self.history = []
        self._user_script_path = os.getcwd() + '/inject/component_starter.js'

        self._ready()

    def my_message_handler(self, message, payload):
        return super().my_message_handler(message, payload)

    def startActivity(self,intent):
        printF("INFO","exec StartActivity : "+repr(intent))
        self._api.launchactivity(intent)
        self.history.append(intent)

    
    def startService(self,intent):
        printF("INFO","exec StartService : "+ repr(intent))
        self._api.startService(intent)
        self.history.append(intent)

    def sendBroadcast(self,intent):
        printF("INFO","exec SendBroadcast : "+ repr(intent))
        self._api.sendbroadcast(intent)
        self.history.apppend(intent)

    def interactProvider(self,args):
        self.result = None
        printF("INFO","exec Provider interact : " + repr(args))
        self.result = self._api.interactprovider(args)
        if self.result != None:
            tmp  = {"exec":args,"result":self.result}
        else :
            tmp = args

        self.history.append(tmp)

        return self.result

    def clearHistory(self):
        self.history = {}
        self.result = None


if __name__ == "__main__":
    my_starter = AppStarter()

    my_intent = open('./template/intent_example.json','r').read()
    target_package = json.loads(my_intent)["package_name"]
    my_starter.setTarget(target_package)
    my_starter.startActivity(my_intent)

    # intent template example is in ./template/intent_example.json
    # provider template example is in ./template/provider_example.json
        

