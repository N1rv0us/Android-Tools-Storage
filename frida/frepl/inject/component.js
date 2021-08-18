console.log("")
const wrapJavaperform = (fn) => {
    return new Promise((resolve,reject) => {
        Java.perform(() => {
            try {
                resolve(fn());
            } catch(error) {
                send(error);
                reject(error);
            }
        });
    });
};

const back2py = (tag,obj) => {
    console.warn("catch ",tag," sending back");
    console.log(JSON.stringify(obj,null,'\t'));
}

var src_package_list = new Array();
var dst_package_list = new Array();

var Binder = null;
var ctx = null;
var pm = null;
var version = null;
var ComponentInfo = null;
var ResolveInfo = null;

rpc.exports = {
    init : () => envInit(),
    src : (packages) => setSrcPackage(packages),
    dst : (pacakges) => setDstPackage(pacakges),
    activity : () => hActivity(),
    broadcast : () => hBroadcast(),
    service : () => hService(),
    provider : () => hProvider(),
};

const envInit = () => {
    return wrapJavaperform(() => {
        Binder = Java.use("android.os.Binder");
        ComponentInfo = Java.use("android.content.pm.ComponentInfo");
        ResolveInfo = Java.use("android.content.pm.ResolveInfo");
        version = Java.use("android.os.Build$VERSION");
    
        Java.choose("com.android.server.am.ActivityManagerService",{
            "onMatch":function(instance) {
                ctx = instance.mContext.value;
            },
            "onComplete" : function() {
                
            }
        });
    
        pm = ctx.getPackageManager();   
    })
}

const setSrcPackage = (pkg_list) => {
    src_package_list = new Array();
    pkg_list.forEach(element => {
        src_package_list.push(element);
    });
};

const setDstPackage = (pkg_list) => {
    dst_package_list = new Array();
    pkg_list.forEach(element => {
        dst_package_list.push(element);
    });
};

const __queryComponent = (type,intent) => {
    var resolves = null;
    var resolveInfo = null;
    var componentInfo = null;

    switch(type) {
        case "activity":
            resolveInfo = pm.resolveActivity(intent,0);
            break;
        case "service":
            resolveInfo = pm.resolveService(intent,0);
            break;
        case "broadcast":
            resolves = pm.queryBroadcastReceivers(intent,0);
            if (resolves != null && resolves.size() > 1) {
                resolveInfo = Java.cast(resolves.get(0),ResolveInfo);
            }
            break;
        case "provider":
            componentInfo = pm.resolveContentProvider(intent,0);
            return componentInfo;
        default:
            break;
    }

    if (resolveInfo != null) {
        componentInfo = resolveInfo.getComponentInfo();
    }

    return componentInfo;
}

const __monitorPackage = (type,action,intent) => {
    var detail = '';
    var targetPackage = '';
    var targetComponent = '';

    var cpt_info = __queryComponent(type,intent);
    if (cpt_info != null) {
        targetPackage = cpt_info.packageName.value;
        targetComponent = cpt_info.name.value;
    }

    var uid = Binder.getCallingUid();
    var callingPackage = pm.getNameForUid(uid);

    if (src_package_list.indexOf(callingPackage) != -1 || dst_package_list.indexOf(targetPackage) != -1) {
        if (type != 'provider') {
            detail += intent.toUri(1);
        } else {
            detail = 'content://' + intent;
        }

        var back = {
            'action' : action,
            'caller' : callingPackage,
            'callee' : targetPackage,
            'call_component' : targetComponent,
            'intent' : detail
        }

        back2py(type,back);
    }
}

const hActivity = () => {
    return wrapJavaperform(() => {
        switch(version.SDK_INT.value) {
            case 28:
                
            case 29:
                Java.use("com.android.server.wm.ActivityTaskManagerService")
                .startActivityAsUser
                .overload('android.app.IApplicationThread', 'java.lang.String', 'android.content.Intent', 'java.lang.String', 'android.os.IBinder', 'java.lang.String', 'int', 'int', 'android.app.ProfilerInfo', 'android.os.Bundle', 'int', 'boolean')
                .implementation = function() {
                    __monitorPackage('activity','startActivity',arguments[2]);
                    return this.startActivityAsUser.apply(this,arguments);
                }
                break;
            case 30:
                Java.use('com.android.server.wm.ActivityTaskManagerService')
                .startActivityAsUser
                .overload('android.app.IApplicationThread', 'java.lang.String', 'java.lang.String', 'android.content.Intent', 'java.lang.String', 'android.os.IBinder', 'java.lang.String', 'int', 'int', 'android.app.ProfilerInfo', 'android.os.Bundle', 'int', 'boolean')
                .implementation = function() {
                    __monitorPackage('activity','startActivity',arguments[3]);
                    return this.startActivityAsUser.apply(this,arguments)
                }

                break;
            default:
                console.error("UnSupport SDK VERSION HERE");
                break;
        }
    })
}

const hBroadcast = () => {
    return wrapJavaperform(() => {
        switch(version.SDK_INT.value) {
            case 28:

            case 29:
                Java.use("com.android.server.am.ActivityManagerService")
                .broadcastIntent
                .implementation = function() {
                    __monitorPackage('broadcast','sendBroadcast',arguments[1]);
                    return this.broadcastIntent.apply(this,arguments);
                }
                break;
            case 30:
                Java.use("com.android.server.am.ActivityManagerService")
                .broadcastIntentWithFeature
                .implementation = function() {
                    __monitorPackage('broadcast','sendBroadcast',arguments[2]);
                    return this.broadcastIntentWithFeature.apply(this,arguments);
                }
                break;
            default:
                console.error("UnSupport SDK VERSION HERE ");
                break;
        }
    })
}

const hProvider = () => {
    return wrapJavaperform(() => {
        Java.use("com.android.server.am.ActivityManagerService")
        .getContentProvider
        .overload('android.app.IApplicationThread', 'java.lang.String', 'java.lang.String', 'int', 'boolean')
        .implementation = function() {
            __monitorPackage('provider','getProvider',arguments[2]);
            return this.getContentProvider.apply(this,arguments);
        }
    })
}

const hService = () => {
    return wrapJavaperform(() => {
        Java.use("com.android.server.am.ActivityManagerService")
        .startService
        .overload('android.app.IApplicationThread', 'android.content.Intent', 'java.lang.String', 'boolean', 'java.lang.String', 'java.lang.String', 'int')
        .implementation = function() {
            __monitorPackage('service','startService',arguments[1]);
            return this.startService.apply(this,arguments);
        }

        Java.use("com.android.server.am.ActivityManagerService")
        .bindIsolatedService
        .overload('android.app.IApplicationThread', 'android.os.IBinder', 'android.content.Intent', 'java.lang.String', 'android.app.IServiceConnection', 'int', 'java.lang.String', 'java.lang.String', 'int')
        .implementation = function() {
            __monitorPackage('service','bindService',arguments[2]);
            return this.bindIsolatedService.apply(this,arguments);
        }
    })
}


// set run here;
envInit();
setSrcPackage(['com.lbe.security.miui','com.miui.securitycenter']);
setDstPackage(['com.lbe.security.miui','com.miui.securitycenter']);
hActivity();
hService();
hBroadcast();
hProvider();