/*
 * description : Through hook libc call(open, close, read, write, unlink, remove) to monitor file operations
 * 
 * author : N1rv0us
 * email : zhangjin9@xiaomi.com
 */

function prtLog(method,file) {
    send("API Monitor | "+
        "FileSystem | "+
        method + " - " + 
        file
        );
}

if (Java.available) {
    Java.perform(function() {
        Interceptor.attach(
            Module.findExportByName("libc.so","open"), {
                onEnter : function(args) {
                    var file = Memory.readCString(args[0]);
                    if (!file.includes("/dev/ashmem") && !file.includes("/proc"))
                        prtLog("open",file);
                },
                onLeave : function(retval){}
            }
        );

        Interceptor.attach(
            Module.findExportByName("libc.so","close"), {
                onEnter : function(args) {
                    try {
                        var file = Memory.readCString(args[0]);
                        prtLog("close",file);
                    } catch(error) {

                    }
                    
                },
                onLeave : function(retval) {}
            }
        );

        Interceptor.attach(
            Module.findExportByName("libc.so","read"), {
                onEnter : function(args) {
                    try{
                        var file = Memory.readCString(args[0]);
                        prtLog("read",file);
                    }catch(error) {

                    }
                    
                },
                onLeave : function(retval) {}
            }
        );

        Interceptor.attach(
            Module.findExportByName("libc.so","write"), {
                onEnter : function(args) {
                    try{
                        var file = Memory.readCString(args[0]);
                        prtLog("write",file);
                    } catch(error) {
                        
                    }
                    
                },
                onLeave : function(retval) {}
            }
        );

        Interceptor.attach(
            Module.findExportByName("libc.so","unlink"), {
                onEnter : function(args) {
                    var file = Memory.readCString(args[0]);
                    prtLog("unlink",file);
                },
                onLeave : function(retval) {}
            }
        );

        Interceptor.attach(
            Module.findExportByName("libc.so","remove"), {
                onEnter : function(args) {
                    var file = Memory.readCString(args[0]);
                    prtLog("remove",file);
                },
                onLeave : function(retval) {}
            }
        )
    })
}
