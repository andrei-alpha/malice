from itertools import chain
import Utils, AST, ThreeAdrCode

class Type(object):
    def __init__(self, type):
        self.type = type

    def getType(self):
        return self.type

class Var(Type):
    def __init__(self, name, ref = False):
        super(Var, self).__init__('var')
        self.name = str(name)
        self.ref = ref

    def __str__(self):
        return ('&' if self.ref == True else "") + self.name

    def isInt(self):
        return self.isdigit()        

    def isVar(self):
        return not self.isdigit()

class Arr(Type):
    def __init__(self, name, index):
        super(Arr, self).__init__('arr')
        self.name = name
        self.index = index

    def __str__(self):
        return self.name + "[" + self.index.name + "]"

class Char(Type):
    def __init__(self, name):
        super(Char, self).__init__('char')
        self.name = name

    def __str__(self):
        return "'" + self.name + "'"

class String(Type):
    def __init__(self, name):
        super(String, self).__init__('string')
        self.name = name

    def __str__(self):
        return '"' + self.name + '"'

class Func(Type):
    def __init__(self, name):
        super(Func, self).__init__('func')
        self.name = name

    def __str__(self):
        return "call " + self.name + "()"

class Operator(Type):
    def __init__(self, oper):
        super(Operator, self).__init__('operator')
        self.oper = oper

    def __str__(self):
        return self.oper

class FuncReg(Type):  
    def __init__(self):
        super(FuncReg, self).__init__('funcreg')
    
    def __str__(self):
        return "#eax"

class CodeGenerator(Utils.ASTVisitor): 

    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.regCnt = 0 
        self.label = 0
        self.funcCnt = 0
        self.subProg = 0
        self.labels = {}
        self.globalCode = []
        self.stackCode = []
        self.vars = {}

    def getNewReg(self):
        reg = "$R"
        self.regCnt = self.regCnt + 1
        return reg + str(self.regCnt)

    def getNewLabel(self):
        self.label = self.label + 1
        return str( hex(self.label) )      

    def getNewFuncId(self):
        self.funcCnt += 1
        return ''
        return str(self.funcCnt)

    def printCode(self):
        print ''
        print '---------------', 'Code Generator', '---------------'
        for line in self.code:
            if line.label == '':
                print ''
            print '>', self.code.index(line), line   
            if line.label == '' or line.name == 'end':
                print '' 
        print ''

    def getCode(self):
        return self.code

    def addCode(self, node):
        if self.subProg == 0:
            self.globalCode.append(node)
        else:
            self.stackCode.append(node)

    def pushCallParams(self, params):
        for node in params:
            label = self.getNewLabel()
            if isinstance(node, AST.VarExpr) and (node.decl.getType() == 'ArrDecl' or node.decl.ref == True):
                self.addCode( ThreeAdrCode.Push(label, [self.vars[node]] ) )
            else:
                self.addCode( ThreeAdrCode.Push(label, [self.vars[node]] ) )     

    def check_CompilationUnit(self, node):
        Utils.ASTVisitor.check(self, node)
        self.combineCode()

    def check_FuncDecl(self, node):
        self.subProg += 1
        startLabel = node.name + self.getNewFuncId()
        endLabel = self.getNewLabel() 
        self.labels[node.name] = startLabel
        self.addCode( ThreeAdrCode.Goto('', endLabel) )
        self.addCode( ThreeAdrCode.Func('', startLabel, []) )
        Utils.ASTVisitor.check(self, node)
        self.addCode( ThreeAdrCode.End(endLabel, []) )
        self.subProg -= 1
    
    def check_ProcDecl(self, node):
        self.subProg += 1
        if self.subProg == 1:
            startLabel = node.name
        else:
            startLabel = node.name + self.getNewFuncId()
        endLabel = self.getNewLabel()
        self.labels[node.name] = startLabel
        self.addCode( ThreeAdrCode.Goto('', endLabel) )
        self.addCode( ThreeAdrCode.Func('', startLabel, []) )
        Utils.ASTVisitor.check(self, node)
        self.addCode( ThreeAdrCode.End(endLabel, []) )
        self.subProg -= 1

    def check_VarDecl(self, node):
        var = Var(node.name)
        self.vars[ node ] = var
        label = self.getNewLabel()

        if isinstance(node.parent, AST.FunParams):
            #We use the var name for the moment
            # var = self.getNewReg()
            if node.ref == True:
                var = Var(node.name, True)
                self.vars[ node ] = var
                self.addCode( ThreeAdrCode.Pop(label, [var] ) )
            else:
                self.addCode( ThreeAdrCode.Pop(label, [var]) )
            Utils.ASTVisitor.check(self, node)
        else:
            self.addCode( ThreeAdrCode.Decl(label, [var]) )  
            Utils.ASTVisitor.check(self, node)
            expr = node.getExpr()
            if expr:
                label = self.getNewLabel()
                self.addCode( ThreeAdrCode.Assign(label, [var, '=', Var(self.vars[expr]) ]) )

    def check_ArrDecl(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = node.name
        sizeExpr = self.vars[ node.getSizeExpr() ]
        arr = Arr(var, sizeExpr)
        self.vars[ node ] = arr
        self.addCode( ThreeAdrCode.Decl(label, [arr]) )

    def check_IntExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', Var(node.name) ]) )

    def check_CharExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', Char(node.name) ]) )

    def check_StringExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', String(node.name)]) )

    def check_VarExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.vars[node] = Var(node.name)

    def check_ArrExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        indexExpr = self.vars[ node.getExpr() ]
        self.vars[node] = Arr(node.name, indexExpr)
    
    def check_CallExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.pushCallParams(node.getFunParams() )
        var = self.getNewReg()
        self.vars[ node ] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Call(label, node.name) )
        lalbel = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [Var(var), '=', FuncReg()]) )
           
    def check_BinaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = self.vars[ node.getLeftExpr() ]
        var2 = self.vars[ node.getRightExpr() ]
        label = self.getNewLabel()
        var3 = Var( self.getNewReg() )
        self.vars[ node ] = var3
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var3, '=', var1, Operator(node.getOperator()), var2]) ) )

    def check_UnaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var1 = Var(self.getNewReg())
        var2 = self.vars[ node.getExpr() ]
        self.vars[ node ] = var1
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var1, '=', Operator(node.getOperator()), var2]) ) )

    def check_AssignStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = self.vars[ node.getLeftExpr() ]
        label = self.getNewLabel()
        var2 = self.vars[ node.getRightExpr() ]
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var1, '=', var2]) ) )

    def check_PrintStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = self.vars[ node.getExpr() ]
        self.addCode( ThreeAdrCode.Print(label, var) )

    def check_ReadStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = self.vars[ node.getExpr() ]
        self.addCode( ThreeAdrCode.Read(label, var) )
        
    def check_IncrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = self.vars[ node.getExpr() ]
        self.vars[ node ] = var
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var, '=', var, Operator('+'), Var('1')]) ))
 
    def check_DecrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = self.vars[ node.getExpr() ]
        self.vars[ node ] = var
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var, '=', var, Operator('-'), Var('1')]) ))
        
    def check_ReturnStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Return(label, [var]) )

    def check_CallStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        self.pushCallParams(node.getFunParams() )
        var = self.getNewReg()
        jump = self.labels[node.name]
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Call(label, jump) )

    def check_IfStatement(self, node):
        endLabel = self.getNewLabel()
        nextLabel = self.getNewLabel()
        elseLabel = self.getNewLabel()
        firstCond = True

        for stmt in node.children:
            if isinstance(stmt, AST.CompoundStatement):
                if node.isElseBody(stmt):
                    self.addCode( ThreeAdrCode.Void('', elseLabel, []) )    
    
                self.visit(stmt)
                label = self.getNewLabel()
                self.addCode( ThreeAdrCode.Goto(label, endLabel) )
            else:
                if not firstCond:
                    self.addCode( ThreeAdrCode.Void('', nextLabel, []) )
                firstCont = False

                label = nextLabel
                nextLabel = self.getNewLabel()
                jumpLabel = None
                if node.isLastCond(stmt):
                    if node.hasElse():
                        jumpLabel = elseLabel
                    else:
                        jumpLabel = endLabel
                else:
                    jumpLabel = nextLabel
                
                self.visit(stmt)
                var = self.vars[stmt]
                self.addCode( ThreeAdrCode.IfFalse(label, self.flatten([var, 'goto', jumpLabel]) ) )

        self.addCode( ThreeAdrCode.Void('', endLabel, []) )

    def check_LoopStatement(self, node):
        start = self.getNewLabel()
        end = self.getNewLabel()
        #to do: bad function names here
        condition = node.getExpr() 
        body = node.getCompoundStatement()

        self.visit(condition)
        var = self.vars[ condition ]
        self.addCode( ThreeAdrCode.IfFalse(start, self.flatten([var, 'goto', end]) ))       
        self.visit(body)
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Goto(label, start) )
        self.addCode( ThreeAdrCode.Void('', end, []) )

    def flatten(self, param):
        res = []   
        for var in param:
            res.extend(var if isinstance(var, list) else [var])
        return res
        
    def combineCode(self):
        if len(self.globalCode) > 0:
            pass
            self.code.append( ThreeAdrCode.Void('.global', '', []) )
        for line in self.globalCode:
            self.code.append(line)            

        self.code.append( ThreeAdrCode.Void('.stack', '', []) )
        self.code.append( ThreeAdrCode.Goto('', 'hatta') ) 
        for line in self.stackCode:
            self.code.append(line)
