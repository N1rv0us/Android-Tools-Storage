/**
 * hook MessageDigest
 * @return
 */
 function hookMessageDigest() {
    var MessageDigest = Java.use("java.security.MessageDigest");
    MessageDigest.update.overload('[B').implementation = function(bytes) {
        var ret = this.update(bytes);
        var md = Java.cast(this.clone(),MessageDigest);
        var hash_result = md.digest();
        
        console.log("algorithm : "+this.getAlgorithm());
        console.log("input : "+bytes2str(bytes));
        console.log("result : "+bytes2hexstr(hash_result))
        console.log("toString : "+this.toString())

        return ret
    }

    MessageDigest.update.overload('java.nio.ByteBuffer').implementation = function(buffer) {
        var ret = this.update(buffer);
        var md = Java.cast(this.clone(),MessageDigest);
        var hash_result = md.digest();
        
        console.log("algorithm : "+this.getAlgorithm());
        console.log("input : "+bbuffer2str(bytes));
        console.log("result : "+bytes2hexstr(hash_result))
        console.log("toString : "+this.toString())

        return ret
    } 

    MessageDigest.update.overload('[B','int','int').implementation = function(bytes,offset,length) {
        var ret = this.update(bytes,offset,length);
        var md = Java.cast(this.clone(),MessageDigest);
        var hash_result = md.digest();
        
        console.log("algorithm : "+this.getAlgorithm());
        console.log("input : "+bytes2str(bytes));
        console.log("result : "+bytes2hexstr(hash_result))
        console.log("toString : "+this.toString())

        return ret
    }

}


/**
 * 将java的bytes对象转化为字符串
 * @param {bytes[]} bytes 
 * @return {String}
 */
function bytes2hexstr(bytes) {
    var sb = Java.use("java.lang.StringBuilder").$new();
    var Integer = Java.use("java.lang.Integer");

    for (var i = 0; i < bytes.length; i++) {
        sb.append(Integer.toHexString(bytes[i] & 0xff));
    }

    return sb.toString()
}

function bytes2str(bytes) {
    return Java.use("java.lang.String").$new(bytes)
}

function bbuffer2str(buffer) {
    var charset = Java.use("java.nio.charset.Charset").forName("utf-8");
    return charset.decode(buffer).toString();
}

if (Java.available) {
    Java.perform(function() {
        hookMessageDigest()
    });
}
