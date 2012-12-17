class Mov(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        if self.reg1 == self.reg2:
            return ''
        return 'mov ' + self.reg1 + ', ' + self.reg2

class Add(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'add ' + self.reg1 + ', ' + self.reg2

class Sub(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'sub ' + self.reg1 + ', ' + self.reg2

class Or(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'or ' + self.reg1 + ', ' + self.reg2

class And(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2
    
    def __str__(self):
        return 'and ' + self.reg1 + ', ' + self.reg2

class Xor(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'xor ' + self.reg1 + ', ' + self.reg2

class Not(object):
    def __init__(self, reg):
        self.reg = reg
     
    def __str__(self): 
        return 'not ' + self.reg

class Neg(object):
    def __init__(self, reg):
        self.reg = reg

    def __str__(self):
        return 'not ' + self.reg

class Imul(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'imul ' + self.reg1 + ', ' + self.reg2

class Idiv(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        inst = 'mov rax, ' + self.reg1 + '\n' 
        inst += 'mov rdx, 0\n'
        inst += 'idiv ' + self.reg2
        return inst

class ArrDecl(object):
    def __init__(self, name, size):
        self.name = name
        self.size = getArrSize(size)

    def __str__(self):
        inst = self.name + ' dq '
        inst += '0,' * (self.size - 1) + '0'
        return inst

class StrDecl(object):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
        self.len = len(expr)

    def __str__(self):
        return self.name + ' db `' + self.expr + '`, 0'

class Jump(object):
    def __init__(self, label, name = ''):
        self.name = name
        self.jump = label

    def __str__(self):
       return ('jmp' if self.name == '' else self.name) + ' ' + self.jump

class Cmp(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'cmp ' + self.reg1 + ', ' + self.reg2

class Pop(object):
    def __init__(self, reg):
        self.reg = reg

    def __str__(self):
        return 'pop ' + self.reg

class Push(object):
    def __init__(self, reg):
        self.reg = reg

    def __str__(self):
        return 'push ' + self.reg

def getArrSize(size):
    if isinstance(size, int):
        return size
    if isinstance(size, str) and size.isdigit():
        return int(size)
    return 110
