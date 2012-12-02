import re
import lex

class Lexer(object):
    errors = []
    reserved = {
     'a': 'A',
     'Alice': 'ALICE',
     'and': 'AND',
     'ate': 'ATE',
     'became': 'BECAME',
     'because': 'BECAUSE',
     'but': 'BUT',
     'closed': 'CLOSED',
     'contained': 'CONTAINED',
     'drank': 'DRANK',
     'either': 'EITHER',
     'enough': 'ENOUGH',
     'eventually': 'EVENTUALLY',
     'found': 'FOUND',
     'glass': 'GLASS',
     'had': 'HAD',
     'letter': 'LETTER',
     'looking': 'LOOKING',
     'maybe': 'MAYBE',
     'number': 'NUMBER',
     'of': 'OF',
     'or': 'OR',
     'opened': 'OPENED',
     'perhaps': 'PERHAPS',
     'piece': 'PIECE',
     'room': 'ROOM',
     's': 'S',
     'said': 'SAID',
     'sentence': 'SENTENCE',
     'so': 'SO',
     'spider': 'SPIDER',
     'spoke': 'SPOKE',
     'The': 'THE',
     'then': 'THEN',
     'times': 'TIMES',
     'too': 'TOO',
     'unsure': 'UNSURE',
     'was': 'WAS',
     'what': 'WHAT',
     'which': 'WHICH'}
    literals = ['.',
     ',',
     '*',
     '%',
     '+',
     '-',
     '/',
     '(',
     ')',
     '?',
     '|',
     '&',
     '^',
     '~',
     '{',
     '}']
     
    t_LOGICAL_OR    = "\\|\\|"
    t_LOGICAL_AND   = "&&"
    t_LOGICAL_NOT   = "!"
    t_EQUAL         = "=="
    t_GREATER_EQUAL = ">="
    t_LESS_EQUAL    = "<="
    t_NOT_EQUAL     = "!="
    t_LESS          = "<"
    t_GREATER       = ">"
    t_APOSTROPHE    = "'"  

    tokens = [
#        'PLUS',
#        'MINUS',
#        'MULTIPLY',
#        'DIVIDE',
#        'BINARY_OR',
#        'BINARY_AND',
#        'BINARY_EX_OR',
#        'BINARY_COMP',
        'CHAR_LITERAL',
        'STRING_LITERAL',
        'APOSTROPHE',
        'LOGICAL_OR', 
        'LOGICAL_AND', 
        'LOGICAL_NOT',
        'EQUAL',
        'GREATER_EQUAL',
        'LESS_EQUAL',
        'NOT_EQUAL',
        'LESS',
        'GREATER',
        'ID',
        'INT_LITERAL'] + list(reserved.values() )
      
    def t_ID(self, t):
        r"[a-zA-Z][a-zA-Z0-9_]*"
        t.type = self.reserved.get(t.value, "ID")
        return t

    def t_INT_LITERAL(self, t):
        r"\d+"
        t.value = int(t.value)
        return t
       
    def t_CHAR_LITERAL(self, t):
        r"\'.\'"
        t.value = t.value[1:-1]
        return t        

    def t_STRING_LITERAL(self, t):
        r"\".*\""
        t.value = t.value[1:-1]
        return t

    def t_COMMENT(self, t): 
        r"\#.*\n"  
        t.lexer.lineno += 1

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_SPACE(self, t):
        r"\s"
        pass

    def t_error(self, t):
        t.lexer.skip(1)
        self.errors.append( ("Unknown symbol", t.value) )

    def __init__(self):
        self.lexer = lex.lex(module = self)

    def tokenize(self, Input):
        self.lexer.input(Input)
    
        tokens = []
        for tok in iter(self.lexer.token, None):
            tokens.append( (repr(tok.type), repr(tok.value)) )
        return tokens
    
    
