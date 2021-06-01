from agent import AppAgent
import os
import json


class AppUtils(AppAgent):
    def __init__(self,package_name):
        super().__init__()
        self.target = package_name
        self._package_name = "system_server"
        self.reslut_list = {}
        self._user_script_path = os.getcwd() + "/inject/basic_info.js"
        self._ready()

        self._api.setpackage(self.target)

    def my_message_handler(self,message,payload):
        pass

    def setTarget(self,package_name):
        self.target = package_name
        self.reslut_list = {}
        self._api.setpackage(self.target)

    def getAll(self):
        return self.reslut_list

    def getInfo(self):
        if "info" in self.reslut_list.keys():
            return self.reslut_list["info"]

        info = {}
        info["package"] = self._api.appinfo("packageName")
        info["process_name"] = self._api.appinfo("processName")
        info["version"] = self._api.packageinfo("versionName")
        info["data_directory"] = self._api.appinfo("dataDir")
        info["apk_path"] = self._api.appinfo("publicSourceDir")
        info["uid"] = self._api.appinfo("uid")
        info["gid"] = self._api.packageinfo("gids")
        info["shared_libraries"] = self._api.appinfo("sharedLibraryFiles")
        info["shared_user_id"] = self._api.packageinfo("sharedUserId")
        
        self.reslut_list["info"] = info

        return self.reslut_list["info"]

    def getPermissions(self):
        if "permissions" in self.reslut_list.keys():
            return self.reslut_list["permissions"]

        permissions = {}
        permissions["defines"] = json.loads(self._api.permission())
        permissions["uses"] = self._api.packageinfo("requestedPermissions")

        self.reslut_list["permissions"] = permissions

        return self.reslut_list["permissions"]

    def getComponent(self,TAG):
        if TAG not in self.reslut_list.keys():
            components = self._api.components(TAG)
            self.reslut_list[TAG] = json.loads(components)

    def getActivities(self,exported=True,filter=None):
        self.getComponent("activities")
        ret = []
        if exported == True:
            for activity in self.reslut_list["activities"]:
                if activity["exported"] == True:
                    ret.append(activity)
        else:
            ret = self.reslut_list["activities"]

        if filter != None:
            for activity in ret:
                if filter not in activity["name"]:
                    ret.remove(activity)

        return ret

    def getBroadcasts(self,exported=True,filter=None):
        self.getComponent("receivers")
        ret = []
        if exported == True:
            for receiver in self.reslut_list["receivers"]:
                if receiver["exported"] == True:
                    ret.append(receiver)
        else:
            ret = self.reslut_list["receivers"]

        if filter != None:
            for receiver in ret:
                if filter not in receiver["name"]:
                    ret.remove(receiver)

        return ret

    def getServices(self,exported=True,filter=None):
        self.getComponent("services")
        ret = []
        if exported == True:
            for service in self.reslut_list["services"]:
                if service["exported"] == True:
                    ret.append(service)
        else:
            ret = self.reslut_list["services"]

        if filter != None:
            for service in ret:
                if filter not in service["name"]:
                    ret.remove(service)

        return ret

    def getProviders(self):
        self.getComponent("providers")
        return self.reslut_list["providers"]
                


if __name__ == "__main__":
    my_apk = AppUtils("com.miui.personalassistant")
    print(my_apk.getInfo())
    permissions = my_apk.getPermissions()
    print("----- DEFINES PERMISSION -------")
    for perm in permissions["defines"]:
        print("- {0}".format(perm["name"]))
        print("|__ protect:{0}".format(perm["protectLevel"]))

    print("----- USES PERMISSION -------")
    for perm in permissions["uses"]:
        print("- {0}".format(perm))
