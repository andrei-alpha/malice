#!bin/python
import Lexer

class Parser(object):
    
    def parse(self, Input):
        
        fin1 = open("output1.txt", "w")
        self.lexer = Lexer.Lexer()
        data = self.lexer.tokenize(Input)
        for token in data:
            fin1.write( str(token) + "\n" )
        fin1.close()
  
    def generateAST(self):
        pass

    def __init__(self):
        pass
