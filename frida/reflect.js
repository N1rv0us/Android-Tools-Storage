/*
 * description : checking application calling method via reflection
 *
 * author : N1rv0us
 * email : zhangjin9@xiaomi.com
 */

if (Java.available) {
    Java.perform(() => {
        const reflect_method = Java.use("java.lang.reflect.Method");
        reflect_method.invoke.implementation = function() {
            var ret = this.invoke(...arguments);
            //console.log("Catching Call Inflect Method Success~");
            console.log("======== catchting Method reflect invoke =======")
            var tmp_cls = this.getDeclaringClass().getName().toString();
            var tmp_method = this.getName();

            console.log("class Name : "+ tmp_cls);
            console.log("method Name : "+ tmp_method);

            var instance = arguments[0];
            if (instance == null){
                console.log("reflect is an static method");
            } else {
                console.log("method instance : "+instance);
            } 
            var args = new Array();
            for (var i = 1;i < arguments.length;i++) {
                console.log("argument : "+arguments[i])
                args[i-1] = arguments[i]
            }
            
            return ret;
        }
    });
} else {
    console.error("pls run in an Java environment");
}