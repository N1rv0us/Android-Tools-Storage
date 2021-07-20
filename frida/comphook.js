'use strict';

if (Java.available){
    Activity_hook()
    //Broadcast_hook()
    //Service_hook()
    //LocalBroadcast_hook()
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
function Activity_hook(){
    /*
     * Activity 启动hook 重点hook startActivity/startActivityForResult/getActivity
     */
    Java.perform(function(){
        var clsActivity = Java.use("android.app.Activity")
        var clsIntent = Java.use("android.content.Intent")
        var clsPendingIntent = Java.use("android.app.PendingIntent")

        const Instrumentation = Java.use("android.app.Instrumentation");
        Instrumentation.execStartActivity.overload('android.content.Context', 'android.os.IBinder', 'android.os.IBinder', 'android.app.Activity', 'android.content.Intent', 'int', 'android.os.Bundle').implementation = function() {
            var ret = this.execStartActivity(...arguments)
            console.warn("##############")
            console.log("Got Activity starter : "+arguments[4].toURI())
            console.warn(printStack())
            return ret
        }

        // clsActivity.startActivity.overload('android.content.Intent').implementation = function(intent) {
        //     var ret = this.startActivity(intent)
        //     console.log('Got startActivity : '+intent.toURI())
        //     console.warn(printStack())
        //     return ret
        // }

        // clsActivity.startActivityForResult.overload('android.content.Intent','int').implementation = function(intent,reqcode) {
        //     var ret = this.startActivityForResult(intent,reqcode)
        //     console.log('Got startActivityForResult : '+intent.toURI())
        //     return ret
        // }

        // clsPendingIntent.getActivity.overload('android.content.Context', 'int', 'android.content.Intent', 'int').implementation = function(context,reqcode,intent,flags) {
        //     var ret = this.getActivity(context,reqcode,intent,flags)
        //     console.log('Got PendingIntent getActivity : '+intent.toURI())
        //     return ret
        // }

    })
    
}

function Broadcast_hook() {
    /*
     * Broadcast 启动hook
     */
    Java.perform(function() {
        var clsContextWrapper = Java.use("android.content.ContextWrapper")
        var clsPendingIntent = Java.use("android.app.PendingIntent")
        var clsIntent = Java.use("android.content.Intent")
        
        clsContextWrapper.sendBroadcast.overload("android.content.Intent").implementation = function(intent) {
            var ret = this.sendBroadcast(intent)
            console.log('Got sendBroadcast : '+intent.toURI())
            return ret
        }

        clsContextWrapper.sendBroadcast.overload('android.content.Intent','java.lang.String').implementation = function(intent,perm) {
            var ret = this.sendBroadcast(intent,perm)
            console.log('Got sendBroadcast with permission : '+intent.toURI()+'  perm: '+perm)
            return ret
        }

        clsContextWrapper.sendOrderedBroadcast.overload('android.content.Intent','java.lang.String').implementation = function(intent,perm) {
            var ret = this.sendOrderedBroadcast(intent,perm)
            console.log('Got sendOrderedBroadcast : '+intent.toURI() +' prem : '+perm)
            return ret
        }

        clsContextWrapper.sendOrderedBroadcast.overload('android.content.Intent', 'java.lang.String', 'android.content.BroadcastReceiver', 'android.os.Handler', 'int', 'java.lang.String', 'android.os.Bundle').implementation = function(intent,perm,result,scheduler,initcode,initdata,initextra) {
            var ret = this.sendOrderedBroadcast(intent,perm,result,scheduler,initcode,initdata,initextra)
            console.log('Got sendOrderedBroadcast[1] : '+intent.toURI())
            return ret
        }

        clsContextWrapper.sendStickyBroadcast.overload('android.content.Intent').implementation = function(intent) {
            var ret = this.sendStickyBroadcast(intent)
            console.log('Got sendStickyBroadcast : '+intent.toURI())
            return ret
        }

        clsContextWrapper.registerReceiver.overload('android.content.BroadcastReceiver','android.content.IntentFilter').implementation = function(receiver,intentfilter) {
            var ret = this.registerReceiver(receiver,intentfilter)
            var actionNum = intentfilter.countActions()
            var action = []
            for(var i = 0;i < actionNum;i++) {
                action.push(intentfilter.getAction(i))
            }
            console.log('Got registerReceiver : '+action)
            return ret
        }

        clsContextWrapper.registerReceiver.overload('android.content.BroadcastReceiver','android.content.IntentFilter','java.lang.String','android.os.Handler').implementation = function(receiver,intentfilter,perm,handler) {
            var ret = this.registerReceiver(receiver,intentfilter,perm,handler)
            var actionNum = intentfilter.countActions()
            var action = []
            for(var i = 0;i < actionNum;i++) {
                action.push(intentfilter.getAction(i))
            }
            console.log('Got registerReceiver : '+action)
            return ret
        }

        clsPendingIntent.getBroadcast.overload('android.content.Context', 'int', 'android.content.Intent', 'int').implementation = function(context,reqcode,intent,flags) {
            var ret = this.getBroadcast(context,reqcode,intent,flags)
            console.log('Got PendingIntent getBroadcast : '+ intent.toURI())
            return ret
        }
    })
}

function Service_hook() {
    /*
     * Service Hook 主要hook startService,stopService,bindService
     */
    Java.perform(function() {
        var clsContextWrapper = Java.use("android.content.ContextWrapper")
        var Intent = Java.use("android.content.Intent")
        var clsPendingIntent = Java.use("android.app.PendingIntent")
    
        clsContextWrapper.startService.implementation = function(intent) {
            var ret = this.startService(intent)
            console.log('Got startService : '+intent.toURI())
            return ret
        }

        clsContextWrapper.startForegroundService.implementation = function(intent) {
            var ret = this.startForegroundService(intent)
            console.log('Got startForegroundService : '+intent.toURI())
            return ret
        }

        clsContextWrapper.stopService.implementation = function(intent) {
            var ret = this.stopService(intent)
            console.log('Got stopService : '+intent.toURI())
            return ret
        }

        clsContextWrapper.bindService.overload('android.content.Intent', 'android.content.ServiceConnection', 'int').implementation = function(intent,conn,flags) {
            var ret = this.bindService(intent,conn,flags)
            console.log('Got bindService : '+intent.toURI())
            return ret
        }

        clsContextWrapper.bindService.overload('android.content.Intent', 'int', 'java.util.concurrent.Executor', 'android.content.ServiceConnection').implementation = function(intent,flags,exec,conn) {
            var ret = this.bindService(intent,flags,exec,conn)
            console.log('Got bindService[1] : '+intent.toURI)
            return ret
        }

        clsPendingIntent.getService.overload('android.content.Context', 'int', 'android.content.Intent', 'int').implementation = function(context,reqcode,intent,flags) {
            var ret = this.getService(context,reqcode,intent,flags)
            console.log('Got PendingIntent getService : '+intent.toURI())
            return ret
        }
    })    
}

function LocalBroadcast_hook() {
    /*
     * hook LocalBroadcastManager 不是所有的APP都会有LocalBroadcast
     */
    Java.perform(function() {
        var flag = true
        try{
            var clsLocalBroadcastManager = Java.use("androidx.localbroadcastmanager.content.LocalBroadcastManager")
        } catch(error) {
            try{
                console.log('failed to get androidx')
                clsLocalBroadcastManager = Java.use("android.support.v4.content.LocalBroadcastManager")
            } catch(error) {
                console.log('failed to get android.support.v4')
                flag = false
            }
        } finally {
            if (flag == true) {
                clsLocalBroadcastManager.sendBroadcast.implementation = function(intent) {
                    var ret = this.sendBroadcast(intent)
                    console.log('Got local sendBroadcast : '+intent.toURI())
                    return ret
                }
        
                clsLocalBroadcastManager.sendBroadcastSync.implementation = function(intent) {
                    var ret = this.sendBroadcastSync(intent)
                    console.log('Got local sendBroadcastSync : '+intent.toURI())
                    return ret
                }
        
                clsLocalBroadcastManager.registerReceiver.implementation = function(receiver,intentfilter) {
                    var ret = this.registerReceiver(receiver,intentfilter)
                    var actionNum = intentfilter.countActions()
                    var action = []
                    for(var i = 0;i < actionNum;i++) {
                        action.push(intentfilter.getAction(i))
                    }
                    console.log('Got local registerReceiver : '+action)
                    return ret
                }
            }
        }
    })
}