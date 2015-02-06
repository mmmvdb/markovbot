import random

class MarkovTree:
    def __init__(self):
        self.stopword = '\x03'
        self.chain_length = 2
        self.tree = {}
        self.maxwords = 50

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
        
    #TODO this is all assuming chain_length = 2
    def createMessage(self, seed):
        gen_words = []
        
        appendWord = self.stopword
        
        if seed in self.tree:
            gen_words.append(seed[0])
            gen_words.append(seed[1])
            
            appendWord = random.choice(self.tree[seed])
        
        while appendWord != self.stopword:
            gen_words.append(appendWord)
            
            key = (gen_words[-2], gen_words[-1])
            
            if key in self.tree:
                appendWord = random.choice(self.tree[key])
            else:
                appendWord = self.stopword

            if len(gen_words) >= self.maxwords:
                appendWord = self.stopword
                
        return ' '.join(gen_words)
