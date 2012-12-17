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
        print '--------------- Emulator ---------------'
        self.code = code
        for node in code:
            self.label[node.label] = code.index(node)

        self.dataStack.append({})
        self.execute()

    def execute(self):
        while self.run:
            node = self.code[self.PC]     

            methname = 'eval_%s' % node.name
            method = getattr(self, methname, self.eval_default)
            method(node)

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

    def eval_default(self, node):
        self.PC += 1

    def eval_decl(self, node):
        var = node.getVar()
        if var.type == 'arr':
            size = self.toValue(var.index.name)
            self.declArr(var.name, size)
        self.PC += 1

    def eval_push(self, node):
        self.stack.append(self.get(node.getVarName()))
        self.PC += 1       

    def eval_param(self, node):
        pos = node.getPos()
        self.add(node.getVarName(), self.stack[-(pos+1)])
        self.PC += 1

    def eval_pop(self, node):
        times = node.getNo()
        self.stack = self.stack[:-times]
        self.PC += 1

    def eval_goto(self, node):
        self.PC = self.label[node.getVar()]

    def eval_return(self, node):  
        result = self.getValue( node.getVar() )
        last = len(self.dataStack) - 2
        self.dataStack[last]['#rax'] = result
        self.PC += 1

    def eval_end(self, node):
        if not self.programCounter:
            self.run = False
        else:
            self.dataStack.pop()
            self.PC = self.programCounter.pop()

    def eval_call(self, node):
        self.programCounter.append(self.PC + 1)
        self.PC = self.label[node.children[0]]
        lastData = self.dataStack[-1]
        data = copy.deepcopy(lastData)
        self.dataStack.append(data)

    def toValue(self, var):
        if isinstance(var, int) or (isinstance(var, str) and var.isdigit()):
            return int(var)
        return self.get(var)

    def getValue(self, var):
        if var.type == 'arr':
            index = self.toValue(var.index.name)
            return self.getArr(var.name, index)
        return self.toValue(var.name)

    def setValue(self, var, temp):
        if var.type == 'arr':
            index = self.toValue(var.index.name)
            self.addArr(var.name, index, temp)    
        else:
            self.add(var.name, temp)

    def eval_assign (self, node):
        if node.Second():
            #binary expression
            var = node.getVar()
            operator = node.getOperator()
            left = self.getValue( node.First() )
            right = self.getValue( node.Second() )
            temp = eval( str(left) + str(operator) + str(right) )
            self.setValue(var, temp)
            #print '#1 assign', var, temp
        else:
            if node.getOperator():
                #unary expression
                var = node.getVar()
                operator = node.getOperator()
                exp = self.getValue( node.First() )
                temp = eval( str(operator) + str(exp) )
                self.setValue(var, temp)
                #print '#2 assign', var, temp
            else:
                #var assignment
                var = node.getVar()
                exp = node.First()
                if exp.type == 'arr' or exp.type == 'var' or exp.type == 'funcreg':
                    exp = self.getValue(exp)
                self.setValue(var, exp)
                #print '#3 assign', var, exp
        self.PC += 1

    def eval_print(self, node):
        val = str( self.getValue( node.getVar() ) )     
        val = val.replace('"', '')
        val = val.replace("'", '')
        val = val.replace("\\" + "n", '\n') 
        sys.stdout.write(val)
        self.PC += 1

    def eval_read(self, node):
        var = node.getVar()
        value = input(" ")

        if var.type == 'arr':
            index = self.getValue(var.index.name)
            self.addArr(var.name, index, value)
        else:
            self.add(var.name, value)
        self.PC += 1
    
    def eval_if(self, node):
        first = self.getValue( node.First() )
        second = self.getValue( node.Second() )
        if eval( str(first) + str(node.getOperator()) + str(second) ) == True:
            self.PC = self.label[ node.getJump() ]
        else:
            self.PC += 1

