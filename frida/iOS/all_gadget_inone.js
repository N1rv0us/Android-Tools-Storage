// some useful gadget(method) from <iOS应用逆向与安全之道>

// 枚举一个类中所有的方法，可用于批量拦截；感觉Android也是适用的喔
var resolver = new ApiResolver('objc'); // more info : https://frida.re/docs/javascript-api/#apiresolver
resolver.enumerateMatch('*[WCRedEnvelopesLogicMgr *]',{
    onMatch : function(match) {
        console.log(match['name'] + ':' + match['address'])
    },
    onComplete : function() {

    }
})

// 查找和hook无符号表的function

function get_rva(module,offset) {
    var base_addr = Module.findBaseAddress(module);
    if (base_addr === null)
        base_addr = enum_to_find_module(module);

    console.log(module + 'base_addr = '+ base_addr);
    var target_addr = base_addr.add(offset);

    return target_addr;
}

var target_addr = get_rva("your_module_name_here","offset_in_so");
console.log("target_addr = " + target_addr);

Interceptor.attach(ptr(target_addr),{
    onEnter : function(args) {
        // your doing here yourself;
    },
    onLeave : function(retval) {
        // doing here too;
    }
})