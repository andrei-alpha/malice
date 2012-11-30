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

class ASTNode(object):
	def __init__(self, nodeType, line, lexpos, children):
		self.nodeType = nodeType
		self.line     = line
		self.lexpos   = lexpos
		self.children = children
	
	def getNodeType(self):
		return self.nodeType

class CompilationUnit(self):
	def __init__(self, nodeType, line, lexpos, children):
		super(CompilationUnit, self).__init__(COMPILATION_UNIT, line, lexpos, children)
	
	def getDecls(self):
		return self.children[0]

class Decls(self):
	def __init__(self, line, lexpos, children):
		super(DeclNode, self).__init__(DECLARATION, line, lexpos, children)

def Body(self):
    def __init__(self, nodeType, lien, lexpos, children):
        super(Body, self).__init__(BODY, line, lexpos, children)

    def getDecls(self):
        return self.children[0]

    def getStatement(self):
        return self.children[1]

def FormalParams(self):
    def __init__(self, line, lexpos, children):
        super(FormalParams, self).__init__(FORMAL_PARAMS, line, lexpos, children)


class VarDecl(StatementList):
	def __init__(self, line, lexpos, children):
		super(VarDecl, self).__init__(DECLARATION, line, lexpos, children)

	def getType(self):
		return self.children[1]

class ArrayDecl(DeclNode):
	def __init__(self, line, lexpos, children):
		super(ArrayDecl, self).__init__(DECLARATION, line, lexpos, children)

	def getSizeExpr(self):
		return self.children[0]

	def getBaseType(self):
		return self.children[1]

def CompoundStatement(ASTNOde):
	def __init__(self, nodeType, line, lexpos, chilren):
		super(CompoundStatement, self).__init__(nodeType, line, lexpos, children)

	#def getStatement(self):	

#Statements

def PrintStatement(CompoundStatement):
	def __init__(self, nodeType, line, lexpos, children):
		super(PrintStatement, self).__init__(nodeType, line, lexpos, children)

	def getExpr(self):
		return self.children[0]

def ReadStatement(CompoundStatement):
	def __init__(self, nodeType, line, lexpos, children):
		super(ReadStatement, self).__init__(nodeType, line, lexpos, children)

	def getExpr(self):
		return self.children[0]

def NullStatement(CompoundStatement):
	def __init__(self, nodeType, line, lexpos, children):
		super(NullStatement, self).__init__(nodeType, line, lexpos, children)

def AssignStatement(CompoundStatement):
	def __init__(self, nodeType, line, lexpos, children):
		super(AssignStatement, self).__init__(nodeType, line, lexpos, children)

	def getLeftExpr(self):
		return self.children[0]

	def getRightExpr(self):
		return self.children[1]

def ActualParams(self):
	def __init__(self, nodeType, line, lexpos, children):
		super(ActualParams, self).__init__(nodeType, line, lexpos, children)

	def getLeftExpr(self):
		return self.children[0]

	def getRightExpr(self):
		return self.children[1]

def Operator(self):
	def __init__(self, nodeType, line, lexpos, operator, children):
		super(Operator, self).__init__(nodeType, line, lexpos, children)
		self.operator = operator

	def getOperator(self):
		return self.operator

def UnaryNode(Operator):
	def __init__(self, line, lexpos, operator, children):
		super(UnaryOperator, self).__init__(UNARY_OP, line, lexpos, operaotr, children)

	def getExpr(self):
		return self.children[0]

def BinaryNode(Operator):
	def __init__(self, line, lexpos, operator, children):
		super(BinaryNode, self).__init__(BINARY_OP, line, lexpos, children)

	def getLeftExpr(self):
		return self.children[0]

	def getRightExpr(self):
		return self.children[1]

def Factor(self):
	def __init__(self, nodeType, line, lexpos, children):
		super(Factor, self).__init__(FACTOR, line, lexpos, children)
		self.factorType = nodeType

	def getFactor(self):
		return self.factorType

	def getVal(self):
		return self.children[0]

def Number(Factor):
	def __init__(self, line, lexpos, children):
		super(Number, self).__init__(NUMBER, line, lexpos, children)

def Id(Factor):
	def __init__(self, line, lexpos, children):
		super(Id, self).__init__(ID, line, lexpos, children)

def Letter(Factor):
	def __init__(self, line, lexpos, children):
		super(Letter, self).__init__(LETTER, line, lexpos, children)

def IntType():
	def __init__(self, nodeType, line, lexpos, children):
		super(IntType, self).__init__(nodeType, line, lexpos, children)

def CharType():
	def __init__(self, nodeType, line, lexpos, children):
		super(CharType, self).__init__(nodeType, line, lexpos, children)

def StringType():
	def __init__(self, nodeType, line, lexpos, children):
		super(StringType, self).__init__(nodeType, line, lexpos, children)
