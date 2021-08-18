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

var callingUid = null;
var callingPkg = null;
var UserCtrl = null;
var CtrlPkgList = new Array();

rpc.exports = {
    "mode" : (mode) => {UserCtrl = RESULT_FLAG[mode]},
    "setpkglist" : (pkgs) => {CtrlPkgList = pkgs.split(",")},
    "start" : () => AutoAuthor()
}

var RESULT_FLAG = {
    'LINKED_TO_SETTINGS' : -2,
    'CANCELED' : -1,
    'GRANTED_ALWAYS' : 0,
    'GRANTED_FOREGROUND_ONLY' : 1,
    'DENIED' : 2,
    'DENIED_DO_NOT_ASK_AGAIN' : 3,
    'GRANTED_ONE_TIME' : 4
}

const AutoAuthor = () => {
    if(UserCtrl == null)
        return ;
    return wrapJavaperform(() => {
        var flag = true
        var count = 0
        var ps = ''
        var GrantPermissionsActivity = Java.use('com.android.packageinstaller.permission.ui.GrantPermissionsActivity');
        GrantPermissionsActivity.showNextPermissionGroupGrantRequest.overload().implementation = function(){
            console.warn("calling by ",this.mCallingPackage.value);
            var perm_list = this.mRequestedPermissions.value;
            perm_list.forEach((element) => {
                console.log(element);
            })
            if (!CtrlPkgList.includes(this.mCallingPackage.value)) {
                return this.showNextPermissionGroupGrantRequest.apply(this,arguments);
            }
            if(flag){
                flag = false
                var clazz = Java.use("java.lang.Class");
                var param = Java.cast(this.getClass(), clazz).getDeclaredField("mRequestGrantPermissionGroups");
                param.setAccessible(true);
                ps = param.get(this).toString()
                ps = ps.replace('{', '').replace('}', '').split(', ')
                count = ps.length-1
            }
            
            if (count>=0){
                var p = ps[count--].split('=')[0]
                p = p.split("{")[1].split(" ")[0]
                console.log(p)
                this.onPermissionGrantResult(p, UserCtrl, true, false)
                
                return true
            }else{
                flag = true
                ps = ''
                
                return false
            }
        }
    })
}

// UserCtrl = RESULT_FLAG["GRANTED_FOREGROUND_ONLY"];
// CtrlPkgList.push("com.baidu.searchbox");
// AutoAuthor();