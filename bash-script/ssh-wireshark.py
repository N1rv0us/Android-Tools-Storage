#! /usr/local/bin/python3 
'''
    description : ssh -> tcpdump -> wireshark  command script
    author : N1rv0us
'''

import argparse
import subprocess

global server_ip

def init():
    global server_ip, passwd
    parser = argparse.ArgumentParser(description="ssh -> tcpdump -> wireshark  command script")
    parser.add_argument('--target_ip',help="Router/Server IP Address")

    args = parser.parse_args()

    server_ip = args.target_ip
    

def run():
    global server_ip, passwd
    cmd = "ssh root@{0} tcpdump -U -s0 -w - 'not port 22' | wireshark -k -i -".format(server_ip)
    print('[+] cmd :'+cmd)
    s = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    out,err = s.communicate()
    if err is not None:
        return err
    
    return out


if __name__ == "__main__":
    init()
    run()
