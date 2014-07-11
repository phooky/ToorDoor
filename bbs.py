import serial
import argparse
import local
import modem
import menu
import board
import pickle
import time
import sys

def dump_file(client,path):
    lines = open(path).readlines()
    for line in lines:
        client.send(line)

bbs = None

try:
    bbs = pickle.load(open('board.pickle','rb'))
    print "Loaded saved board."
except Exception as e:
    print "Couldn't load board:",e
    bbs = board.Board()

main = menu.Menu(None,"BBS ROOT")
main.add_entry("Read MOTD",lambda c:dump_file(c,"motd.txt"))
main.add_entry("Enter message board",lambda c:bbs.run(c))

def run_bbs(client):
    dump_file(client,"splash.txt")
    main.run(client)
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
        print "Waiting for call."
        sys.stdout.flush()
        connected = client.wait_for_call()
        print "Starting at",time.strftime("%D %H:%M",time.localtime())
        sys.stdout.flush()
        if connected:
            print "Got call!"
            try:
                run_bbs(client)
            except Exception as e:
                print "GOT EXCEPT. SORRY",repr(e),e
        else:
            print "Lost call!"
        print "Ending at",time.strftime("%D %H:%M",time.localtime())
        print "-------------------"
        sys.stdout.flush()




