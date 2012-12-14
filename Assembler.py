import ThreeAdrCode, Emulator

class Assembler():

    def __init__(self):
        self.asm = []
        self.data = []
        self.asm_comp = {'==': 'je', '<': 'jlt', '>': 'jgt', '<=': 'jle', '>=': 'jge'}

    def generate(self, code):
        self.code = code
        for inst in code:
            str_num = 1
            arr_num = 1
            if inst.name == 'assign':
                if inst.First().type == 'str':
                    self.data.append(('str' + str(str_num) + ' db ' + '"' + inst.FirstName()) + '", ' + len(inst.FirstName()) + ', 0')
                    str_num += 1
            elif inst.name == 'decl':
                if inst.First().type == 'arr':
                    self.data.append('arr' + str(arr_num) + ' dq ')
                    arr_num += 1
                    length = inst.FirstName().index
                    print 'hey', self.getValue(inst.First().index).type
                    for j in xrange (length):   #length - 1
                        self.data.append('0, ')
                    self.data.append('0')
            self.execute(inst)
        for data in self.data:
            print data
        for data in self.asm:
            print data
            
    def getName(self, reg):
        return str(reg)

    def getValue(self, var):
        if isinstance(var, int) or (isinstance(var, str) and var.isdigit()):
            print 'here'
            return int(var)

        else:
            return var

    def addCode(self, line):
        self.asm.append(line)

    def execute(self, inst):
        if inst.name == 'push':
            self.Push(inst)
        elif inst.name == 'pop':
            self.Pop(inst)
        elif inst.name == 'goto':
            self.Goto(inst)
        elif inst.name == 'return':
            self.Return(inst)
        elif inst.name == 'end':
            self.End(inst)
        elif inst.name == 'assign':
            self.Assign(inst)
        elif inst.name == 'ifFalse':
            sef.IfFalse(inst)
        elif inst.name == 'ifTrue':
            self.IfTrue(inst)
        elif inst.name == 'Decl':
            self.Decl(inst)
        elif inst.name == 'Print':
            self.Print(inst)

    def Push(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'push ' + reg
        self.addCode(line)

    def Pop(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'pop ' + reg
        self.addCode(line)

    def Goto(self, inst):
        label = self.getName(inst.getVar())
        line = 'jmp ' + label
        self.addCode(line)

    def Return(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'mov ' + reg + 'eax'
        self.addCode(line)
        line = 'pop ' + reg
        self.addCode(line)
        self.addCode('ret')

    def End(self, inst):
        self.addCode('end')

    def Assign(self, inst):
        if inst.Second():
            #binary expression
            var = inst.getVar()  #self.getName(inst.getVar())
            first = inst.First()
            second = inst.Second()
            operator = inst.getOperator()      

            if first.type == 'arr':
                left = 'rbx'
                self.addCode('mov [' + first.name + '+' + first.index.name + '],' + left)
            else:
                left = first.name
                
            if second.type == 'arr':
                right = 'rcx'
                self.addCode('mov [' + second.name + '+' + second.index.name + '], ' + right)
            else:
                right = second.name

            self.computeBinary(left, right, operator.oper)

            if var.type == 'arr':
                self.addCode('mov[' + var.name + '+' + var.index.name + '], rax')
            else:
                self.addCode('mov ' + var.name + ' rax') 
        else:
            if inst.getOperator():
                #unary expression
                var = self.getName(inst.getVar())
                operator = inst.getOperator()
                exp = inst.First()
                if exp.type == 'arr':
                   self.addCode('mov [' + exp.name + '+' + exp.index.name + '], ' + exp)
                else:
                    exp = exp.name
                self.computeUnary(exp, operator.oper)
                if var.type == 'arr':
                    self.addCode('mov[' + var.name + '+' + var.index.name + '], rax')
                else:
                    self.addCode('mov ' + var.name + ' rax')
            else:
                #var assignment
                var = inst.getVar()
                exp = inst.First()
                if exp.type == 'arr':
                    self.addCode('mov[' + exp.name + '+' + exp.index.name + '], ' + exp)
                else:
                    exp = exp.name
                if var.type == 'arr':
                    self.addCode('mov[' + var.name + '+' + var.index.name + '], ' + exp)
                else:
                    self.addCode('mov ' + var.name + ' ' + exp)


    def computeBinary(self, left, right, operator):
        if (operator == '+'):
            self.addCode('mov rax ' + ', ' + left)
            self.addCode('add rax' + ', ' + right)
        elif (operator == '-'):
            self.addCode('mov rax' + ', ' + left)
            self.addCode('sub rax' + ', ' + right)
        elif (operator == '*'):
            self.addCode('mov rax ' + ', ' + left)
            self.addCode('imul ' + right)
        elif (operator == '/'):
            self.addCode('mov rax ' + ', ' + left)
            self.addCode('idiv ' + right)
        elif (operator == '%'):
            pass
        elif (operator == '|' or operator == '||'):
            self.addCode('mov rax' + ', ' + left)
            self.addCode('or ' + var + ', ' + right)
        elif (operator == '&' or operator == '&&'):
            self.addCode('mov rax' + ', ' + left)
            self.addCode('and rax' + ', ' + right)
        elif (operator == '^'):
            self.addCode('mov rax' + ', ' + left)
            self.addCode('xor rax' + ', ' + right)
                   
 
    def computeUnary(self, exp, operator):
        if operator == '!':
            self.addCode('not ' + exp)
        elif operator == '-':
            self.addCode('neg ' + exp)
        elif operator == '~':
            self.addCode('neg ' + exp) #TO DO

    def If(self, inst):
        left = self.getName(inst.First())
        op = inst.getOperator()
        right = self.getName(inst.Second())
        jump = inst.getJump()
        self.addCode('cmp ' + left + right)
        self.addCode(self.asm_comp[op] + ' ' + jump) 

    def Decl(self, inst):
        pass

    def Print(self, inst):
        pass
