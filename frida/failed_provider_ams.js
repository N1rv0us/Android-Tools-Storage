if (Java.available) {
    Java.perform(() => {
        var ActivityManagerService = Java.use("com.android.server.am.ActivityManagerService");
        // console.error(JSON.stringify(IActivityManager))

        ActivityManagerService.getContentProvider
        .overload("android.app.IApplicationThread","java.lang.String","java.lang.String","int","boolean")
        .implementation = function(caller,callingPackage,name,userId,stable) {
            var ret = this.getContentProvider(caller,callingPackage,name,userId,stable);

            if (ret == null) {
                console.warn("#############  Failed to Get Content Provider  ##############");
                console.log("callingPackage : ",callingPackage);
                console.log("name : ",name);
                // console.log("userId : ",userId);
                console.log("stable : "+JSON.stringify(stable));
            }

            return ret;
        }
    })
} else {
    console.error("pls check your spell");
    console.error("otherwise, is this an iOS APP ?");
}