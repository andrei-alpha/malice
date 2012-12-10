import CodeGenerator

class CodeNode(object):
    def __init__(self, name, label, children):
        self.name = name
        self.label = label
        self.children = children

    def isFuncCall(self):  
        return isinstance(self, Call)
 
    def isOnlyJump(self):
        return isinstance(self, Return) or isinstance(self, Goto) or self.isFuncCall()

    def __str__(self):
        s = ''

        if not self.label == '':
            s += str(self.label) + ': '
        if not self.name == 'assign':
            s += self.name + ' '
        for child in self.children:
            s += str(child) + ' '

        return s

class Push(CodeNode):
    def __init__(self, label, children):
        super(Push, self).__init__('push', label, children)

    def getVar():
        return self.children[0]

class Pop(CodeNode):
    def __init__(self, label, children):
        super(Pop, self).__init__('pop', label, children)

    def getVar():
        return self.children[0]

class Goto(CodeNode):
    def __init__(self, label, jump):
        super(Goto, self).__init__('goto', label, [jump])

class Return(CodeNode):
    def __init__(self, label, children):
        super(Return, self).__init__('return', label, children)
    
    def getVar():
        return self.children[0]

class End(CodeNode):
    def __init__(self, label, children):
        super(End, self).__init__('end', label, children)

class Assign(CodeNode):
    def __init__(self, label, children):    
        super(Assign, self).__init__('assign', label, children)
    
    def getOperator(self):
        if len(self.children) > 2 and isinstance(self.children[2], CodeGenerator.Operator):
            return self.children[2]
        elif len(self.children) > 3 and isinstance(self.children[3], CodeGenerator.Operator):
            return self.children[3]
        return None

    def First(self):
        return self.children[0]

    def Second(self):
        if len(self.children) == 4:
            return self.children[3]
        return self.children[2]
    
    def Third(self):
        if len(self.children) == 5:
            return self.children[4]
        return None

class Print(CodeNode):
    def __init__(self, label, var):
        super(Print, self).__init__('print', label, [var])

class Read(CodeNode):
    def __init__(self, label, var):
        super(Read, self).__init__('read', label, [var])

class Call(CodeNode):
    def __init__(self, label, name):
        super(Call, self).__init__('call', label, [name])

    def getJump(self):
        return self.children[0]

class IfTrue(CodeNode):
    def __init__(self, label, children):
        super(IfTrue, self).__init__('ifTrue', label, children)

    def getJump(self):
        return self.children[2]

class Decl(CodeNode):
    def __init__(self, label, children):
        super(Decl, self).__init__('decl', label, children)

class IfFalse(CodeNode):
    def __init__(self, label, children):
        super(IfFalse, self).__init__('ifFalse', label, children)

    def getJump(self):
        return self.children[2]

class Void(CodeNode):
    def __init__(self, name, label, children):
        super(Void, self).__init__(name, label, children)

class Func(CodeNode):
    def __init__(self, name, label, children):
        super(Func, self).__init__(name, label, children)

