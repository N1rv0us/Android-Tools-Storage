/*
 * Try to implement the tracer function myself 
 * Observe the order in which specific classes are called
 * 
 * author : N1rv0us
 * mail : zhangjin9@xiaomi.com
 */

var MatchRegEx = "com.miui.gallery"

function getTid() {
    var Thread = Java.use("java.lang.Thread")
    return Thread.currentThread().getId();
}

function getTName() {
    var Thread = Java.use("java.lang.Thread")
    return Thread.currentThread().getName();
}

function getCurrentTime() {
    var myDate = new Date()
    return myDate.toLocaleString();
}

function traceClass(clsname) {
    try {
        var target = Java.use(clsname);
        var methods = target.class.getDeclaredMethods();
        methods.forEach(function (method) {
            var methodName = method.getName();
            ///console.log("We Got a Method : "+clsname+'.'+methodName);
            var overloads = target[methodName].overloads;
            overloads.forEach(function (overload) {
                var proto = '(';
                overload.argumentTypes.forEach(function(type) {
                    proto += type.className+", ";
                });
                if (proto.length > 1) {
                    proto = proto.substr(0,proto.length-2);
                }
                proto += ')'

                //console.log("hooking: "+clsname+"."+methodName+proto);
                overload.implementation = function() {
                    var args = [];
                    var tid = getTid();
                    var tname = getTName();
                    var curtime = getCurrentTime();
                    for (var j = 0;j < arguments.length;j++) {
                        args[j] = arguments[j]+"";
                    }
                    console.log('['+curtime+'] ['+tid+','+tname+'] '+clsname+"."+methodName+proto+' with '+args);

                    var ret = this[methodName].apply(this,arguments);
                    return ret;
                }
            }); 
        });
    } catch(e) {
        console.log(clsname+" hook failed : "+e);
    }
}

function hook_target() {
    if (Java.available) {
        Java.perform(function() {
            console.log("Now Tracing Start ...")
            Java.enumerateLoadedClasses({
                onMatch:function(aClass) {
                    if (aClass.match(MatchRegEx)) {
                       //console.log('We catched class named : '+aClass)
                       traceClass(aClass)
                    } 
                    //traceClass(aClass)
                },
    
                onComplete:function() {
                    console.log("Hook Complete")
                }
            })
        })
    }
}

setTimeout(hook_target,300)
