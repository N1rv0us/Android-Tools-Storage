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

Java.perform(() => {
    var a = Java.use("com.android.server.am.ActivityManagerService");
    var am = a.startService.overload('android.app.IApplicationThread', 'android.content.Intent', 'java.lang.String', 'boolean', 'java.lang.String', 'java.lang.String', 'int');
    console.log(JSON.stringify(a));
    console.log(am.implementation);

    am.implementation = function() {
        console.log("helllll");
        return this.startService.apply(this,arguments);
    }

    console.log(JSON.stringify(am.implementation))
    am.implementation = null;
})