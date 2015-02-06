import socket
import urllib
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from time import clock

class MarkovTree:
    def __init__(self):
        self.stopword = '\x03'
        self.chain_length = 2
        self.tree = {}

    def addMessage(self, msg):
        words = msg.split()
        
        if len(words) > self.chain_length:
            words.append(self.stopword)
            
            for i in range(len(words) - self.chain_length):
                self.addToTree(words[i:i + self.chain_length + 1])
    
    #this needs to have list be a list of chain_length + 1
    def addToTree(self, list):
        key = tuple(list[:self.chain_length])
        value = list[-1]
        
        if key in self.tree:
            if value not in self.tree[key]:
                self.tree[key].append(value)
        else:
            self.tree[key] = [value]
    
    def printTree(self):
        return str(self.tree)


nick = 'Markovbot'
network = 'chat.freenode.net'
port = 8000
#chan = '#r/kansascity'
chan = '#bottesting'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((network,port))

irc.recv (4096)
irc.send('NICK ' + nick + '\r\n')
irc.send('USER ' + nick + ' 8 * :' + nick + '\r\n')
irc.send('JOIN ' + chan + '\r\n')

mTree = MarkovTree()

while True:
    data = irc.recv (4096)
    print data
    if data.find('PING') != -1:
        print 'PONG ' + data.split()[1]
        irc.send('PONG ' + data.split()[1] + '\r\n')
    
    if data.find('PRIVMSG ' + nick + ' :mbquit') != -1:
        print 'Quit due to PM command from' + nick
        irc.send('QUIT :Food\r\n')
        
    if data.find('PRIVMSG ' + nick + ' :mbprinttree') != -1:
        print mTree.printTree()
    
    if data.find('PRIVMSG ' + chan) > 0:
        print 'Adding message to MarkovTree ' + " ".join(data.split()[3:])[1:]
        mTree.addMessage(" ".join(data.split()[3:])[1:])
    
    if len(data) == 0:
        break;
    
