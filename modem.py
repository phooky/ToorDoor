import serial
import re
import time
import sys

connectre = re.compile("CONNECT ([0-9]+)")

class TimeoutError(RuntimeError):
    pass

class NoCarrierError(RuntimeError):
    pass


class Client:
    def __init__(self,port):
        self.portname = port
        self.p = serial.Serial(port)
        # Set up call
        self.do_hayes("atz","OK")
        self.do_hayes("ats0=1","OK")

    def do_hayes(self,command,rsp,timeout=3):
        self.p.write(command+"\r")
        self.wait_for(rsp,timeout)
        print "Did command",command,rsp

    def wait_for(self,text,timeout=None):
        self.p.timeout = timeout
        l = ""
        while not l.startswith(text):
            l = self.p.readline()
            if len(l) == 0:
                raise TimeoutError()
        print "[{0}]".format(l.strip())
        return l.strip()

    def wait_for_call(self):
        try:
            self.wait_for("RING")
            print "Incoming ring!"
            l = self.wait_for("CONNECT",30)
            m = connectre.match(l)
            try:
                speed = int(m.group(1))
                print "Connected at {0}".format(speed)
            except:
                pass
            return True
        except TimeoutError:
            return False

    def send(self,text,norepl=False):
        if norepl:
            self.p.write(text)
        else:
            self.p.write(text.replace('\n','\r\n'))
        self.p.flush()

    def getch(self):
        self.p.timeout = 160
        c= self.p.read(1)
        #sys.stdout.write("{0:02x} {1}".format(ord(c[0]),c))
        #sys.stdout.flush()
        if len(c) == 0:
            print "Timeout on read!"
            raise TimeoutError()
        if ord(c[0]) == 0xff:
            print "Lost carrier!"
            raise NoCarrierError()
        return c

    def getline(self):
        m = ""
        while 1:
            c = self.getch()
            self.send(c)
            m = m + c
            if len(c) == 0 or c == '\n':
                return m

    def hangup(self):
        time.sleep(1)
        self.p.write("+++")
        self.p.flush()
        time.sleep(1)
        self.do_hayes("ATH0","OK")

