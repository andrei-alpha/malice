import sys, copy, ThreeAdrCode

class Emulate():
    
    def __init__(self):
        self.label = {}
        self.stack = []
        self.programCounter = []
        self.dataStack = []
        self.PC = 0
        self.run = True;
        self.p0 = 0

    def emulate(self, code):
        self.code = code
        for node in code:
            self.label[node.label] = code.index(node)

        self.dataStack.append({})
        self.execute()

    def execute(self):
        while self.run == True:
            node = self.code[self.PC]     

            if (node.name == 'decl'):
                self.Decl(node)
            elif (node.name == 'push'):
                self.Push(node)
            elif (node.name == 'pop'):
                self.Pop(node)
            elif (node.name == 'goto'):
                self.Goto(node)
            elif (node.name == 'return'):
                self.Return(node)
            elif (node.name == 'end'):
                self.End(node)
            elif (node.name == 'assign'):
                self.Assign(node)
            elif (node.name == 'print'):
                self.Print(node)
            elif (node.name == 'read'):
                self.Read(node)
            elif (node.name == 'call'):
                self.Call(node)
            elif (node.name == 'ifFalse'):
                self.IfFalse(node)  
            elif (node.name == 'ifTrue'):
                self.IfTrue(node)
            else:
                self.PC += 1

    def get(self, var):
        last = len(self.dataStack) - 1
        return self.dataStack[last][var]

    def getArr(self, arr, index):
        last = len(self.dataStack) - 1
        return self.dataStack[last][arr][index]

    def add(self, var, value):
        last = len(self.dataStack) - 1
        self.dataStack[last][var] = value 
    
    def addArr(self, arr, index, value):
        last = len(self.dataStack) - 1
        self.dataStack[last][arr][index] = value

    def declArr(self, arr, size):
        last = len(self.dataStack) - 1
        self.dataStack[last][arr] = [0] * size

    def Decl(self, node):
        var = node.getVar()
        if var.type == 'arr':
            size = self.getValue(var.index.name)
            self.declArr(var.name, size)
        self.PC += 1

    def Push(self, node):
        #print 'push', node.getVarName()
        self.stack.append(self.get(node.getVarName()))
        self.PC += 1       

    def Pop(self, node):
        #print 'pop', node.getVarName()
        self.add(node.getVarName(), self.stack.pop())
        self.PC += 1

    def Goto(self, node):
        self.PC = self.label[node.getVar()]

    def Return(self, node):
        self.PC = self.programCounter.pop()  
        var = node.getVar()
        if var.type == 'arr':
            index = self.getValue(var.index.name)
            result = self.getArr(var.name, index)
        else:
            result = self.getValue(var.name)
        self.dataStack.pop()
        self.add('#eax', result)
        

    def End(self, node):
        if not self.programCounter:
            self.run = False
        else:
            self.PC = self.programCounter.pop()

    def Call(self, node):
        self.programCounter.append(self.PC + 1)
        self.PC = self.label[node.children[0]]
        lastData = self.dataStack[-1]
        data = copy.deepcopy(lastData)
        self.dataStack.append(data)

    def getValue(self, var):
        if isinstance(var, int) or (isinstance(var, str) and var.isdigit()):
            return int(var)
        return self.get(var)

    def Assign (self, node):
        if node.Second():
            #binary expression
            var = node.getVar()
            operator = node.getOperator()
            left = node.First()
            if left.getType() == 'arr':
                index = self.getValue(left.index.name)
                left = self.getArr(left.name, index) 
            else:
                left = self.getValue(left.name)
            right = node.Second()
            if right.getType() == 'arr':
                index = self.getValue(right.index.name)
                right = self.getArr(right.name, index) 
            else:
                right = self.getValue(right.name)
            temp = self.computeValBinary(left, right, operator.oper)
            if (node.getVar().getType() == 'var'):
                self.add(var.name, temp) 
            else:
                index = self.getValue(var.index.name)
                self.addArr(var.name, index, temp)
            #print 'var', var, '=', temp
        else:
            if node.getOperator():
                #unary expression
                var = node.getVar()
                operator = node.getOperator()
                exp = node.First()
                if exp.getType == 'arr':
                    index = self.getValue(exp.index.name)
                    exp = self.getArr(exp.name, index)
                else:
                    exp = self.getValue(exp.name)
        
                temp = self.computeValUnary(exp, operator.oper)
                if (node.getVar().getType() == 'var'):
                    self.add(var.name, temp)
                else:
                    index = self.getValue(var.index.name)
                    self.addArr(var.name, index, temp)
            else:
                #var assignment
                var = node.getVar()
                exp = node.First()
                if exp.getType() == 'arr':
                    index = self.getValue(exp.index.name)
                    exp = self.getArr(exp.name, index)
                elif exp.getType() == 'var' or exp.getType() == 'funcreg':
                    exp = self.getValue(exp.name)

                if node.getVar().getType() == 'var':
                    ###print 'assign', var, exp
                    self.add(var.name, exp)
                else:
                    index = self.getValue(var.index.name)
                    self.addArr(var.name, index, exp) 
                #print 'var', var, '=', exp
        self.PC += 1

    def computeValBinary(self, left, right, operator):
        #print 'ask?', left, right, operator

        if (operator == '+'):
            return left + right
        elif (operator == '-'):
            return left - right
        elif (operator == '*'):
            return left * right
        elif (operator == '/'):
            return left / right
        elif (operator == '%'):
            return left % right
        elif (operator == '|'):
            return left | right
        elif (operator == '&'):
            return left & right
        elif (operator == '^'):
            return left ^ right
        elif (operator == '||'):
            return left or right
        elif (operator == '&&'):
            return left and right
        elif (operator == '=='):
            return (left == right)
        elif (operator == '!='):
            return (left != right)
        elif (operator == '<='):
            return (left <= right)
        elif (operator == '>='):
            return (left >= right)
        elif (operator == '<'):
            return (left < right)
        elif (operator == '>'):
            return (left > right)

    def computeValUnary(self, expr, operator):
        if (operator == '!'):
            return not(expr)
        elif (operator == '~'):
            return ~expr
        elif (operator == '-'):
            return -expr

                
    def Print(self, node):
        #if isinstance(node.children[0], str):
         #   print self.data[node.children[0]]
        #else
        var = node.getVar()        
        if var.type == 'arr':
            index = self.getValue(var.index.name)
            value = str( self.getArr(var.name, index) )   
        else:
            value = str( self.get(var.name) )
            if value[0] == '"' or value[0] == "'":
                value = value[1:-1]

        value = value.replace("\\" + "n", '\n') 
        sys.stdout.write(value)
        self.PC += 1

    def Read(self, node):
        var = node.getVar()
        value = input(" ")

        if var.type == 'arr':
            index = self.getValue(var.index.name)
            self.addArr(var.name, index, value)
        else:
            self.add(node.name, value)
        print ''
        self.PC += 1
    
    def IfTrue(self, node):
        if self.get(node.getVarName()) == True:
            self.PC = self.label[ node.getJump() ]
        else:
            self.PC += 1

    def IfFalse(self, node):
        if self.get(node.getVarName()) == True:
            self.PC += 1
        else:
            self.PC = self.label[ node.getJump() ]
