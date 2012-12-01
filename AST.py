COMPILATION_UNIT = "compilation_unit"
UNARY_OP         = "unary_op"
BINARY_OP        = "binary_op"
DECLARATION      = "declaration"
FACTOR           = "factor"
NUMBER           = "number"
ID               = "id"
LETTER           = "letter"
BODY             = "body"
FORMAL_PARAMS    = "formal_params"
MOKE             = "moke"

class ASTNode(object):
    def __init__(self, nodeType, children, line, lexpos):
        self.nodeType = nodeType            
        self.line     = line
        self.lexpos   = lexpos
        self.children = children
    
    def __repr__(self):
        return "ASTNode(%r, %r, %r, %r)" % (self.nodeType, self.line, self.lexpos, self.children)

    def getNodeType(self):
        return self.nodeType

class CompilationUnit(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CompilationUnit, self).__init__(COMPILATION_UNIT, children, line, lexpos)
    
    def getDecls(self):
        return self.children[0]

class Decls(ASTNode):
    def __init__(self, children, line, lexpos):
        super(Decls, self).__init__(DECLARATION, children, line, lexpos)

class Body(ASTNode):
    def __init__(self, children, line, lexpos):
        super(Body, self).__init__(BODY, children, line, lexpos)

    def getDecls(self):
        return self.children[0]

    def getStatement(self):
        return self.children[1]

class FormalParams(ASTNode):
    def __init__(self, children, line, lexpos):
        super(FormalParams, self).__init__(FORMAL_PARAMS, children, line, lexpos)


class VarDecl(ASTNode):
    def __init__(self, children, line, lexpos):
        super(VarDecl, self).__init__(DECLARATION, children, line, lexpos)

    def getType(self):
        return self.children[1]

class ArrDecl(ASTNode):
    def __init__(self, children, line, lexpos):
        super(ArrDecl, self).__init__(DECLARATION, children, line, lexpos)

    def getSizeExpr(self):
        return self.children[0]

    def getBaseType(self):
        return self.children[1]

class FuncDecl(Decls):
    def __init__(self, children, line, lexpos):
        super(FuncDecl, self).__init__(children, line, lexpos)

    def getFormalParams(self):
        return self.children[0]

    def getBody(self):
        return self.children[1]

class ProcDecl(Decls):
    def __init__(self, children, line, lexpos):
        super(ProcDecl, self).__init__(children, line, lexpos)

    def getFormalParams(self):
        return self.children[0]

    def getBody(self):
        return self.children[1]

class FunParams(ASTNode):
    def __init__(self, children, line, lexpos):
        super(FunParams, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class CallParams(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CallParams, self).__init__(MOKE, children, line, lexpos)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]


class CompoundStatement(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CompoundStatement, self).__init__(MOKE, children, line, lexpos)

    def getStatement(self):    
        return self.children[0]

    def getStatementList(self):
        return self.childre[1]        

#Statements

class PrintStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(PrintStatement, self).__init__(children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class ReadStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(ReadStatement, self).__init__(children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class NullStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(NullStatement, self).__init__(children, line, lexpos)

class AssignStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(AssignStatement, self).__init__(children, line, lexpos)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]

class IncrementStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(IncrementStatement, self).__init__(children, line, lexpos)

    def getExpr(self):
        return self.childre[0]

class DecrementStatement(CompoundStatement):
    def __init__(self, children, line, lexpos):
        super(DecrementStatement, self).__init__(children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class ReturnStatement(ASTNode):
    def __init__(self, children, line, lexpos):
        super(ReturnStatement, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class CallStatement(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CallStatement, self).__init__(MOKE, children, line, lexpos)

    def getFunParams(self):
        return self.children[0].children

    def NumberOfFunParams(self):
        return len(self.childre[0].children)

class LoopStatement(ASTNode):
    def __init__(self, children, line, lexpos):
        super(LoopStatement, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

    def getCompoundStatement(self):
        return self.children[1]

class IfStatement(ASTNode):
    def __init__(self, children, line, lexpos):
        super(IfStatement, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

    def getStatement1(self):
        return self.children[1]

    def getStatement2(self):
        return self.children[2] 

class Operator(ASTNode):
    def __init__(self, children, line, lexpos, operator):
        super(Operator, self).__init__(MOKE, children, line, lexpos)
        self.operator = operator

    def getOperator(self):
        return self.operator

class UnaryExpr(Operator):
    def __init__(self, children, line, lexpos, operator):
        super(UnaryExpr, self).__init__(children, line, lexpos, operator)

    def getExpr(self):
        return self.children[0]

class BinaryExpr(Operator):
    def __init__(self, children, line, lexpos, operator):
        super(BinaryExpr, self).__init__(children, line, lexpos, operator)

    def getLeftExpr(self):
        return self.children[0]

    def getRightExpr(self):
        return self.children[1]

class ArrExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(ArrExpr, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class CallExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CallExpr, self).__init__(MOKE, children, line, lexpos)

    def getCallParams(self):
        return self.children[0]

class VarExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(VarExpr, self).__init__(MOKE, children, line, lexpos)

class IntExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(IntExpr, self).__init__(MOKE, children, line, lexpos)
    
    def getExpr(self):
        return self.children[0]

class CharExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CharExpr, self).__init__(MOKE, children, line, lexpos)

    def getExpr(self):
        return self.children[0]

class StringExpr(ASTNode):
    def __init__(self, children, line, lexpos):
        super(StringExpr, self).__init__(MOKE, children, line, lexpos)
    
    def getExpr(self):
        return self.children[0]

class Factor(ASTNode):
    def __init__(self, children, line, lexpos):
        super(Factor, self).__init__(FACTOR, children, line, lexpos)
        #self.factorType = nodeType

#    def getFactor(self):
#        return self.factorType

    def getVal(self):
        return self.children[0]

class Number(Factor):
    def __init__(self, children, line, lexpos):
        super(Number, self).__init__(children, line, lexpos)

class Id(Factor):
    def __init__(self, children, line, lexpos):
        super(Id, self).__init__(children, line, lexpos)

class Letter(Factor):
    def __init__(self, children, line, lexpos):
        super(Letter, self).__init__(children, line, lexpos)

class IntType(ASTNode):
    def __init__(self, children, line, lexpos):
        super(IntType, self).__init__(MOKE, children, line, lexpos)

class CharType(ASTNode):
    def __init__(self, children, line, lexpos):
        super(CharType, self).__init__(MOKE, children, line, lexpos)

class StringType(ASTNode):
    def __init__(self, children, line, lexpos):
        super(StringType, self).__init__(MOKE, children, line, lexpos)
