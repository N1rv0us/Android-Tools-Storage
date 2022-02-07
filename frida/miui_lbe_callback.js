var ops = [4, 20, 13, 74, 5, 7, 10013, 0, 1, 2, 10, 12, 41, 42, 79, 51, 65, 29, 36, 10028, 10029, 10030, 10031, 26, 10032, 59, 60, 56, 10008, 27, 8, 9, 10022, 14, 16, 17, 21, 6, 30]
Java.perform(() => {
    // var AppOpsServiceState = Java.use("com.android.server.AppOpsServiceState");
    // AppOpsServiceState.onAppApplyOperation
    // .overload("int", "java.lang.String", "int", "int", "int", "int", "int", "boolean")
    // .implementation = function() {
    //     op = arguments[2];
    //     console.warn("notice op is ",op,"   from package ["+arguments[1]+"]");
    //     console.log(stacktrace());
    // }
    var Binder = Java.use("android.os.Binder");
    var MiuiBinderProxy = Java.use("android.os.MiuiBinderProxy");
    MiuiBinderProxy.callTransact
    .overload('int', 'int', 'java.lang.Class', '[Ljava.lang.Object;')
    .implementation = function() {
        var ret = this.callTransact.apply(this,arguments);
        var description = this.mDescriptor.value;
        
        if (arguments[0] == 4) {
            var objs = arguments[3];
            var pkg = objs[1];
            var op = objs[2];
            // console.error(op.toString())
            if (ops.indexOf(parseInt(op.toString())) != -1) {
                if(op == 10 || op == 1) return ret;
                if (op == 10032) console.error("call from ",Binder.getCallingUid());
                console.error("hit record policy");
                console.warn("proxy post to binder : ",description + "with id :"+arguments[0]);
                console.warn("record package [",pkg,'] with operation : ',op);
                console.log(stacktrace());
            }
        }

        return ret;
    }
})

function stacktrace() {
    var thread = Java.use('java.lang.Thread');
    var instance = thread.$new();
    var stack = instance.currentThread().getStackTrace();
    var at = "";

    for (var i = 2;i < stack.length ; i++) {
        at += stack[i].toString()+"\n";
    }

    return at;
}

// com.android.server.AppOpsServiceState.onAppApplyOperation(int, java.lang.String, int, int, int, int, int, boolean) : void
// Descriptor: Lcom/android/server/AppOpsServiceState;->onAppApplyOperation(ILjava/lang/String;IIIIIZ)V

// android.os.MiuiBinderProxy.callTransact(int, int, java.lang.Class, java.lang.Object[]) : java.lang.Object
// Descriptor: Landroid/os/MiuiBinderProxy;->callTransact(IILjava/lang/Class;[Ljava/lang/Object;)Ljava/lang/Object;
