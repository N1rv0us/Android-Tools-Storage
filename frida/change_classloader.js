if(Java.available) {
    Java.perform(function(){
        var ClassLoaderFactory = Java.use("your.happened.xxx");

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


        ClassLoaderFactory.createPluginClassLoader.implementation = function(str,str2) {
            var ret = this.createPluginClassLoader(str,str2)
            console.log("Load Dex File:"+str)

            return ret
        }
        
       Java.enumerateClassLoaders({
           "onMatch": function(loader) {
                //Load Dex File:/data/user/0/com.xiaomi.shop/app_plugin_signed/44dcee4a9c232c1684e55bce3fe3c436_32c6020a35585f0e1858a1eecbcc68a9.zip
                //console.log(loader)
                if (loader.toString().indexOf("44dcee4a9c232c1684e55bce3fe3c436_32c6020a35585f0e1858a1eecbcc68a9.zip")) {
                    Java.classFactory.loader = loader;
                    //console.warn("change classloader success");
                }
           },
           "onComplete": function() {
               console.log("success");
           }
       })
       var RootFragment = Java.classFactory.use("com.abc.xxx");
       RootFragment.run.implementation = function(arg) {
            var ret = this.run(arg)
            var stack = stacktrace()
            console.warn(stack)
            return ret;
        }

    })
}