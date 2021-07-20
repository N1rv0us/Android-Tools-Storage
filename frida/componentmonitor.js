var MonitorCallerPackages = ['com.dragon.read']
var MonitorTargetPackages = ['com.xiaomi.market']

var debug = false


var Throwable = null;
var JavaString = null;
var Charset = null;
var Binder = null
var mPms = null
var mContext = null
var ComponentInfo = null
var ResolveInfo = null
var VERSION = null 
Java.perform(function () {
    Throwable = Java.use("java.lang.Throwable");
    JavaString = Java.use('java.lang.String');
    Charset = Java.use('java.nio.charset.Charset');
    Binder = Java.use('android.os.Binder');
    ComponentInfo = Java.use('android.content.pm.ComponentInfo');
    ResolveInfo = Java.use('android.content.pm.ResolveInfo');
    VERSION = Java.use('android.os.Build$VERSION');

    // var LocalServices = Java.use("com.android.server.LocalServices")
    // var PackageManagerInternal = Java.use("android.content.pm.PackageManagerInternal")
    // mPms = Java.cast(LocalServices.getService(PackageManagerInternal.class), PackageManagerInternal)
    // console.log('found pms ' + mPms)

    Java.choose("com.android.server.am.ActivityManagerService", { 
         "onMatch":function(instance){
            mContext = instance.mContext.value
              console.log("[*] Instance found " + instance.mContext.value);
         },
         "onComplete":function() {
              console.log("[*] Finished heap search")
         }
    });
    mPms = mContext.getPackageManager()
    // console.log("settings " + mPms.resolveContentProvider("settings", 0).packageName.value)

    // String callingApp = context.getPackageManager().getNameForUid(Binder.getCallingUid());

});

function logDebug(msg) {
    if (debug) {
        console.log(msg)
    }
}

function MonitorPackage(cType, action, intent) {
    if (debug)
        logDebug('\nmonitor ' + action + ' ' + intent)
    var detail = ''
    var targetPackageName = ''
    var targetComponent = ''

    if (cType != 'provider') {
        var cpt = intent.getComponent()
        if (cpt != null) {
            targetPackageName = cpt.getPackageName()
            targetComponent = cpt.getClassName()
        } 

        if (targetPackageName == '' || targetPackageName == null ) {
            targetPackageName = intent.getPackage()
        }
    } 

    if (targetPackageName == '' || targetPackageName == null) {
        var cptInfo = queryComponent(cType, intent)
        if (cptInfo != null) {
            targetPackageName = cptInfo.packageName.value
            targetComponent = cptInfo.name.value
        }
    }

    var uid = Binder.getCallingUid()
    var callingPackage = mPms.getNameForUid(uid)

    if (debug || MonitorCallerPackages.indexOf(callingPackage) != -1 || MonitorTargetPackages.indexOf(targetPackageName) != -1) {
        if (cType != 'provider') {
            detail += intent.toUri(1);
        } else {
            detail = 'content://'+ intent
        }
        console.log(callingPackage + ' ' + action + ' ' + targetPackageName + ' /(' + targetComponent + ') : ' + detail + '\n')
    }

    return
}

function queryComponent(cType, intent) {
    if (debug)
        logDebug('query ' + cType + ' ' +  intent)
    var resolves = null
    var resolveInfo = null
    var componentInfo = null
    switch(cType) {
        case 'activity':
            // resolves = mPms.queryIntentActivities(intent, 0)
            resolveInfo = mPms.resolveActivity(intent, 0)
            break;
        case 'service':
            resolveInfo = mPms.resolveService(intent, 0)
            break;
        case 'broadcast':
            resolves = mPms.queryBroadcastReceivers(intent, 0)
            if (resolves != null && resolves.size() > 1) {
                resolveInfo = Java.cast(resolves.get(0), ResolveInfo)
                if (debug)
                    logDebug('found broadcast ' + resolveInfo)
            }
            break;
        case 'provider':
            componentInfo = mPms.resolveContentProvider(intent, 0)
            return componentInfo
            break;
        default:
            break
    }

    if (resolveInfo != null) {
        return resolveInfo.getComponentInfo()
    } 

    return componentInfo
}

/*
 * byte数组转字符串，如果转不了就返回byte[]
 * bytes:       字符数组
 * charset:     字符集(可选)
 */
function BytesToString(bytes, charset) {
    if (bytes !== undefined && bytes != null) {
        charset = charset || Charset.defaultCharset();
        var str = JavaString.$new.
            overload('[B', 'java.nio.charset.Charset').
            call(JavaString, bytes, charset).toString();
        try {
            return str.toString();
        } catch(e) {
            return null;
        }
    } else {
        return null;
    }
}

/*
 * 输出当前调用堆栈
 */
function PrintStack() {
    __PrintStack(Throwable.$new().getStackTrace());
};

/*
 * 调用当前函数，并输出参数返回值
 * object:      对象(一般直接填this)
 * args:   args(固定填这个)
 * show:        true/false(默认为false，可不填)
 */
function CallMethod(object, args, show) {
    if (Binder.getCallingUid() == 10229) {
        show = true
    } else {
        show = false
    }
    var stackElement = Throwable.$new().getStackTrace()[0];
    var method = __AdjustMethod(stackElement.getMethodName());
    return __CallMethod(stackElement, method, object, args, show);
};

/*
 * 打印栈，调用当前函数，并输出参数返回值
 * object:      对象(一般直接填this)
 * args:   args(固定填这个)
 * show:        true/false(默认为true，可不填)
 */
function PrintStackAndCallMethod(object, args, show) {
    show = show !== false;
    var stackElements = Throwable.$new().getStackTrace();
    var method = __AdjustMethod(stackElements[0].getMethodName());
    if (show) __PrintStack(stackElements);
    return __CallMethod(stackElements[0], method, object, args, show);
}

function __AdjustMethod(method) {
    if (method == "<init>") {
        method = "$init";
    }
    return method;
}

function __PrintStack(stackElements) {
    var body = "Stack: " + stackElements[0];
    for (var i = 0; i < stackElements.length; i++) {
        body += "\\n    at " + stackElements[i];
    }
    send({"frida_stack": body});
}

function __CallMethod(stackElement, method, object, args, show) {
    var argsStr = "";
    for (var i = 0; i < args.length; i++) {
        argsStr += "args[" + i + "],";
    }
    var ret = eval("object." + method + "(" + argsStr.substring(0, argsStr.length - 1) + ")");
    if (!show) {
        return ret;
    }
    var body = "Method: " + stackElement;

    body += "\n\t Caller: " + Binder.getCallingUid()

    for (var i = 0; i < args.length; i++) {
        body += "\n    Arguments[" + i + "]: " + args[i];
    }
    if (ret !== undefined) {
        body += "\n    Return: " + ret;
    }
    console.log(body)
    // send({"frida_method": body});
    return ret;
}

function ShowArgs(args) {
    var body = ''
    for (var i = 0; i < args.length; i++) {
        body += "\n    Arguments[" + i + "]: " + args[i];
    }
    console.log(body)
}

function HookAndroid9() {
    // https://cs.android.com/android/platform/superproject/+/android-9.0.0_r8:frameworks/base/core/java/android/app/IActivityManager.aidl
    logDebug(Java.use("com.android.server.am.ActivityManagerService"))
    var ActivityManagerService = Java.use("com.android.server.am.ActivityManagerService")
    var ActivityManagerServiceGetContentProviderFunc = ActivityManagerService.getContentProvider
    ActivityManagerServiceGetContentProviderFunc.implementation = function() {
        // .overload('android.app.IApplicationThread', 'java.lang.String', 'int', 'boolean')
        MonitorPackage('provider', 'getProvider', arguments[1])
        return ActivityManagerServiceGetContentProviderFunc.apply(this, arguments);
    }
    var ActivityManagerServiceBroadcastIntentFunc = ActivityManagerService.broadcastIntent
    ActivityManagerServiceBroadcastIntentFunc.implementation = function() {
        // .overload('android.app.IApplicationThread', 'android.content.Intent', 'java.lang.String', 'android.content.IIntentReceiver', 'int', 'java.lang.String', 'android.os.Bundle', '[Ljava.lang.String;', 'int', 'android.os.Bundle', 'boolean', 'boolean', 'int')
        MonitorPackage('broadcast', 'sendBroadcast', arguments[1])
        return ActivityManagerServiceBroadcastIntentFunc.apply(this, arguments);
    }
    var ActivityManagerServiceStartServiceFunc = ActivityManagerService.startService.overload('android.app.IApplicationThread', 'android.content.Intent', 'java.lang.String', 'boolean', 'java.lang.String', 'int')
    ActivityManagerServiceStartServiceFunc.implementation = function() {
        MonitorPackage('service', 'startService', arguments[1])
        return ActivityManagerServiceStartServiceFunc.apply(this, arguments);
    }
    var ActivityManagerServiceBindServiceFunc = ActivityManagerService.bindService
    ActivityManagerServiceBindServiceFunc.implementation = function() {
        // .overload('android.app.IApplicationThread', 'android.os.IBinder', 'android.content.Intent', 'java.lang.String', 'android.app.IServiceConnection', 'int', 'java.lang.String', 'int')
        MonitorPackage('service', 'bindService', arguments[2])
        return ActivityManagerServiceBindServiceFunc.apply(this, arguments)
    }

    var ActivityManagerServiceStartActivityAsUserFunc = ActivityManagerService.startActivityAsUser.overload('android.app.IApplicationThread', 'java.lang.String', 'android.content.Intent', 'java.lang.String', 'android.os.IBinder', 'java.lang.String', 'int', 'int', 'android.app.ProfilerInfo', 'android.os.Bundle', 'int', 'boolean')

    ActivityManagerServiceStartActivityAsUserFunc.implementation = function() {
        MonitorPackage('activity', 'startActivity', arguments[2])
        return ActivityManagerServiceStartActivityAsUserFunc.apply(this, arguments)
    }
}

function HookAndroid10() {
    var ActivityManagerService = Java.use("com.android.server.am.ActivityManagerService");

    var ActivityManagerServiceGetContentProviderFunc = ActivityManagerService.getContentProvider.overload('android.app.IApplicationThread', 'java.lang.String', 'java.lang.String', 'int', 'boolean')
    ActivityManagerServiceGetContentProviderFunc.implementation = function() {
        // .overload('android.app.IApplicationThread', 'java.lang.String', 'int', 'boolean')
        MonitorPackage('provider', 'getProvider', arguments[2])
        return ActivityManagerServiceGetContentProviderFunc.apply(this, arguments);
    }

    var ActivityManagerServiceBroadcastIntentFunc = ActivityManagerService.broadcastIntent
    ActivityManagerServiceBroadcastIntentFunc.implementation = function() {
        // ShowArgs(arguments)
        MonitorPackage('broadcast', 'sendBroadcast', arguments[1])
        return ActivityManagerServiceBroadcastIntentFunc.apply(this, arguments);
    }

    var ActivityManagerServiceStartServiceFunc = ActivityManagerService.startService
    ActivityManagerServiceStartServiceFunc.implementation = function() {
        MonitorPackage('service', 'startService', arguments[1])
        return ActivityManagerServiceStartServiceFunc.apply(this, arguments);
    }

    var ActivityManagerServiceBindServiceFunc = ActivityManagerService.bindIsolatedService.overload('android.app.IApplicationThread', 'android.os.IBinder', 'android.content.Intent', 'java.lang.String', 'android.app.IServiceConnection', 'int', 'java.lang.String', 'java.lang.String', 'int')
    ActivityManagerServiceBindServiceFunc.implementation = function() {
        MonitorPackage('service', 'bindService', arguments[2])
        return ActivityManagerServiceBindServiceFunc.apply(this, arguments)
    }

    // ActivityManagerService.registerReceiver.implementation = function() {
    //     ShowArgs(arguments)
    //     MonitorPackage('broadcast', 'registerReceiver', arguments[3])
    //     return CallMethod(this, arguments);
    // }

    var ActivityTaskManagerService = Java.use("com.android.server.wm.ActivityTaskManagerService");
    

    var ActivityTaskManagerServiceStartActivityAsUserFunc = ActivityTaskManagerService.startActivityAsUser.overload('android.app.IApplicationThread', 'java.lang.String', 'android.content.Intent', 'java.lang.String', 'android.os.IBinder', 'java.lang.String', 'int', 'int', 'android.app.ProfilerInfo', 'android.os.Bundle', 'int', 'boolean')

    ActivityTaskManagerServiceStartActivityAsUserFunc.implementation = function() {
        MonitorPackage('activity', 'startActivity', arguments[2])
        return ActivityTaskManagerServiceStartActivityAsUserFunc.apply(this, arguments)
    }

}

function HookAndroid11() {
    var ActivityManagerService = Java.use("com.android.server.am.ActivityManagerService");

    var ActivityManagerServiceGetContentProviderFunc = ActivityManagerService.getContentProvider.overload('android.app.IApplicationThread', 'java.lang.String', 'java.lang.String', 'int', 'boolean')
    ActivityManagerServiceGetContentProviderFunc.implementation = function() {
        MonitorPackage('provider', 'getProvider', arguments[2])
        return ActivityManagerServiceGetContentProviderFunc.apply(this, arguments);
    }

    var ActivityManagerServiceBroadcastIntentFunc = ActivityManagerService.broadcastIntentWithFeature
    ActivityManagerServiceBroadcastIntentFunc.implementation = function() {
        MonitorPackage('broadcast', 'sendBroadcast', arguments[2])
        return ActivityManagerServiceBroadcastIntentFunc.apply(this, arguments);
    }

    var ActivityManagerServiceStartServiceFunc = ActivityManagerService.startService
    ActivityManagerServiceStartServiceFunc.implementation = function() {
        MonitorPackage('service', 'startService', arguments[1])
        return ActivityManagerServiceStartServiceFunc.apply(this, arguments);
    }

    var ActivityManagerServiceBindServiceFunc = ActivityManagerService.bindIsolatedService.overload('android.app.IApplicationThread', 'android.os.IBinder', 'android.content.Intent', 'java.lang.String', 'android.app.IServiceConnection', 'int', 'java.lang.String', 'java.lang.String', 'int')
    ActivityManagerServiceBindServiceFunc.implementation = function() {
        MonitorPackage('service', 'bindService', arguments[2])
        return ActivityManagerServiceBindServiceFunc.apply(this, arguments)
    }

    // ActivityManagerService.registerReceiverWithFeature.implementation = function() {
    //     MonitorPackage('broadcast', 'registerReceiver', arguments[3])
    //     return CallMethod(this, arguments);
    // }
    var ActivityTaskManagerService = Java.use("com.android.server.wm.ActivityTaskManagerService");

    var ActivityTaskManagerServiceStartActivityAsUserFunc = ActivityTaskManagerService.startActivityAsUser.overload('android.app.IApplicationThread', 'java.lang.String', 'java.lang.String', 'android.content.Intent', 'java.lang.String', 'android.os.IBinder', 'java.lang.String', 'int', 'int', 'android.app.ProfilerInfo', 'android.os.Bundle', 'int', 'boolean')

    ActivityTaskManagerServiceStartActivityAsUserFunc.implementation = function() {
        MonitorPackage('activity', 'startActivity', arguments[3])
        return ActivityTaskManagerServiceStartActivityAsUserFunc.apply(this, arguments)
    }

}

Java.perform(function () {
    switch(VERSION.SDK_INT.value) {
        case 28:
            HookAndroid9()
            break
        case 29:
            HookAndroid10()
            break
        case 30:
            HookAndroid11()
            break
        default:
        break
    }
    console.log('start')
});