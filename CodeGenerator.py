from itertools import chain
import Utils, AST, ThreeAdrCode

class Type(object):
    def __init__(self, type):
        self.type = type

    def getType(self):
        return self.type

    def isVar(self):
        return False

class Var(Type):
    def __init__(self, name, ref = False):
        super(Var, self).__init__('var')
        self.name = str(name)
        self.ref = ref

    def __str__(self):
        return ('&' if self.ref == True else "") + self.name

    def isInt(self):
        return self.name.isdigit()        

    def isVar(self):
        return not self.name.isdigit()

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
        self.name = "#rax"
    
    def __str__(self):
        return "#rax"

class CodeGenerator(Utils.ASTVisitor): 

    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.regCnt = 7 
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
        return 'L' + str( hex(self.label) )      

    def getNewFuncId(self):
        self.funcCnt += 1
        return str( hex(self.funcCnt) )

    def printCode(self):
        print ''
        print '---------------', 'Code Generator', '---------------'
        for line in self.code:
            if isinstance(line, ThreeAdrCode.Func):
                print ''
            print '>', self.code.index(line), line   
            if line.name == 'end':
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
        for node in reversed(params):
            var = self.vars[node]
            if isinstance(node, AST.VarExpr) and (node.decl.getType() == 'ArrDecl' or node.decl.ref == True):
                newVar = Var(var.name, True)
                self.addCode( ThreeAdrCode.Push('', [newVar] ) )
            else:
                self.addCode( ThreeAdrCode.Push('', [var] ) )     

    def check_CompilationUnit(self, node):
        Utils.ASTVisitor.check(self, node)
        self.combineCode()

    def check_FuncDecl(self, node):
        self.subProg += 1
        self.popCnt = 0
        startLabel = node.name + self.getNewFuncId()
        node.startLabel = startLabel
        endLabel = self.getNewLabel() 
        node.endLabel = endLabel    
        endLabel2 = self.getNewLabel()
        self.labels[node.name] = startLabel
        self.addCode( ThreeAdrCode.Goto('', endLabel2) )
        self.addCode( ThreeAdrCode.Func('', startLabel, []) )
        Utils.ASTVisitor.check(self, node)
        self.addCode( ThreeAdrCode.End(endLabel, []) )
        self.addCode( ThreeAdrCode.Void('', endLabel2, []) )
        self.subProg -= 1
    
    def check_ProcDecl(self, node):
        self.subProg += 1
        self.popCnt = 0
        if self.subProg == 1:
            startLabel = node.name
        else:
            startLabel = node.name + self.getNewFuncId()
        node.startLabel = startLabel
        endLabel = self.getNewLabel()
        node.endLabel = endLabel
        endLabel2 = self.getNewLabel()
        self.labels[node.name] = startLabel
        self.addCode( ThreeAdrCode.Goto('', endLabel2) )
        self.addCode( ThreeAdrCode.Func('', startLabel, []) )
        Utils.ASTVisitor.check(self, node)
        self.addCode( ThreeAdrCode.End(endLabel, []) )
        self.addCode( ThreeAdrCode.Void('', endLabel2, []) )
        self.subProg -= 1

    def check_VarDecl(self, node):
        var = Var(node.name)
        self.vars[ node ] = var

        if isinstance(node.parent, AST.FunParams):
            #We use the var name for the moment
            if node.ref == True:
                var = Var(node.name, True)
                self.vars[ node ] = var
                self.addCode( ThreeAdrCode.Param('', [var], self.popCnt) )
            else:
                self.addCode( ThreeAdrCode.Param('', [var], self.popCnt) )
            self.popCnt = self.popCnt + 1
            Utils.ASTVisitor.check(self, node)
        else:
            self.addCode( ThreeAdrCode.Decl('', [var]) )  
            Utils.ASTVisitor.check(self, node)
            expr = node.getExpr()
            if expr:
                label = self.getNewLabel()
                self.addCode( ThreeAdrCode.Assign('', [var, '=', Var(self.vars[expr]) ]) )

    def check_ArrDecl(self, node):
        Utils.ASTVisitor.check(self, node)
        var = node.name
        sizeExpr = self.vars[ node.getSizeExpr() ]
        arr = Arr(var, sizeExpr)
        self.vars[ node ] = arr
        self.addCode( ThreeAdrCode.Decl('', [arr]) )

    def check_IntExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        self.addCode( ThreeAdrCode.Assign('', [var, '=', Var(node.name) ]) )

    def check_CharExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        self.addCode( ThreeAdrCode.Assign('', [var, '=', Char(node.name) ]) )

    def check_StringExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = Var(self.getNewReg())
        self.vars[node] = var
        self.addCode( ThreeAdrCode.Assign('', [var, '=', String(node.name)]) )

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
        var = Var(self.getNewReg())
        self.vars[ node ] = var
        label = node.decl.startLabel
        self.addCode( ThreeAdrCode.Call('', label) )
        self.addCode( ThreeAdrCode.Pop('', len(node.getFunParams()) ) )
        self.addCode( ThreeAdrCode.Assign('', [var, '=', FuncReg()]) )
           
    def check_BinaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = self.vars[ node.getLeftExpr() ]
        var2 = self.vars[ node.getRightExpr() ]
        var3 = Var( self.getNewReg() )
        self.vars[ node ] = var3
        self.addCode( ThreeAdrCode.Assign('', self.flatten([var3, '=', var1, Operator(node.getOperator()), var2]) ) )

    def check_UnaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = Var(self.getNewReg())
        var2 = self.vars[ node.getExpr() ]
        self.vars[ node ] = var1
        self.addCode( ThreeAdrCode.Assign('', self.flatten([var1, '=', Operator(node.getOperator()), var2]) ) )

    def check_AssignStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = self.vars[ node.getLeftExpr() ]
        var2 = self.vars[ node.getRightExpr() ]
        self.addCode( ThreeAdrCode.Assign('', self.flatten([var1, '=', var2]) ) )

    def check_PrintStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        self.addCode( ThreeAdrCode.Print('', var) )

    def check_ReadStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        self.addCode( ThreeAdrCode.Read('', var) )
        
    def check_IncrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        self.vars[ node ] = var
        self.addCode( ThreeAdrCode.Assign('', self.flatten([var, '=', var, Operator('+'), Var('1')]) ))
 
    def check_DecrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        self.vars[ node ] = var
        self.addCode( ThreeAdrCode.Assign('', self.flatten([var, '=', var, Operator('-'), Var('1')]) ))
        
    def check_ReturnStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.vars[ node.getExpr() ]
        label = node.decl.endLabel
        self.addCode( ThreeAdrCode.Return('', [var]) )
        self.addCode( ThreeAdrCode.Goto('', label) )        
        
    def check_CallStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        self.pushCallParams(node.getFunParams() )
        var = self.getNewReg()
        jump = self.labels[node.name]
        self.addCode( ThreeAdrCode.Call('', jump) )
        self.addCode( ThreeAdrCode.Pop('', len(node.getFunParams()) ) )

    def handleConditional(self, node, startLabel, endLabel, rev = False):
        stack = []
        onot = {'!=': '==', '<': '>=', '>': '<=', '>=': '<', '<=': '>', '==': '!=', '||': '&&', '&&': '||'}
        
    
        def preCompute(node):
            if isinstance(node, AST.BinaryExpr) and node.isBoolean(node.getOperator()):
                preCompute(node.getLeftExpr())
                node.firstIfChild = preCompute(node.getRightExpr()) 
                node.operator = (node.operator if rev == False else onot[node.operator])
                return node.firstIfChild
            else:
                node.ifLabel = self.getNewLabel()
                node.operator = (node.operator if rev == False else onot[node.operator])
                return node
        
        def getNextLabel(node, stack, operator):
            prev = node
            for parent in reversed(stack):
                if parent.getOperator() == operator and parent.getLeftExpr() == prev:
                    return parent.firstIfChild.ifLabel
                prev = parent
            return (endLabel if operator == '||' else startLabel)

        def computeJumps(node):
            if isinstance(node, AST.BinaryExpr) and node.isBoolean(node.getOperator()):
                stack.append(node)
                computeJumps( node.getLeftExpr() )
                computeJumps( node.getRightExpr() )
                stack.pop()
            else:
                operator = node.getOperator()
                self.visit( node.getLeftExpr() )
                self.visit( node.getRightExpr() )
                left = self.vars[ node.getLeftExpr() ]
                right = self.vars[ node.getRightExpr() ]

                if not isinstance(node.parent, AST.BinaryExpr) or node.parent.getOperator() == '&&':
                    label = getNextLabel(node, stack, '||')
                    self.addCode( ThreeAdrCode.If(node.ifLabel, [left, onot[operator], right, 'goto', label]) )
                else:
                    label = getNextLabel(node, stack, '&&')
                    self.addCode( ThreeAdrCode.If(node.ifLabel, [left, operator, right, 'goto', label]) )

        preCompute(node)
        computeJumps(node)
        

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
                firstCond = False

                label = self.getNewLabel()
                nextLabel = self.getNewLabel()
                jumpLabel = None
                if node.isLastCond(stmt):
                    if node.hasElse():
                        jumpLabel = elseLabel
                    else:
                        jumpLabel = endLabel
                else:
                    jumpLabel = nextLabel

                startLabel = self.getNewLabel()
                self.handleConditional(stmt, startLabel, jumpLabel)
                self.addCode( ThreeAdrCode.Void('', startLabel, []) )
               
        self.addCode( ThreeAdrCode.Void('', endLabel, []) )

    def check_LoopStatement(self, node):
        beginLabel = self.getNewLabel()
        startLabel = self.getNewLabel()
        endLabel = self.getNewLabel()
        condition = node.getExpr() 
        body = node.getCompoundStatement()

        self.addCode( ThreeAdrCode.Void('', beginLabel, []) )
        self.handleConditional(condition, startLabel, endLabel, True)
        self.addCode( ThreeAdrCode.Void('', startLabel, []) )
        # visit loop body
        self.visit(body)
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Goto(label, beginLabel) )
        self.addCode( ThreeAdrCode.Void('', endLabel, []) )

    def flatten(self, param):
        res = []   
        for var in param:
            res.extend(var if isinstance(var, list) else [var])
        return res
        
    def combineCode(self):
        for line in self.globalCode:
            self.code.append(line)            

        self.code.append( ThreeAdrCode.Goto('', 'hatta') ) 
        for line in self.stackCode:
            self.code.append(line)
