
if (Java.available) {
    Java.perform(function() {
        var certCache = {};

        var SSLUtils = Java.use("com.android.org.conscrypt.SSLUtils");
        var Base64 = Java.use("android.util.Base64");

        function getCert(server_name) {
            var certs = certCache[server_name];
            if (certs == null) {
                var der_certs = [];
                send(server_name);

                var op = recv('input', function(value) {
                    Java.perform(function() {
                        for (var index in value.payload) {
                            der_certs.push(Base64.decode(value.payload[index],2))
                        }
                    });
                });

                op.wait();

                certs = Java.array('[B',der_certs);
                certCache[server_name] = certs
            }

            return certs
        }

        var NativeSsl = Java.use("com.android.org.conscrypt.NativeSsl");
        NativeSsl.getPeerCertificates.implementation = function() {
            return SSLUtils.decodeX509CertificateChain(getCert(this.getRequestedServerName()))
        };

        var ConscryptEngine = Java.use("com.android.org.conscrypt.ConscryptEngine")
        ConscryptEngine.verifyCertificateChain.implementation = function(certChain, authMethod){
            return this.verifyCertificateChain(getCert(this.getPeerHost()), authMethod)
        };
    });
}