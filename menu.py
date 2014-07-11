
class Menu:
    def __init__(self,parent,title,description='Select an entry:'):
        self.parent = parent
        self.title = title
        self.description = description
        self.entries = []
    def add_entry(self,text,fn):
        self.entries.append((text,fn))
    def display(self,client):
        client.send(self.title+"\n")
        client.send(self.description+"\n")
        for i in range(len(self.entries)):
            client.send("{0}. {1}\n".format(i+1,self.entries[i][0]))
        if self.parent:
            client.send("0. Back to {0}\n".format(self.parent.title))
        else:
            client.send("0. LOG OUT\n")
    def run(self,client):
        self.display(client)
        while 1:
            c = client.getch()
            try:
                choice = int(c)
                if choice == 0:
                    return
                if choice < (len(self.entries)+1):
                    self.entries[choice-1][1](client)
                    self.display(client)
            except ValueError as e:
                pass #print e
