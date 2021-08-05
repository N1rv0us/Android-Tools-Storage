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

const back2py = (tag,obj) => {
    console.warn("catch ",tag," sending back");
    console.log(JSON.stringify(obj,null,'\t'));
}


var ctx = null;
var pm = null;
var pinfo = null;

rpc.exports = {
    init : () => envInit(),
    permlist : () => getPermissionList(),
    permcheck : (permission) => checkPermission(permission),
    permctrl : () => hookPermissionRequest()
}

const envInit = () => {
    return wrapJavaperform(() => {
        ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        pm = ctx.getPackageManager();
        var flag = 0x00001000;
        pinfo = pm.getPackageInfo(ctx.getPackageName(),flag);
    })
}

const getPermissionList = () => {
    if (ctx == null || pm == null) {
        envInit();
    }

    return wrapJavaperform(() => {
        try {
            var ret = pinfo['requestedPermissions'].value;
            if (typeof(ret) == 'object') {
                var relist = new Array();
                for (let i = 0; i < ret.length; i++) {
                    relist[i] = ret[i].toString();
                }
                return relist;
            }
            return ret;
        } catch(error) {
            return null;
        }
    })    
}

const checkPermission = (permission) => {
    if (ctx == null) {
        envInit();
    }

    return wrapJavaperform(() => {
        var ret = ctx.checkSelfPermission(permission);
        if(ret == 0) {
            return true;
        } else {
            return false;
        }
    })
}

const hookPermissionRequest = () => {
    return wrapJavaperform(() => {
        var Activity = Java.use("android.app.Activity");

        Activity.requestPermissions
        .overload('[Ljava.lang.String;','int')
        .implementation = function(permissions,requestcode) {
            var recorder = {}
            recorder['activity'] = JSON.stringify(this);
            recorder['permissions'] = permissions;
            recorder['reqcode'] = requestcode;
            back2py("REQUEST_PERMISSION",recorder);

            return this.requestPermissions(permissions,requestcode);
        }
        
    })
}