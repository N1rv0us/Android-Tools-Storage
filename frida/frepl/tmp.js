Java.perform(function() {
    var mContext = null;
        Java.choose("com.android.server.am.ActivityManagerService",{
            "onMatch": (instance) => {
                mContext = instance.mContext.value;
                console.log("[*] instance found " + instance.mContext.value);
            },
            "onComplete" : () => {
                console.log("[*] finished Heap Search");
            }
        });
    
        var mPs = mContext.getPackageManager();

        var flags = 15
        var tPkgInfo = mPs.getPackageInfo("com.qiyi.video",flags);
        console.warn(tPkgInfo)
})