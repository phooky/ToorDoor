import time
import pickle

class Post:
    def __init__(self):
        self.time = time.localtime()
        self.content = ""
        self.author = "<anon>"
    def run(self,client):
        t = time.strftime("%D %H:%M",self.time)
        client.send("{0} by {1}\n".format(t,self.author))
        client.send(self.content)
        client.send("\n --- any key to continue ---\n")
        client.getch()
    def edit(self,client):
        client.send("New post. Enter your name: ")
        self.author = client.getline().strip()
        client.send("Enter your message now. Two blank lines to finish.\n")
        blanks = 0
        m = ""
        while 1:
            l = client.getline().strip()
            if len(l) == 0:
                blanks = blanks + 1
            else:
                blanks = 0
            if blanks > 1:
                break;
            else:
                m = m + l + "\n"
        self.content = m
        client.send("--- message posted ---\n")

class Topic:
        def __init__(self,name):
            self.name = name
            self.posts = []
        def display(self,client,page=0):
            client.send("**TOPIC {0}**\n".format(self.name))
            client.send("SELECT OPTION\n")
            first = page*10
            num = min(len(self.posts)-first,10)
            for i in range(num):
                p = self.posts[i+first]
                t = time.strftime("%D %H:%M",p.time)
                content = p.content.split('\n')[0]
                l = "{0}. {1:30s} {2}\n".format(i,content[:30],t)
                client.send(l)
            if len(self.posts) > num+first:
                client.send("N. Next page\n")
            if page > 0:
                client.send("P. Previous page\n")
            client.send("+. Post to topic\n")
            client.send("X. Exit topic\n")
        def run(self,client,board):
            page = 0
            lastpg = len(self.posts)/10
            while 1:
                self.display(client,page)
                while 1:
                    c = client.getch()
                    if c == "+":
                        p = Post()
                        p.edit(client)
                        self.posts.append(p)
                        pickle.dump(board, open('board.pickle','wb'))
                        self.display(client,page)
                    if c == "X" or c == "x":
                        return
                    if page < lastpg and c == "N" or c == "n":
                        page = page + 1
                        self.display(client,page)
                    if page > 0 and c == "P" or c == "p":
                        page = page - 1
                        self.display(client,page)
                    try:
                        choice = int(c)
                        if choice < (len(self.posts)-page*10):
                            self.posts[page*10+choice].run(client)
                            self.display(client,page)
                    except ValueError as e:
                        pass

class Board:
    def __init__(self):
        self.topics = []

    def display(self,client):
        client.send("SELECT A MESSSAGE BOARD:\n")
        for i in range(len(self.topics)):
            t = self.topics[i]
            l = "{0}. {1:40s}\n".format(i,t.name)
            client.send(l)
        client.send("X. Exit message board\n")
    def run(self,client):
        self.display(client)
        while 1:
            c = client.getch()
            if c == "A":
                # hidden add topic
                client.send("ENTER TOPIC:")
                ts = client.getline()
                self.topics.append(Topic(ts.strip()))
                self.display(client)
                pickle.dump(self, open('board.pickle','wb'))
            if c == "X" or c == "x":
                return
            try:
                choice = int(c)
                if choice < (len(self.topics)):
                    self.topics[choice].run(client,self)
                    self.display(client)
            except ValueError as e:
                pass
    
