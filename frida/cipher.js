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
        console.log("result : "+bytes2hexstr(hash_result));
        console.log("toString : "+this.toString());
        console.log("backtrace : "+printStack());

        return ret
    }

    MessageDigest.update.overload('java.nio.ByteBuffer').implementation = function(buffer) {
        var ret = this.update(buffer);
        var md = Java.cast(this.clone(),MessageDigest);
        var hash_result = md.digest();
        
        console.log("algorithm : "+this.getAlgorithm());
        console.log("input : "+bbuffer2str(bytes));
        console.log("result : "+bytes2hexstr(hash_result));
        console.log("toString : "+this.toString());
        console.log("backtrace : "+printStack());

        return ret
    } 

    MessageDigest.update.overload('[B','int','int').implementation = function(bytes,offset,length) {
        var ret = this.update(bytes,offset,length);
        var md = Java.cast(this.clone(),MessageDigest);
        var hash_result = md.digest();
        
        console.log("algorithm : "+this.getAlgorithm());
        console.log("input : "+bytes2str(bytes));
        console.log("result : "+bytes2hexstr(hash_result));
        console.log("toString : "+this.toString());
        console.log("backtrace : "+printStack());

        return ret
    }

}
/**
 * hook javax.crypto.Cipher
 */
function hookCipher() {
    var CipherType = Java.use("javax.crypto.Cipher");
    var SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");

    // secret key 
    SecretKeySpec.$init.overload("[B","java.lang.String").implementation = function(key,algorithm) {
        var ret = this.$init(key,algorithm);
        console.log("Got Cipher Algorithm : "+algorithm);
        console.log("Got Cipher Key : "+bytes2hexstr(key));
        console.log("backtrace : "+printStack());
        return ret;
    }

    //doFinal
    CipherType.doFinal.overload('[B','int').implementation = function(bytes,offset) {
        var ret = this.doFinal(bytes,offset);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(bytes));
            console.log("ciphertext : "+bytes2base64(ret));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(bytes));
            console.log("ciphertext : "+bytes2str(ret));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }

    CipherType.doFinal.overload('[B').implementation = function(bytes) {
        var ret = this.doFinal(bytes);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(bytes));
            console.log("ciphertext : "+bytes2base64(ret));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(bytes));
            console.log("ciphertext : "+bytes2str(ret));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }

    CipherType.doFinal.overload('[B','int','int').implementation = function(bytes,offset,length) {
        var ret = this.doFinal(bytes,offset,length);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(bytes));
            console.log("ciphertext : "+bytes2base64(ret));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(bytes));
            console.log("ciphertext : "+bytes2str(ret));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }

    CipherType.doFinal.overload('[B','int','int','[B').implementation = function(bytes,offset,length,output) {
        var ret = this.doFinal(bytes,offset,length,output);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(bytes));
            console.log("ciphertext : "+bytes2base64(output));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(bytes));
            console.log("ciphertext : "+bytes2str(output));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }

    CipherType.doFinal.overload('[B','int','int','[B','int').implementation = function(bytes,offset,length,output,outlen) {
        var ret = this.doFinal(bytes,offset,length,output,outlen);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(bytes));
            console.log("ciphertext : "+bytes2base64(output));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(bytes));
            console.log("ciphertext : "+bytes2str(output));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }

    CipherType.doFinal.overload('java.nio.ByteBuffer','java.nio.ByteBuffer').implementation = function(input,output) {
        var ret = this.doFinal(input,output);
        if (this.opmode.value == 1) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : encrypt");
            console.log("plaintext : "+ bytes2str(input));
            console.log("ciphertext : "+bytes2base64(output));
        }else if (this.opmode.value == 2) {
            console.log("Got Cipher Algorithm :"+this.getAlgorithm());
            console.log("type : decrypt");
            console.log("plaintext : "+ bytes2base64(input));
            console.log("ciphertext : "+bytes2str(output));
        } else {
            console.log("Ooops!");
        }

        console.log("backtrace : "+printStack());

        return ret;

    }
} 

/**
 * 将java的bytes对象转化为hex字符串
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
/**
 * 将bytes数组转化为字符串
 * @param {*} bytes 
 * @returns 
 */
function bytes2str(bytes) {
    return Java.use("java.lang.String").$new(bytes)
}
/**
 * 将bytebuffer 对象（java.nio.ByteBuffer）转化为字符串
 * @param {*} buffer 
 * @returns 
 */
function bbuffer2str(buffer) {
    var charset = Java.use("java.nio.charset.Charset").forName("utf-8");
    return charset.decode(buffer).toString();
}
/**
 * 将byte数组转化为Base64字符串
 * @param {*} bytes 
 * @returns 
 */
function bytes2base64(bytes) {
    var Base64 = Java.use("android.util.Base64");
    return Base64.encodeToString(bytes,0);
}

function printStack() {
    var Throwable = Java.use("java.lang.Throwable");
    return __printStack(Throwable.$new().getStackTrace());
}

function __printStack(stackElements) {
    // var body = "Stack: " + stackElements[0];    
    // for (var i = 0; i < stackElements.length; i++) {
    //     body += "\n    at " + stackElements[i];
    // }
    // return body
}

if (Java.available) {
    Java.perform(function() {
        hookCipher();
        hookMessageDigest();
    });
}
