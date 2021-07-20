if(Java.available) {
    Java.perform(function(){
        
       Java.enumerateClassLoaders({
           "onMatch": function(loader) {
                //Load Dex File:/data/user/0/com.xiaomi.shop/app_plugin_signed/44dcee4a9c232c1684e55bce3fe3c436_32c6020a35585f0e1858a1eecbcc68a9.zip
                //console.log(loader)
                // if (loader.toString().indexOf("44dcee4a9c232c1684e55bce3fe3c436_32c6020a35585f0e1858a1eecbcc68a9.zip")) {
                //     Java.classFactory.loader = loader;
                //     //console.warn("change classloader success");
                // }
                console.log(loader.toString());
           },
           "onComplete": function() {
               console.log("success");
           }
       })

    //    var VipUserInfo = Java.use('com.xiaomi.vip.service.XiaomiVipSdkService');
    //    var InfoMethod = VipUserInfo.class.getDeclaredMethods();
    //    InfoMethod.forEach(function(s) {
    //        console.log(s)
    //    })
    //    var clsAsResource = VipUserInfo.class.getName().replace('.', '/').concat(".class");
    //    console.log(clsAsResource)
    //    var clsloader = VipUserInfo.class.getClassLoader();
    //    console.warn(clsloader.toString())
    //    console.warn(clsloader.getResource("miui/vip/VipUserInfo.class"))
    
    //    var RootFragment = Java.classFactory.use("com.abc.xxx");
    //    RootFragment.run.implementation = function(arg) {
    //         var ret = this.run(arg)
    //         var stack = stacktrace()
    //         console.warn(stack)
    //         return ret;
    //     }

    })

//     Java.perform(() => {
//         var process_Obj_Module_Arr = Process.enumerateModules();
//         for(var i = 0; i < process_Obj_Module_Arr.length; i++) {
//             var name = process_Obj_Module_Arr[i].name;
//             if (name.indexOf('.so') == -1){
//                 console.log("",name)
//             }
//         }

//         const hooks = Module.load("boot-miuisystemsdk@boot.oat");
//         console.log("文件系统路径",hooks.path);
//         var Symbol = hooks.enumerateSymbols();
//         for(var i = 0; i < Symbol.length; i++) {
//             console.log("isGlobal:",Symbol[i].isGlobal);
//             console.log("type:",Symbol[i].type);
//             console.log("section:",JSON.stringify(Symbol[i].section));
//             console.log("name:",Symbol[i].name);
//             console.log("address:",Symbol[i].address);
//         }
//       });
}