import serial
import argparse
import local
import modem
import menu

def dump_file(client,path):
    lines = open(path).readlines()
    for line in lines:
        client.send(line)

main = menu.Menu(None,"BBS ROOT")
main.add_entry("Read MOTD",lambda c:dump_file(c,"motd.txt"))

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
        connected = client.wait_for_call()
        if connected:
            print "Got call!"
            try:
                run_bbs(client)
            except Exception as e:
                print "GOT EXCEPT. SORRY",repr(e),e
        else:
            print "Lost call!"




