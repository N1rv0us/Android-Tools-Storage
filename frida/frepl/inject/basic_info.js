send("load agent.js DONE")

var mContext = null;
var mPs = null;
var tPkgInfo = null;
var tAppInfo = null;

rpc.exports = {
    setpackage : (pkgname) => Init(pkgname),
    components : (tag) => getComponents(tag),
    packageinfo : (tag) => getPackageInfo(tag),
    appinfo : (tag) => getApplicationInfo(tag),
    permission : () => getDefinesPermissions(),
    test : (str) => send(str)
}

const Init = (pkgname) => {
    return wrapJavaperform(() => {
        if (!mPs) {
            Java.choose("com.android.server.am.ActivityManagerService",{
                "onMatch": (instance) => {
                    mContext = instance.mContext.value;
                    send("[*] instance found " + instance.mContext.value);
                },
                "onComplete" : () => {
                    send("[*] finished Heap Search");
                }
            });
        
            mPs = mContext.getPackageManager();
        }

        var flags = PackageFlags.GET_ACTIVITIES | PackageFlags.GET_RECEIVERS | PackageFlags.GET_PROVIDERS | PackageFlags.GET_SERVICES | PackageFlags.GET_GIDS
                    | PackageFlags.GET_PERMISSIONS | PackageFlags.GET_CONFIGURATIONS | PackageFlags.GET_SHARED_LIBRARY_FILES;
        tPkgInfo = mPs.getPackageInfo(pkgname,flags);
        tAppInfo = tPkgInfo.applicationInfo.value;
    })
}

const getComponents = (TAG) => {
    return wrapJavaperform(() => {
        if (!mPs) {
            send("error : Please init first");
            return "Package Manager is None!";
        }

        var ret = new Array();
        if (TAG != "providers") {
            var components = tPkgInfo[TAG].value;
            for(let i = 0; i < components.length; i++) {
                var component = components[i];
                var name = component.name.value;
                var permission = component.permission.value;
                var exported = component.exported.value;

                ret[i] = {"name":name,"permission":permission,"exported":exported}
            }
        } else {
            var providers = tPkgInfo.providers.value;
            for(let i = 0; i < providers.length; i++) {
                var provider = providers[i];
                var authority = provider.authority.value;
                var exported = provider.exported.value;
                var name = provider.name.value;
                var multiprocess = provider.multiprocess.value;
                var readPermission = provider.readPermission.value;
                var writePermission = provider.writePermission.value;

                ret[i] = {
                    "authorithy" : authority,
                    "name" : name,
                    "exported" : exported,
                    "multiprocess" : multiprocess,
                    "readPermission" : readPermission,
                    "writePermission": writePermission
                }
            }
        }

        return JSON.stringify(ret);
    });
}

const getPackageInfo = (TAG) => {
    return wrapJavaperform(() => {
        try {
            var ret = tPkgInfo[TAG].value;
            if (typeof(ret) == "object") {
                var relist = new Array();
                for (let i = 0; i<ret.length; i++) {
                    relist[i] = ret[i].toString();
                }
                return relist;
            }
            return ret;
        } catch(e) {
            return "Not Found";
        }
    })
}

const getApplicationInfo = (TAG) => {
    return wrapJavaperform(() => { 
        try {
            var ret = tAppInfo[TAG].value;
            return ret;
        } catch(e) {
            return "Not Found";
        }
    })
}

const getDefinesPermissions = () => {
    return wrapJavaperform(() => {
        try {
            var permissions = tPkgInfo["permissions"].value;
            var retlist = new Array();
            for(let i = 0; i<permissions.length; i++) {
                var permission = permissions[i];
                var name = permission["name"].value;
                var protectLevel = permission.protectionToString(permission["protectionLevel"].value);

                retlist[i] = {"name":name,"protectLevel":protectLevel}
            }

            return JSON.stringify(retlist)
        } catch(e) {
            return "Not Found"
        }
    });
}

const wrapJavaperform = (fn) => {
    return new Promise((resolve,reject) => {
        Java.perform(() => {
            try {
                resolve(fn());
            } catch(e) {
                send(e);
                reject(e)
            }
        })
    });
};

const PackageFlags = {
    GET_ACTIVITIES : 0x00000001,
    GET_CONFIGURATIONS : 0x00004000,
    GET_DISABLED_COMPONENTS : 0x00000200,
    GET_GIDS : 0x00000100,
    GET_INSTRUMENTATION : 0x00000010,
    GET_INTENT_FILTERS : 0x00000020,
    GET_META_DATA : 0x00000080,
    MATCH_DEFAULT_ONLY : 0x00010000,
    GET_PERMISSIONS : 0x00001000,
    GET_PROVIDERS : 0x00000008,
    GET_RECEIVERS : 0x00000002,
    GET_RESOLVED_FILTER : 0x00000040,
    GET_SERVICES : 0x00000004,
    GET_SHARED_LIBRARY_FILES : 0x00000400,
    GET_SIGNATURES : 0x00000040,
    GET_URI_PERMISSION_PATTERNS : 0x00000800  
}

