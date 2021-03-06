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
        self.strs = {}
        self.types = {}
        self.strCnt = 0
        self.arrCnt = 0 
        self.asm_comp = {'==': 'je', '!=': 'jne', '<': 'jl', '>': 'jg', '<=': 'jle', '>=': 'jge'}
        self.regs = set(['rax','rbx','rcx','rdx','r8','r9','r10','r11','r12','r13','r14','r15','r16'])
        self.text.append('main:')
        self.extern.append('global main')
        self.extern.append('extern print_int')
        self.extern.append('extern print_str')
        self.extern.append('extern print_char')
        self.extern.append('extern read_int')
        self.extern.append('extern read_char')
        self.totalRegs = 7

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
                self.strs[node.First().name] = name
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
        if arr.name in self.arrs:
            name = self.arrs[arr.name]
        else:
            name = arr.name        

        index = arr.index.name
        self.addCode('mov ' + reg + ', ' + name)
        self.addCode('mov ' + reg + ', [' + reg + '+8*' + index + ']') 

    def putArr(self, arr, temp, reg):
        if arr.name in self.arrs:
            name = self.arrs[arr.name]
        else:
            name = arr.name
        index = arr.index.name
        self.addCode('mov ' + temp + ', ' + name)
        self.addCode('mov ' + '[' + temp + '+8*' + index + '], ' + reg)

    def addCode(self, line):
        self.text.append(line)

    def gen_default(self, inst):
        pass

    def saveAll(self, used = []):
        for x in xrange(8, 9 + self.totalRegs):
            reg = 'r' + str(x)
            if not reg in used:
                self.addCode( Inst.Push(reg) )
        
    def loadAll(self, used = []):
        for x in reversed( xrange(8, 9 + self.totalRegs) ):
            reg = 'r' + str(x)
            if not reg in used:
                self.addCode( Inst.Pop(reg) )

    def gen_Void(self, inst):
        self.addCode(inst.label + ':')

    def gen_Func(self, inst):
        self.addCode('')
        self.addCode(inst.label + ':')
        self.addCode( Inst.Push('rbp') )
        self.addCode( Inst.Mov('rbp', 'rsp') )
        self.saveAll()

    def gen_Push(self, inst):
        #TO DO: after constant propagation
        var = inst.getVar()
        if var.Btype == 'ArrDecl':
            self.addCode( Inst.Mov('rax', self.arrs[ var.name ]) )
            name = 'rax'
        else:
            name = var.name
        self.addCode( Inst.Push(name) )

    def gen_Param(self, inst):
        var = inst.getVar()
        pos = inst.getPos()
        if var.ref == True:
            pass
            #TO DO:
        else:
            self.addCode('mov ' + var.name + ', [rbp+' + str(8 * pos + 16) + ']')

    def gen_Pop(self, inst):
        cnt = inst.getNo()
        self.addCode('add rsp, ' + str(8 * cnt) )

    def gen_Call(self, inst):
        label = inst.getJump()
        self.addCode( Inst.Jump(label, 'call') ) 

    def gen_Goto(self, inst):
        label = inst.getJump()
        self.addCode( Inst.Jump(label) )

    def gen_Return(self, inst):
        var = inst.getVar()
        self.addCode( Inst.Mov('rax', var.name) )

    def gen_End(self, inst):
        self.addCode(inst.label + ':')
        self.loadAll()
        self.addCode( Inst.Pop('rbp') )
        self.addCode('ret')

    def SAFE_NAME(self, var):
        if var in self.regs:
            return var
        #print 'Warning: unsed code detected!'
        return 'rax' 

    def gen_Assign(self, inst):
        if inst.Second():
            #binary expression
            var = inst.getVar() 
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
                self.addCode( Inst.Mov( self.SAFE_NAME(var.name), result) )
                self.types[var.name] = 'int'

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
                    self.addCode( Inst.Mov( self.SAFE_NAME(var.name), result) )
                    self.types[var.name] = 'int'
                pass
            else:
                #var assignment
                var = inst.getVar()
                first = inst.First()
                typex = 'int'
            
                # change name of default return reg
                if first.name == '#rax':
                    first.name = 'rax'
                reg = first.name

                if first.type == 'var' and first.name in self.types:
                    typex = self.types[first.name]
                elif first.type == 'arr':
                    reg = 'rbx'
                    self.getArr(first, reg)
                elif first.type == 'char':
                    reg = hex( ord(first.name) )
                    typex = 'char'
                elif first.type == 'string':
                    typex = 'string'
                if var.type == 'arr':
                    self.putArr(var, 'rax', reg)
                else:
                    self.addCode( Inst.Mov( self.SAFE_NAME(var.name), reg) )
                    self.types[var.name] = typex

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
        left = inst.First()
        operator = inst.getOperator()
        right = inst.Second()
        label = inst.getJump()
        
        #TO DO after constant propagation
        self.addCode( Inst.Cmp(left.name, right.name) )
        self.addCode( Inst.Jump(label, self.asm_comp[operator]) ) 

    def gen_Print(self, inst):
        self.saveAll()

        var = inst.getVar()
        if var.type == 'arr':
            self.getArr(var, 'rdi')
            self.addCode('call print_int')
        elif var.type == 'char' or var.Btype == 'CharType':
            self.addCode( Inst.Mov('rdi', var.name) )
            self.addCode('call print_char') 
        elif var.Btype == 'StringType':
            label = (self.strs[var.name] if var.name in self.strs else var.name)
            self.addCode( Inst.Mov('rdi', label ) )
            self.addCode('call print_str')       
        else:
            self.addCode( Inst.Mov('rdi', var.name) )
            if var.name in self.types and self.types[var.name] == 'string':
                self.addCode('call print_str')
            elif var.name in self.types and self.types[var.name] == 'char':
                self.addCode('call print_char')
            else:
                self.addCode('call print_int')

        self.loadAll()

    def gen_Read(self, inst):
        var = inst.getVar()

        if var.type == 'char' or var.Btype == 'CharType':
            self.saveAll([var.name])
            self.addCode('call read_char')
            self.addCode( Inst.Mov(var.name, 'rax') )
            self.loadAll([var.name])
        elif var.type == 'arr':
            self.saveAll([var.name])
            self.addCode('call read_int')
            self.putArr(var, 'rbx', 'rax')
            self.loadAll()
        else:
            self.saveAll([var.name])
            self.addCode('call read_int')
            self.addCode( Inst.Mov(var.name, 'rax') )
            self.types[var.name] = 'int'
            self.loadAll([var.name])

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


