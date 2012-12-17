import ThreeAdrCode, Emulator

class Mov(object):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2
    
    def __str__(self):
        return 'mov', str(self.reg1), ',', str(self.reg2)

class Add(object):
    def __init__(self, reg1, reg2):
        self.

class Add(object):
    pass

class Assembler():

    def __init__(self, code):
        self.asm = []
        self.extern = []
        self.data = []
        self.text = []
        self.code = code
        self.strCnt = 0
        self.arrCnt = 0 
        self.asm_comp = {'==': 'je', '!=': 'jne', '<': 'jlt', '>': 'jgt', '<=': 'jle', '>=': 'jge'}

    def newStrId(self):
        return 'str' + str(self.strCnt)

    def newArrId(self):
        return 'arr' + str(self.arrCnt)

    def generate(self):
        str_num = 1
        arr_num = 1        

        for node in code:
            if isinstance(node, ThreeAdrCode.Assign) and node.First().type == 'str':
                
                self.data.append('')

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
            #self.execute(inst)
        #for data in self.data:
        #    print data
        #for data in self.asm:
        #    print data
            
    

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

    def gen_push(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'push ' + reg
        self.addCode(line)

    def gen_pop(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'pop ' + reg
        self.addCode(line)

    def gen_goto(self, inst):
        label = self.getName(inst.getVar())
        line = 'jmp ' + label
        self.addCode(line)

    def gen_return(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'mov ' + reg + 'eax'
        self.addCode(line)
        line = 'pop ' + reg
        self.addCode(line)
        self.addCode('ret')

    def gen_end(self, inst):
        self.addCode('end')

    def gen_assign(self, inst):
        if inst.Second():
            #binary expression
            var = inst.getVar()  #self.getName(inst.getVar())
            first = inst.First()
            second = inst.Second()
            operator = inst.getOperator()      

        else:
            if inst.getOperator():
                #unary expression
            else:
                #var assignment

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

    def printCode(self):
        print ''
        print '---------------', 'Asembler', '---------------'

        for line in self.extern:
            print line
        print ''
        print 'segment .data'
        print ''
        for line in self.data:
            print line
        print ''
        print 'segment .text'
        print ''
        for line in self.text:
            print line
