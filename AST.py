def setName(self, nodeType):
    if nodeType == '':
        return self.__class__.__name__
    return nodeType

# This is the constructor
class ASTNode(object):
    def __init__(self, nodeType, children, line, lexpos):
        self.nodeType = nodeType            
        self.line     = line
        self.lexpos   = lexpos
        self.children = children
    
    def setSymbolTable(table):
        self.table = table

    def getSymbolTable(table):
        return table

    def __repr__(self):
        return "ASTNode(%r, %r)" % (self.nodeType, self.children)

    def getType(self):
        return self.nodeType

class CompilationUnit(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(CompilationUnit, self).__init__(nodeType, children, line, lexpos)
    
    def getDecls(self):
        return self.children[0]

class Decls(ASTNode):
    def __init__(self, children, line, lexpos, name='', nodeType=''):
        nodeType = setName(self, nodeType)
        self.name = name
        super(Decls, self).__init__(nodeType, children, line, lexpos)

    def getID():
        return self.name

class Body(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(Body, self).__init__(nodeType, children, line, lexpos)

    def getDecls(self):
        return self.children[0]

    def getStatement(self):
        return self.children[1]

class VarDecl(Decls):
    def __init__(self, children, line, lexpos, name, ref=False):
        self.ref = ref
        super(VarDecl, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getBaseType(self):
        return self.children[0]

    def getType(self):
        return self.children[0].nodeType

    def getExpr(self):
        if len(self.children) == 2:
            return self.children[1]
        return None

class ArrDecl(Decls):
    def __init__(self, children, line, lexpos, name):
        super(ArrDecl, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getSizeExpr(self):
        return self.children[0]

    def getBaseType(self):
        return self.children[1]

class FuncDecl(Decls):
    def __init__(self, children, line, lexpos, name):
        super(FuncDecl, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getReturnType(self):
        return self.children[1]

    def getFunParams(self):
        return self.children[0].children

class ProcDecl(Decls):
    def __init__(self, children, line, lexpos, name):
        super(ProcDecl, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getFunParams(self):
        return self.children[0].children

    def getBody(self):
        return self.children[1]

class FunParams(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(FunParams, self).__init__(nodeType, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class CallParams(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(CallParams, self).__init__(nodeType, children, line, lexpos)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]


class CompoundStatement(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(CompoundStatement, self).__init__(nodeType, children, line, lexpos)

    def getStatement(self):    
        return self.children[0]

    def getStatementList(self):
        return self.children[1]        

#Statements

class PrintStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(PrintStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class ReadStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(ReadStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class NullStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(NullStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

class AssignStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(AssignStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]

class IncrementStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(IncrementStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class DecrementStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(DecrementStatement, self).__init__(children, line, lexpos, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class ReturnStatement(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(ReturnStatement, self).__init__(nodeType, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class CallStatement(Decls):
    def __init__(self, children, line, lexpos, name):
        super(CallStatement, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getFunParams(self):
        return self.children[0].children

    def NumberOfFunParams(self):
        return len(self.children[0].children)

class LoopStatement(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(LoopStatement, self).__init__(nodeType, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

    def getCompoundStatement(self):
        return self.children[1]

class IfStatement(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(IfStatement, self).__init__(nodeType, children, line, lexpos)

    def hasElse(self):
        return len(self.children) % 2 == 1

    def isElseBody(self, child):
        index = self.children.index(child)
        return self.hasElse() and index == len(self.children) - 1        
    
    def isLastCond(self, child):
        index = self.children.index(child)
        return index == len(self.children) - 2 or index == len(self.children) - 3 

    def getExpr(self):
        return self.children[0]

    def getStatement1(self):
        return self.children[1]

    def getStatement2(self):
        return self.children[2] 

class Operator(ASTNode):
    def __init__(self, children, line, lexpos, operator, nodeType=''):
        nodeType = setName(self, nodeType)
        super(Operator, self).__init__(nodeType, children, line, lexpos)
        self.operator = operator

    def getOperator(self):
        return self.operator

class UnaryExpr(Operator):
    def __init__(self, children, line, lexpos, operator):
        super(UnaryExpr, self).__init__(children, line, lexpos, operator, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class BinaryExpr(Operator):
    def __init__(self, children, line, lexpos, operator):
        super(BinaryExpr, self).__init__(children, line, lexpos, operator, self.__class__.__name__)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]

    def isBoolean(self, operator):
        return operator == '&&' or operator == '||'

    def isRelational(self, operator):
        return operator == '!=' or operator == '<' or operator == '>' or operator == '<=' or operator == '>=' or operator == '=='

class ArrExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(ArrExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getExpr(self):
        return self.children[0]

class CallExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(CallExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)

    def getFunParams(self):
        return self.children[0].children

class VarExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(VarExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)

class IntExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(IntExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)
    
    def getValue(self):
        return self.name

class CharExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(CharExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)
 
    def getValue(self):
        return self.name

class StringExpr(Decls):
    def __init__(self, children, line, lexpos, name):
        super(StringExpr, self).__init__(children, line, lexpos, name, self.__class__.__name__)
    
    def getValue(self):
        return self.name

class Factor(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(Factor, self).__init__(nodeType, children, line, lexpos)

    def getFactor(self):
        return self.nodeType

    def getVal(self):
        return self.children[0]

class Number(Factor):
    def __init__(self, children, line, lexpos):
        super(Number, self).__init__(children, line, lexpos, self.__class__.__name__)

class Id(Factor):
    def __init__(self, children, line, lexpos):
        super(Id, self).__init__(children, line, lexpos, self.__class__.__name__)

class Letter(Factor):
    def __init__(self, children, line, lexpos):
        super(Letter, self).__init__(children, line, lexpos, self.__class__.__name__)

class IntType(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(IntType, self).__init__(nodeType, children, line, lexpos)

class CharType(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(CharType, self).__init__(nodeType, children, line, lexpos)

class StringType(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        nodeType = setName(self, nodeType)
        super(StringType, self).__init__(nodeType, children, line, lexpos)

class BooleanType(ASTNode):
    def __init__(self, children, line, lexpos, nodeType=''):
        node = setName(self, nodeType)
        super(StringType, self).__init__(nodeType, children, line, lexpos)
