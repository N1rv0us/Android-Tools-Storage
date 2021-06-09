'''
 description : ssl unpining via frida
 author : N1rv0us
'''

import frida 
import idna
import base64
from socket import socket
from OpenSSL import SSL, crypto
import sys
import time

script = None

def get_certificate(hostname,port=443):
    sock = socket()
    sock.setblocking(True)
    sock.connect((hostname,port),)
    ctx = SSL.Context(SSL.TLSv1_2_METHOD)
    ctx.check_hosthame = False
    ctx.verify_mode = SSL.VERIFY_NONE

    socket_ssl = SSL.Connection(ctx,sock)
    socket_ssl.set_tlsext_host_name(idna.encode(hostname))
    socket_ssl.set_connect_state()
    socket_ssl.do_handshake()
    certs = socket_ssl.get_peer_cert_chain()
    socket_ssl.close()
    sock.close()
    
    return certs

def on_message(message,data):
    global script
    print(message)
    certs = get_certificate(message['payload'])
    pem_certs = []

    for cert in certs:
        pem_certs.append(base64.b64encode(crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)).decode())

    script.post({'type': 'input', 'payload': pem_certs})

def frida_part(process):
    global script
    script_path = "./script.js"
    fp = open(script_path)

    device = frida.get_usb_device()
    pid = device.spawn([process])
    
    time.sleep(1)
    session = device.attach(pid)
    script = session.create_script(fp.read())
    script.on('message',on_message)
    script.load()
    device.resume(pid)
    sys.stdin.read()


if __name__ == "__main__":
    # test for script
    frida_part("com.UCMobile")
    # certs = get_certificate("www.mi.com")
    # for cert in certs :
    #     print(crypto.dump_certificate(crypto.FILETYPE_ASN1, cert))