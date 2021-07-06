send("load compontent starter .js success");

var fd = null;

rpc.exports = {
    launchactivity : (intent) => ActivityLauncher(intent),
    startservice : (intent) => ServiceStarter(intent),
    sendbroadcast : (intent) => BroadcastSender(intent),
    interactprovider : (args) => InteractProvider(args),
    tmp : (str) => parseString(str)
}

const getApplicationContext = () => {
    const ActivityThread = Java.use("android.app.ActivityThread");
    const currentApplication = ActivityThread.currentApplication();

    return currentApplication.getApplicationContext();
}

const ActivityLauncher = (intent) => {
    return wrapJavaperform(() => {
        var newIntent = parseIntent(intent);
        const context = getApplicationContext();

        send(newIntent.toURI());
        context.startActivity(newIntent);
        send("Activity successfully asked to start");
    })
}

const ServiceStarter = (intent) => {
    return wrapJavaperform(() => {
        var newIntent = parseIntent(intent);
        const context = getApplicationContext();

        send(newIntent.toURI());
        context.startService(intent);
        send("start Service success");
    })
}

const BroadcastSender = (intent) => {
    return wrapJavaperform(() => {
        var newIntent = parseIntent(intent);
        const context = getApplicationContext();

        send(newIntent.toURI());
        context.sendBroadcast(context);
        send("send Broadcast Success");
    })
}

const InteractProvider = (args) => {
    var ret = null;
    var tmp = null;
    wrapJavaperform(() => {
        const Uri = Java.use("android.net.Uri");
        const resolver = getApplicationContext().getContentResolver();

        const args_json = JSON.parse(args);
        const uri = Uri.parse(args_json.uri);
        const params = args_json.params;
        const type = args_json.action;

        switch(type) {
            case "query" :
                const selection = params.selection;
                const sortOrder = params.sortOrder;
                const projection_list = params.projection;
                const selectionArgs_list = params.selectionArgs;

                var projection = null;
                var selectionArgs = null;

                if (projection_list != null) {
                    var my_list = new Array();
                    projection_list.forEach((element) => {
                        my_list.push(element)
                    })
                    projection = Java.array("java.lang.String",my_list);
                }

                if (selectionArgs_list != null) {
                    var my_list = null;
                    selectionArgs_list.forEach((element) => {
                        my_list.push(element)
                    })
                    selectionArgs = Java.array("java.lang.String",my_list);
                }

                tmp = resolver.query(uri,projection,selection,selectionArgs,sortOrder);
                ret = {
                    "status":"success",
                    "action":"query",
                    "content":JSON.stringify(tmp)
                }
                break;
            case "openFile" :
                const mode = params.mode;
                fd = resolver.openFile(uri,mode,null);
                ret = {
                    "status":"success",
                    "action":"openFile",
                    "content":"None"
                }
                break;
            case "call" : 
                const method = params.method;
                const arg = params.arg
                tmp = resolver.call(uri,method,arg,null);
                ret = {
                    "status":"success",
                    "action":"call",
                    "content":JSON.stringify(tmp)
                }
                break;
            default : 
                ret = {
                    "status":"error",
                    "content":"UnSupport Type"
                }
        }
    })

    return ret
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

const parseIntent = (intent) => {
    const my_bundle = JSON.parse(intent);

    const targetPackage = my_bundle.package_name;
    const targetActivity = my_bundle.component_name;
    const action = my_bundle.action;
    const data = my_bundle.data;
    
    const androidIntent = Java.use("android.content.Intent");
    const ComponentName = Java.use("android.content.ComponentName");
    const Uri = Java.use("android.net.Uri")
    //const Context = Java.use("android.content.Context");

    var newIntent = androidIntent.$new();
    if (targetActivity != undefined && targetPackage != undefined) {
        var componentname = ComponentName.$new(targetPackage,targetActivity);
        newIntent.setComponent(componentname);            
    }
    
    if (action != undefined) {
        newIntent.setAction(action)
    }

    if (data != undefined) {
        newIntent.setData(Uri.parse(data));
    }

    if (my_bundle.flags != undefined) {
        var my_flags = 0;
        for (const flag in my_bundle.flags) {
            my_flags |= flags[flag];
        }
        newIntent.setFlags(my_flags);
    }
    
    if (my_bundle.extra != undefined) {
        for (const extra of my_bundle.extra) {
            newIntent.putExtra(extra.key,extra.value);
        }
    }

    return newIntent;
}

const flags = {       
    'ACTIVITY_BROUGHT_TO_FRONT': 0x00400000,
    'ACTIVITY_CLEAR_TASK': 0x00008000,
    'ACTIVITY_CLEAR_TOP': 0x04000000,
    'ACTIVITY_CLEAR_WHEN_TASK_RESET': 0x00080000,
    'ACTIVITY_EXCLUDE_FROM_RECENTS': 0x00800000,
    'ACTIVITY_FORWARD_RESULT': 0x02000000,
    'ACTIVITY_LAUNCHED_FROM_HISTORY': 0x00100000,
    'ACTIVITY_MULTIPLE_TASK': 0x08000000,
    'ACTIVITY_NEW_TASK': 0x10000000,
    'ACTIVITY_NO_ANIMATION': 0x00010000,
    'ACTIVITY_NO_HISTORY': 0x40000000,
    'ACTIVITY_NO_USER_ACTION': 0x00040000,
    'ACTIVITY_PREVIOUS_IS_TOP': 0x01000000,
    'ACTIVITY_REORDER_TO_FRONT': 0x00020000,
    'ACTIVITY_RESET_TASK_IF_NEEDED': 0x00200000,
    'ACTIVITY_SINGLE_TOP': 0x20000000,
    'ACTIVITY_TASK_ON_HOME': 0x00004000,
    'FLAG_DEBUG_LOG_RESOLUTION': 0x00000008,
    'FROM_BACKGROUND': 0x00000004,
    'GRANT_READ_URI_PERMISSION': 0x00000001,
    'GRANT_WRITE_URI_PERMISSION': 0x00000002,
    'RECEIVER_REGISTERED_ONLY': 0x40000000 
}