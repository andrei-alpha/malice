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

    def getArr(self, arr, index, value):
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
        self.stack.append(self.get(node.getVarName()))
        #print 'push', self.get(node.getVarName())
        self.PC += 1       

    def Pop(self, node):
        self.add(node.getVarName(), self.stack.pop())
        print 'pop', self.get(node.getVarName())
        self.PC += 1

    def Goto(self, node):
        #print node.children[0]
        self.PC = self.label[node.getVar()]

    def Return(self, node):
        self.PC = self.programCounter.pop()  #self.stack.pop()
        #print 'return', self.PC
        #self.p0 = self.data[node.getVarName()]
        result = self.get(node.getVarName())
        self.dataStack.pop()
        self.add('#eax', result)
        #self.data['#eax'] = self.data[node.getVarName()]

    def End(self, node):
        if not self.stack:
            self.run = False
        else:
            self.stack.pop(self.PC)

    def Call(self, node):
        #self.stack.append(self.PC + 1)
        self.programCounter.append(self.PC + 1)
        #print 'append', self.PC + 1
        #print 'pop', self.stack.pop()
        #self.PC = self.code.index(node) 
        self.PC = self.label[node.children[0]]
        #print 'call', self.PC
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
                self.add(var.name, temp)  #self.data[var] = temp
            else:
                index = self.getValue(var.index.name)
                self.addArr(var.name, index, temp)
            #print 'var', var, self.get(var)
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
                #print 'var', var, self.get(var)
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
        value = str( self.get(node.getVarName()) )
        if value[0] == '"' or value[0] == "'":
            value = value[1:-1]

        sys.stdout.write(value)
        self.PC += 1

    def Read(self, node):
        self.add(node.getVarName(), input(" "))
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
