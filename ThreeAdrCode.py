import CodeGenerator

class CodeNode(object):
    def __init__(self, name, label, children, single = False):
        self.name = name
        self.label = label
        self.single = single
        self.children = children

    def isFuncCall(self):  
        return isinstance(self, Call)
 
    def isOnlyJump(self):
        return isinstance(self, Return) or isinstance(self, Goto) or self.isFuncCall()

    def getVar(self):
        return self.children[0]

    def getVarName(self):
        return self.children[0].name

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
        super(Push, self).__init__('push', label, children, True)

class Pop(CodeNode):
    def __init__(self, label, children):
        super(Pop, self).__init__('pop', label, children, True)

class Goto(CodeNode):
    def __init__(self, label, jump):
        super(Goto, self).__init__('goto', label, [jump])

class Return(CodeNode):
    def __init__(self, label, children):
        super(Return, self).__init__('return', label, children, True)
    
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
        if len(self.children) == 4:
            return self.children[3]
        return self.children[2]

    def FirstName(self):
        if len(self.children) == 4:
            return self.children[3].name
        return self.children[2].name
    
    def Second(self):
        if len(self.children) == 5:
            return self.children[4]
        return None

    def SecondName(self):
        if len(self.children) == 5:
            return self.chilren[4].name
        return ""

class Print(CodeNode):
    def __init__(self, label, var):
        super(Print, self).__init__('print', label, [var], True)

class Read(CodeNode):
    def __init__(self, label, var):
        super(Read, self).__init__('read', label, [var], True)

class Call(CodeNode):
    def __init__(self, label, name):
        super(Call, self).__init__('call', label, [name])

    def getJump(self):
        return self.children[0]

class Decl(CodeNode):
    def __init__(self, label, children):
        super(Decl, self).__init__('decl', label, children)

class If(CodeNode):
    def __init__(self, label, children):
        super(If, self).__init__('if', label, children, True)

    def First(self):
        return self.children[0]

    def Second(self):
        return self.children[2]

    def getOperator(self):
        return self.children[1]

    def getJump(self):
        return self.children[4]

class Void(CodeNode):
    def __init__(self, name, label, children):
        super(Void, self).__init__(name, label, children)

class Func(CodeNode):
    def __init__(self, name, label, children):
        super(Func, self).__init__(name, label, children)

