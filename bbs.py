import serial
import argparse
import local
import modem

def run_bbs(client):
    lines = open("splash.txt").readlines()
    for line in lines:
        client.send(line)
    client.hangup()

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-p","--port",default="/dev/ttyACM0",
                   help="Port that modem resides on")
    p.add_argument("-l","--local",action="store_true",default=False,
                   help="Operate in local mode for testing")
    args = p.parse_args()
    if args.local:
        print "local"
        client = local.Client()
    else:
        client = modem.Client(args.port)
    while True:
        connected = client.wait_for_call()
        if connected:
            print "Got call!"
            try:
                run_bbs(client)
            except Exception as e:
                print "GOT EXCEPT. SORRY",repr(e),e
        else:
            print "Lost call!"




