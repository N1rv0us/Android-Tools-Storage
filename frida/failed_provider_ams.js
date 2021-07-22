if (Java.available) {
    Java.perform(() => {
        var ActivityManagerService = Java.use("com.android.server.am.ActivityManagerService");
        var Binder = Java.use("android.os.Binder");
        // console.error(JSON.stringify(IActivityManager))

        ActivityManagerService.getContentProvider
        .overload("android.app.IApplicationThread","java.lang.String","java.lang.String","int","boolean")
        .implementation = function(caller,callingPackage,name,userId,stable) {
            var ret = this.getContentProvider(caller,callingPackage,name,userId,stable);
            var uid = Binder.getCallingUid();

            if (ret == null) {
                console.error("#############  Failed to Get Content Provider  ##############");
                console.log("callingPackage : ",callingPackage);
                console.log("callingUid : ",uid);
                console.log("name : ",name);
                // console.log("userId : ",userId);
                console.log("stable : "+JSON.stringify(stable));
            } else {
                var providerInfo = ret.info.value;

                console.warn("############# Get ContentProvider Holder Success ##############");
                console.log("calling Package : ",callingPackage);
                console.log('callingUid :',uid);
                console.log("Content Provider Info :",providerInfo.toString());
            }

            return ret;
        }
    })
} else {
    console.error("pls check your spell");
    console.error("otherwise, is this an iOS APP ?");
}