Java.perform(() => {
    var api_level = Java.use("android.os.Build$VERSION").SDK_INT.value;
    console.log("### APP running in Android "+api_level);
    if(api_level < 30) {
        console.error("this script couldn't run under Android R !!")
        exit();
    }
    var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
    const AppOpsCls = Java.use("android.app.AppOpsManager");
    const AppOps = Java.cast(ctx.getSystemService("appops"),AppOpsCls)
    const AppOpsCallback = Java.use("android.app.AppOpsManager$OnOpNotedCallback");

    const mycallback = Java.registerClass({
        name: 'com.n1rv0us.appops.callback',
        superClass: AppOpsCallback,
        methods: {
            onNoted : [{
                returnType: 'void',
                argumentTypes : ['android.app.SyncNotedAppOp'],
                implementation(op) {
                    var opcode = op.getOp();
                    var tag = op.getAttributionTag();
                    console.warn("[onNoted] : opcode ==>",opcode," tag ==>",tag);
                    console.error(stacktrace());
                }
            }],
            onSelfNoted : [{
                returnType: 'void',
                argumentTypes: ['android.app.SyncNotedAppOp'],
                implementation(op) {
                    var opcode = op.getOp();
                    var tag = op.getAttributionTag();
                    console.warn("[onSelfNoted] : opcode ==>",opcode," tag ==>",tag);
                    console.error(stacktrace());
                }
            }],
            onAsyncNoted : [{
                returnType:'void',
                argumentTypes: ['android.app.AsyncNotedAppOp'],
                implementation(op) {
                    var opcode = op.getOp();
                    var tag = op.getAttributionTag();
                    var msg = op.getMessage();
                    console.warn("[onSelfNoted] : opcode ==>",opcode," tag ==>",tag);
                    console.error("[msg] ==> ",msg);
                }
            }]
        }
    });
    var instance = mycallback.$new();
    // console.log(JSON.stringify(AppOps.sOnOpNotedCallback.value))
    // try {
    //     AppOps.setOnOpNotedCallback(ctx.getMainExecutor(),instance);
    // } catch(error) {
    //     AppOps.setOnOpNotedCallback(ctx.getMainExecutor(),null);
    //     AppOps.setOnOpNotedCallback(ctx.getMainExecutor(),instance);
    // }
    
    var default_callback = AppOps.sOnOpNotedCallback.value
    // console.log(default_callback.$className)
    if (default_callback == null){
        AppOps.setOnOpNotedCallback(ctx.getMainExecutor(),instance);
    } else{
        default_callback = Java.use(default_callback.$className)
        default_callback.onNoted.implementation = function(op) {
            var opcode = op.getOp();
            var tag = op.getAttributionTag();
            console.warn("[onNoted] : opcode ==>",opcode," tag ==>",tag);
            console.error(stacktrace());
        }

        default_callback.onSelfNoted.implementation = function(op) {
            var opcode = op.getOp();
            var tag = op.getAttributionTag();
            console.warn("[onSelfNoted] : opcode ==>",opcode," tag ==>",tag);
            console.error(stacktrace());
        }

        default_callback.onAsyncNoted.implementation = function(op) {
            var opcode = op.getOp();
            var tag = op.getAttributionTag();
            var msg = op.getMessage();
            console.warn("[onSelfNoted] : opcode ==>",opcode," tag ==>",tag);
            console.error("[msg] ==> ",msg);
        }
    }
})

function stacktrace() {
    var thread = Java.use('java.lang.Thread');
    var instance = thread.$new();
    var stack = instance.currentThread().getStackTrace();
    var at = "";

    for (var i = 0;i < stack.length ; i++) {
        at += stack[i].toString()+"\n";
    }

    return at;
}
