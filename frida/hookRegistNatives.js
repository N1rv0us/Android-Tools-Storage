/*
 * description : hook JNIEnv -> RegistNatives to get JNI Bridge reflect
 *  source: https://github.com/deathmemory/fridaRegstNtv/blob/master/src/index.ts
 * 
 * author : N1rv0us
 * email : zhangjin9@xiaomi.com
 */

const getModuleInfoByPtr = (fnPtr) => {
    var modules = Process.enumerateModules();
    var modname = null , base = null;

    modules.forEach((mod) => {
        if (mod.base <= fnPtr && fnPtr.toInt32() <= mod.base.toInt32() + mod.size) {
            modname = mod.name;
            base = mod.base;
            return false;
        }
    });
    return [modname,base];
}

const hookRegistNative = () => {
    var env = Java.vm.getEnv();
    var handlePointer = env.handle.readPointer();
    console.log("handle :  " + handlePointer);
    var nativePointer = handlePointer.add(215 * Process.pointerSize).readPointer();
    console.log("register : " + nativePointer);

    Interceptor.attach(nativePointer,{
        onEnter : (args) => {
            var env = Java.vm.getEnv();
            var p_size = Process.pointerSize;
            var methods = args[2];
            var method_count = args[3].toInt32();
            var name = env.getClassName(args[1]);

            // writeObj(methods)

            console.log("======== class : " + name + "======");
            console.log("==== methods: " + methods + " nMethods: " + method_count + " ====");

            for (var i = 0; i < method_count; i++) {
                var idx = i * p_size * 3;
                var fnPtr = methods.add(idx + p_size*2).readPointer();
                const InfoArr = getModuleInfoByPtr(fnPtr);
                const modname = InfoArr[0];
                const base = InfoArr[1];

                var my_log = "name : "+ methods.add(idx).readPointer().readCString()
                    + ", signature : "+ methods.add(idx + p_size).readPointer().readCString()
                    + ", fnPtr : "+ fnPtr
                    + ", module name : "+ modname
                    + " -> base : "+ base;

                if (null != modname) {
                    my_log += ", offset : "+fnPtr.sub(base);
                }

                console.log(my_log);
                
            }
        }
    });
}

if (Java.available) {
    Java.perform(() => {
        hookRegistNative();
    })
}

// function writeObj(obj){ 
//     var description = ""; 
//     for(var i in obj){ 
//      var property=obj[i]; 
//      description+=i+" = "+property+"\n"; 
//     } 
//     console.warn(description); 
// }