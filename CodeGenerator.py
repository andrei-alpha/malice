from itertools import chain
import Utils, AST

class CodeNode:
    def __init__(self, name, label, children):
        self.name = name
        self.label = label
        self.children = children

    def __str__(self):
        s = ''
                
        if not self.label == '':
            s += str(self.label) + ': '
        if not self.name == 'assign':
            s += self.name + ' '
        for child in self.children:
            s += str(child) + ' '
    
        return s

class ThreeAdrCode(object):
    def __init__(self):
        pass
        
    @staticmethod
    def Push(label, children):
        return CodeNode('push', label, children)

    @staticmethod
    def Pop(label, children):
        return CodeNode('pop', label, children)

    @staticmethod
    def Goto(label, jump):
        return CodeNode('goto', label, [jump])
 
    @staticmethod
    def Return(label, children):
        return CodeNode('return', label, children)

    @staticmethod
    def End(label, children):
        return CodeNode('end', label, [])

    @staticmethod
    def Assign(label, children):
        return CodeNode('assign', label, children)

    @staticmethod
    def Print(label ,var):
        return CodeNode('print', label, [var])

    @staticmethod
    def Read(label, var):
        return CodeNode('read', label, [var])

    @staticmethod
    def Call(label, name):
        return CodeNode('call', label, [name])

    @staticmethod
    def IfTrue(label, children):
        return CodeNode('ifTrue', label, children)

    @staticmethod
    def Decl(label, children):
        return CodeNode('decl', label, children)

    @staticmethod
    def IfFalse(label, children):
        return CodeNode('ifFalse', label, children)

    @staticmethod
    def Void(name, label, children):
        return CodeNode(name, label, children)

class CodeGenerator(Utils.ASTVisitor): 

    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.regCnt = 0 
        self.label = 0
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

    def printCode(self):
        print ''
        print '---------------', 'Code Generator', '---------------'
        for line in self.code:
            if line.label == '':
                print ''
            print line   
            if line.label == '' or line.name == 'end':
                print '' 
        print ''

    def addCode(self, node):
        if self.subProg == 0:
            self.globalCode.append(node)
        else:
            self.stackCode.append(node)

    def pushCallParams(self, params):
        for node in params:
            label = self.getNewLabel()
            if isinstance(node, AST.VarExpr) and (node.decl.getType() == 'ArrDecl' or node.decl.ref == True):
                self.addCode( ThreeAdrCode.Push(label, ['&', self.vars[node] ]) )
            else:
                self.addCode( ThreeAdrCode.Push(label, [ self.vars[node] ]) )     

    def check_CompilationUnit(self, node):
        Utils.ASTVisitor.check(self, node)
        self.combineCode()

    def check_FuncDecl(self, node):
        self.subProg += 1
        label = node.name
        self.labels[node.name] = label
        self.addCode( ThreeAdrCode.Void('', label, []) )   
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.End(label, []) )
        self.subProg -= 1
    
    def check_ProcDecl(self, node):
        self.subProg += 1
        label = node.name
        self.labels[node.name] = label
        self.addCode( ThreeAdrCode.Void('', label, []) )
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.End(label, []) )
        self.subProg -= 1

    def check_VarDecl(self, node):
        var = node.name
        self.vars[ node ] = var
        label = self.getNewLabel()

        if isinstance(node.parent, AST.FunParams):
            #We use the var name for the moment
            # var = self.getNewReg()
            if node.ref == True:
                self.addCode( ThreeAdrCode.Pop(label, ['&', var]) )
            else:
                self.addCode( ThreeAdrCode.Pop(label, [var]) )
            Utils.ASTVisitor.check(self, node)
        else:
            self.addCode( ThreeAdrCode.Decl(label, [var]) )  
            Utils.ASTVisitor.check(self, node)
            expr = node.getExpr()
            if expr:
                label = self.getNewLabel()
                self.addCode( ThreeAdrCode.Assign(label, [var, '=', self.vars[expr] ]) )

    def check_ArrDecl(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = node.name
        self.vars[ node ] = var
        sizeExpr = self.vars[ node.getSizeExpr() ]
        self.addCode( ThreeAdrCode.Decl(label, [var, '[', sizeExpr, ']']) )

    def check_IntExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.getNewReg()
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', node.name ]) )

    def check_CharExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.getNewReg()
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', '"' + node.name + '"']) )

    def check_StringExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var = self.getNewReg()
        self.vars[node] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', '"' + node.name + '"']) )

    def check_VarExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.vars[node] = node.name

    def check_ArrExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        indexExpr = self.vars[ node.getExpr() ]
        self.vars[node] = [node.name, '[', indexExpr, ']']
    
    def check_CallExpr(self, node):
        #TO DO:
        Utils.ASTVisitor.check(self, node)
        self.pushCallParams(node.getFunParams() )
        var = self.getNewReg()
        self.vars[ node ] = var
        label = self.getNewLabel()
        self.addCode( ThreeAdrCode.Assign(label, [var, '=', 'call', node.name]) )
           
    def check_BinaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        var1 = self.vars[ node.getLeftExpr() ]
        var2 = self.vars[ node.getRightExpr() ]
        label = self.getNewLabel()
        var3 = self.getNewReg()
        self.vars[ node ] = var3
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var3, '=', var1, node.getOperator(), var2]) ) )

    def check_UnaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var1 = self.getNewReg()
        var2 = self.vars[ node.getExpr() ]
        self.vars[ node ] = var1
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var1, '=', node.getOperator(), var2]) ) )

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
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var, '=', var, '+', '1']) ))
 
    def check_DecrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        label = self.getNewLabel()
        var = self.vars[ node.getExpr() ]
        self.vars[ node ] = var
        self.addCode( ThreeAdrCode.Assign(label, self.flatten([var, '=', var, '-', '1']) ))
        
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
            self.code.append( ThreeAdrCode.Void('.global', '', []) )
        for line in self.globalCode:
            self.code.append(line)            

        self.code.append( ThreeAdrCode.Void('.stack', '', []) )
        for line in self.stackCode:
            self.code.append(line)
