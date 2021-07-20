if (Java.available) {
    Java.perform(() => {
        //var ActivityThread = Java.use("android.app.ActivityThread");

        Java.use("android.app.ActivityThread")
        .acquireProvider
        .overload('android.content.Context', 'java.lang.String', 'int', 'boolean')
        .implementation = function(ctx,auth,userId,stable) {
            var ret = this.acquireProvider(ctx,auth,userId,stable);

            if (ret != null) {
                return ret
            }

            console.warn("########################################");
            console.error("ret is ",JSON.stringify(ret));
            console.log("what is ",ctx.getOpPackageName())
            console.log("acquire ing target Provider with auth",auth);
            console.error(printStack())
            return ret;
        }
    })
} else {
    console.error("pls check your spell");
    console.error("otherwise, is this an iOS APP ?");
}

function printStack() {
    var Throwable = Java.use("java.lang.Throwable");
    return __printStack(Throwable.$new().getStackTrace());
}

function __printStack(stackElements) {
    var body = "Stack: " + stackElements[0];    
    for (var i = 0; i < stackElements.length; i++) {
        body += "\n    at " + stackElements[i];
    }
    return body
}