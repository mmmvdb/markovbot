import socket
import urllib
import markovTree
import random
import re

nick = 'markovbot'
network = 'chat.freenode.net'
port = 8000
chan = '#r/kansascity'
#chan = '#bottesting'
treexml = 'rkc.xml'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((network,port))

irc.recv (4096)
irc.send('NICK ' + nick + '\r\n')
irc.send('USER ' + nick + ' 8 * :' + nick + '\r\n')
irc.send('JOIN ' + chan + '\r\n')

mTree = markovTree.MarkovTree()

try:
    mTree.importTreeFromXML(treexml)
except IOError:
    print 'Error loading tree from XML. Continuing with empty tree.'
    
    
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

    if data.lower().find('privmsg ' + chan + ' :'+ nick) != -1:
        print 'Trying to print a message'
        
        #again this assumes chain of 2
        if len(data.split()) > 5:
            print (data.split()[4],data.split()[5])
            print mTree.createMessage((data.split()[4].lower(),data.split()[5].lower()))
        
    if data.find('PRIVMSG ' + chan) > 0 and data.lower().find('privmsg ' + chan + ' :'+ nick) == -1:
        print 'Adding message to MarkovTree "' + " ".join(data.split()[3:])[1:]+ '"'
        addMsg = " ".join(data.split()[3:])[1:].lower()
        
        mTree.addMessage(re.sub(r'[^a-zA-Z0-9= ]','',addMsg))

    if len(data) == 0:
        break;
    
mTree.writeTreeToXML(treexml)