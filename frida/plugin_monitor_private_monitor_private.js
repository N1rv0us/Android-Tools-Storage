
/** 
 * Hook android.net.wifi.WifiManager related interface
 */
function hookWifiPart() {
    var WifiInfo = Java.use("android.net.wifi.WifiInfo");
    
    WifiInfo.getMacAddress.implementation = function() {
        var ret = this.getMacAddress();
        console.warn("catch getMacAddress : "+ret);
        console.warn(printStack());
        return ret;
    }

    WifiInfo.getSSID.implementation = function() {
        var ret = this.getSSID();
        console.warn("catch getSSID : "+ ret);
        console.warn(printStack());
        return ret;
    }

    WifiInfo.getIpAddress.implementation = function() {
        var ret = this.getIpAddress();
        var ip = (ret & 0xff)+'.'+(ret>>8 & 0xff)+'.'+(ret>>16 & 0xff)+'.'+(ret>>24 & 0xff);
        console.log("catch getIpAddress : "+ ret);
        console.warn(printStack());
        return ret;
    }
}

/** 
 * Hook data query by android.provider.Settings$Secure 
 */
function hookSecureSettingsPart() {
    var private_dict = new Array("bluetooth_address","android_id");
    var secure = Java.use("android.provider.Settings$Secure");
    
    secure.getString.implementation = function(resolver,str) {
        var ret = this.getString(resolver,str);
        if (private_dict.indexOf(str) > -1) {
            console.log("catch SecureSettings "+str+" with result "+ret);
            console.warn(printStack());
        }
        return ret;
    }
}

/** 
 * Hook data obtain from idProvider(com.android.id.impl.IdProviderImpl)
 * ## ATTATION : the target is content://com.miui.idprovider ## 
 */
function hookidProviderPart() {
    var idProvider = Java.use("com.android.id.impl.IdProviderImpl");
    
    idProvider.getUDID.implementation = function(context) {
        var ret = this.getUDID(context);
        console.log("catch idProvider uuid with "+ret);
        console.warn(printStack());
        return ret;
    }

    idProvider.getOAID.implementation = function(context) {
        var ret = this.getOAID(context);
        console.log("catch idProvider OAID with "+ret);
        console.warn(printStack());
        return ret;
    }

    idProvider.getVAID.implementation = function(context) {
        var ret = this.getVAID(context);
        console.log("catch idProvider VAID with "+ret);
        console.warn(printStack());
        return ret;
    }

    idProvider.getAAID.implementation = function(context) {
        var ret = this.getAAID(context);
        console.log("catch idProvider AAID with "+ ret);
        console.warn(printStack());
        return ret;
    }
}

/** 
 * Hook Device info from android.telephony.TelephonyManager
 *
 */
function hookTelephoneManagerPart() {
    var TelephonyManager = Java.use("android.telephony.TelephonyManager");

    //imei
    TelephonyManager.getImei.overload('int').implementation = function(slotIndex) {
        var ret = this.getImei(slotIndex);
        console.log("catch imei : "+ret);
        console.warn(printStack());
        return ret;
    }
    TelephonyManager.getDeviceId.overload('int').implementation = function(slotIndex) {
        var ret = this.getDeviceId(slotIndex);
        console.log("catch deviceId : "+ret);
        console.warn(printStack());
        return ret
    }
    //meid
    TelephonyManager.getMeid.overload('int').implementation = function(slotIndex) {
        var ret = this.getMeid(slotIndex);
        console.log("catch meid : "+ret);
        console.warn(printStack());
        return ret;
    }
    //imsi
    TelephonyManager.getSubscriberId.overload('int').implementation = function(slotIndex) {
        var ret = this.getSubscriberId(slotIndex);
        console.log("catch imsi : "+ret );
        console.warn(printStack());
        return ret;
    }
    //phoneNum
    TelephonyManager.getLine1Number.overload('int').implementation = function(subId) {
        var ret = this.getLine1Number(subId);
        console.log("catch phoneNum : "+ret);
        console.warn(printStack());
        return ret;
    }
}

function printStack() {
    var Throwable = Java.use("java.lang.Throwable");
    var stackElements = Throwable.$new().getStackTrace();
    var body = "Stack: " + stackElements[0];    
    for (var i = 0; i < stackElements.length; i++) {
        body += "\n    at " + stackElements[i];
    }
    return body
}

/*** script running ***/
if (Java.available) {
    Java.perform(function() {
        hookWifiPart();
        hookSecureSettingsPart();
        hookidProviderPart();
        hookTelephoneManagerPart();
    });
}