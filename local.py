import sys

class Client:
    def __init__(self):
        pass
    def wait_for_call(self):
        return True

    def wait_for(self,text,timeout=None):
        l = ""
        while not l.startswith(text):
            l = sys.stdin.readline()
            if len(l) == 0:
                raise TimeoutError()
        print "[{0}]".format(l.strip())
        return l.strip()

    def send(self,text):
        sys.stdout.write(text)

    def getch(self):
        sys.stdin.flush()
        return sys.stdin.read(1)

    def getline(self):
        return sys.stdin.readline()

    def hangup(self):
        sys.stdout.write("HANGUP\n")

