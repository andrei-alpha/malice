import ThreeAdrCode, Emulator
import ASMInst as Inst

class Assembler():

    def __init__(self, code):
        self.asm = []
        self.extern = []
        self.data = []
        self.text = []
        self.code = code
        self.arrs = {}
        self.types = {}
        self.strCnt = 0
        self.arrCnt = 0 
        self.asm_comp = {'==': 'je', '!=': 'jne', '<': 'jlt', '>': 'jgt', '<=': 'jle', '>=': 'jge'}

        self.text.append('main:')
        self.extern.append('global main')
        self.extern.append('extern print_int')
        self.extern.append('extern print_str')
        self.extern.append('extern print_char')
        self.extern.append('extern read_int')
        self.extern.append('extern read_char')

    def newStrId(self):
        self.strCnt += 1
        return 'str' + str(self.strCnt)

    def newArrId(self):
        self.arrCnt += 1
        return 'arr' + str(self.arrCnt)

    def generate(self):
        str_num = 1
        arr_num = 1        

        for node in self.code:
            if isinstance(node, ThreeAdrCode.Assign) and node.First().type == 'string':
                name = self.newStrId()
                self.data.append( Inst.StrDecl(name, node.First().name) )
                node.First().name = name
            if isinstance(node, ThreeAdrCode.Decl) and node.getVar().type == 'arr':
                name = self.newArrId()
                self.data.append( Inst.ArrDecl(name, node.getVar().index) )
                self.arrs[node.getVar().name] = name
                
        for inst in self.code:
            methname = 'gen_%s' % inst.__class__.__name__
            method = getattr(self, methname, self.gen_default)
            method(inst)  
    

    def getName(self, reg):
        return str(reg)

    def getValue(self, var):
        if isinstance(var, int) or (isinstance(var, str) and var.isdigit()):
            return int(var)
        else:
            return var

    def getArr(self, arr, reg):
        name = self.arrs[arr.name]
        index = arr.index.name
        self.addCode('mov ' + reg + ', ' + name)
        self.addCode('mov ' + reg + ', [' + reg + '+8*' + index + ']') 

    def putArr(self, arr, temp, reg):
        name = self.arrs[arr.name]
        index = arr.index.name
        self.addCode('mov ' + temp + ', ' + name)
        self.addCode('mov ' + '[' + reg + '+8*' + index + '], ' + temp)

    def addCode(self, line):
        self.text.append(line)

    def gen_default(self, inst):
        pass

    def gen_Void(self, inst):
        self.addCode(inst.label + ':')

    def gen_Func(self, inst):
        self.addCode('')
        self.addCode(inst.label + ':')

    def gen_Push(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'push ' + reg
        #self.addCode(line)

    def gen_Pop(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'pop ' + reg
        #self.addCode(line)

    def gen_Goto(self, inst):
        label = self.getName(inst.getVar())
        line = 'jmp ' + label
        #self.addCode(line)

    def gen_Return(self, inst):
        reg = self.getName(inst.getVarName())
        line = 'mov ' + reg + 'eax'
        self.addCode(line)
        line = 'pop ' + reg
        self.addCode(line)
        self.addCode('ret')

    def gen_End(self, inst):
        self.addCode('ret')

    def gen_Assign(self, inst):
        if inst.Second():
            #binary expression
            var = inst.getVar()  #self.getName(inst.getVar())
            first = inst.First()
            second = inst.Second()
            operator = inst.getOperator().oper     
            reg1 = first.name
            reg2 = second.name
            if first.type == 'arr':
                reg1 = 'rax'
                self.getArr(first, reg1)
            if second.type == 'arr':
                reg2 = 'rbx'
                self.getArr(second, reg2)

            result = self.computeBinary(reg1, reg2, operator)
            if var.type == 'arr':
                self.putArr(var, 'rbx', result)
            else:
                self.addCode( Inst.Mov(var.name, result) )

        else:
            if inst.getOperator():
                #unary expression
                operator = inst.getOperator().oper
                var = inst.getVar()
                first = inst.First()
                reg = first.name
                if first.type == 'arr':
                    reg = 'rbx'
                    self.getArr(first, reg)
                
                result = self.computeUnary(reg, operator)
                if var.type == 'arr':
                    self.putArr(var, 'rax', result)
                else:
                    self.addCode( Inst.Mov(var.name, result) )
                pass
            else:
                #var assignment
                var = inst.getVar()
                first = inst.First()
                reg = first.name
                if first.type == 'arr':
                    reg = 'rbx'
                    self.getArr(first, reg)
                if var.type == 'arr':
                    self.putArr(var, 'rax', reg)
                else:
                    self.addCode( Inst.Mov(var.name, reg) )

    def computeBinary(self, left, right, operator):
        #result in rax
        if operator == '+':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Add('rax', right) )
        elif operator == '-':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Sub('rax', right) )
        elif operator == '*':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Imul('rax', right) )
        elif operator == '/':
            self.addCode( Inst.Idiv(left, right) )
        elif operator == '%':
            self.addCode( Inst.Idiv(left, right) )
            return 'rdx'
        elif operator == '|':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Or('rax', right) )
        elif operator == '^':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Xor('rax', right) )
        elif operator == '&':
            self.addCode( Inst.Mov('rax', left) )
            self.addCode( Inst.Add('rax', right) )

        return 'rax'

    def computeUnary(self, var, operator):
        self.addCode( Inst.Mov('rax', var) )
        if operator == '!':
            self.addCode( Inst.Not('rax') )
        elif operator == '-':
            self.addCode( Inst.Imul('rax', '-1') )
        elif operator == '~':
            self.addCode( Inst.Neg('rax') )
        
        return 'rax'

    def gen_If(self, inst):
        left = self.getName(inst.First())
        op = inst.getOperator()
        right = self.getName(inst.Second())
        jump = inst.getJump()
        #self.addCode('cmp ' + left + right)
        #self.addCode(self.asm_comp[op] + ' ' + jump) 

    def gen_Print(self, inst):
        var = inst.getVar()
        if var.type == 'arr':
            self.getArr(var, 'rdi')
            self.addCode('call print_int')
        else:
            self.addCode( Inst.Mov('rdi', var.name) )
            if var.name in self.types and self.types[var.name] == 'string':
                self.addCode('call print_str')
            if var.name in self.types and self.types[var.name] == 'char':
                self.addCode('call print_char')
            else:
                self.addCode('call print_int')

    def gen_Read(self, inst):
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

    def writeToFile(self, filename):
        stdout = open(filename, 'w')
        
        for line in self.extern:
            stdout.write(str(line) + '\n')
        stdout.write('\n')
        stdout.write('segment .data\n')
        stdout.write('\n')
        for line in self.data:
            stdout.write(str(line) + '\n')
        stdout.write('\n')
        stdout.write('segment .text\n')
        stdout.write('\n')
        for line in self.text:
            stdout.write(str(line) + '\n')

