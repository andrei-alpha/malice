import AST, Utils

# The constructor takes an ASTVisitor to traverse the tree
class TypeChecker(Utils.ASTVisitor):

    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.nodeType = {}
   
    # Converts an ExprType into a nice;) English representation
    def seeType(self, nodeType):
        if nodeType == 'IntType':
            return 'number'
        elif nodeType == 'CharType':
            return 'letter'
        elif nodeType == 'StringType':
            return 'sentence'
        elif nodeType == 'BooleanType':
            return 'boolean'
        elif nodeType == 'ArrType':
            return 'array'
        return None

    # Converts an ExprNode into a NodeType
    def convertToType(self, nodeType):
        if nodeType == 'IntExpr':
            return 'IntType'
        elif nodeType == 'CharExpr':
            return 'CharType'
        elif nodeType == 'StringExpr':
            return 'StringType'
        elif nodeType == 'ArrExpr':
            return 'ArrType'
        return None

    def checkParams(self, node, callParams, funParams):
        for callParam, funParam in zip(callParams, funParams):
            type1 = self.nodeType[callParam]
            type2 = self.nodeType[funParam]
            
            if funParam.ref == True:
                type1 = 'ArrType'
            if isinstance(callParam, AST.VarExpr) and (callParam.decl.getType() == 'ArrDecl' or callParam.decl.ref == True):
                type2 = 'ArrType'

            #print callParam.decl, type1, type2, node.line

            if type1 != type2:
                self.errors.append("Type clash on call for function '%s' on line %d for parameter '%s'" % (node.name, node.line, callParam.name))
        pass
 
    def check_VarDecl(self, node):
        Utils.ASTVisitor.check(self, node)
        if len(node.children) > 1:
            typeExpr = node.getType()
            expr = self.nodeType[node.getExpr()]
            if typeExpr != expr:
                self.errors.append("Type clash in assignment on line %d. One type is '%s' and the other is '%s'" % (node.line, self.seeType(typeExpr), self.seeType(expr)))
        else:
            self.nodeType[node] = node.getType()

    def check_VarExpr(self, node):
        #print node.decl

        self.nodeType[node] = node.decl.getType()
        Utils.ASTVisitor.check(self, node)

    def check_PrintStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        pass

    def check_ReadStatement(self, node):
        Utils.ASTVisitor.check(self, node)

        expr = node.getExpr()
        if not (isinstance(expr, AST.VarExpr) or isinstance(expr, AST.ArrExpr)):
            self.errors.append("Read statement on line %d is only possible to an r-value" % (node.line) )

        pass

    def check_AssignStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        #print node.getLeftExpr(), node.line

        if not (isinstance(node.getLeftExpr(), AST.VarExpr) or isinstance(node.getLeftExpr(), AST.ArrExpr)):
            self.errors.append("Assignment on line %d is only possible to an r-value" % (node.line) )

        leftExprType = self.nodeType[node.getLeftExpr()]
        rightExprType = self.nodeType[node.getRightExpr()]
        if leftExprType != rightExprType:
            self.errors.append("Type clash in assignment on line %d. One type is '%s' and the other is '%s'" % (node.line, self.seeType(leftExprType), self.seeType(rightExprType)))
        pass

    def check_IncrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        exprType = self.nodeType[node.getExpr()]
        if not exprType == 'IntType':
            self.errors.append("Increment statement on line %d is not applied to an integer" % node.line)
        if not (isinstance(node.getExpr(), AST.VarExpr) or isinstance(node.getExpr(), AST.ArrExpr)):
            self.errors.append("Increment Statement on line %d is only possible to an r-value" % (node.line) )
    
    def check_DecrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        exprType = self.nodeType[node.getExpr()]
        if not exprType == 'IntType':
            self.errors.append("Decrement statement on line %d is not applied to an integer" % node.line)
        elif not (isinstance(node.getExpr(), AST.VarExpr) or isinstance(node.getExpr(), AST.ArrExpr)):
            self.errors.append("Decrement on line %d is only possible to an r-value" % (node.line) )

    def check_CallStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        funParams = node.decl.getFunParams()
        callParams = node.getFunParams()
        self.checkParams(node, callParams, funParams)
        pass

    def check_LoopStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        condType = self.nodeType[node.getExpr()]
        if not condType == 'BooleanType':
            self.errors.append("Loop header conditional on line %d does not evaluate to a Boolean" % node.line)

    def check_IfStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        conditional = self.nodeType[node.getExpr()]
        
        if not conditional == 'BooleanType':
            print conditional
            self.errors.append("Conditional on line %d doesn't have a boolean condition" % node.line)

    def check_BinaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)

        #print 'ask', node.getRightExpr(), node.line
        leftExprType = self.nodeType[node.getLeftExpr()]
        rightExprType = self.nodeType[node.getRightExpr()]
        #print 'found', leftExprType, rightExprType       

        if leftExprType != rightExprType:
            self.errors.append("Type clash for binary operator '%s' in line %d. One type is '%s' and the other is '%s'" % (node.operator,
                                node.line, self.seeType(leftExprType), self.seeType(rightExprType)))
        if node.isRelational(node.operator):
            if (not(leftExprType == 'IntType' and rightExprType == 'IntType')) and (not(leftExprType == 'CharType' and rightExprType == 'CharType')):
                self.errors.append("Relational operator '%s' on line %d not applied to integer or character values" % (node.operator, node.line))
            self.nodeType[node] = 'BooleanType'
        elif node.isBoolean(node.operator):
            if not leftExprType == 'BooleanType' and not rightExprType == 'BooleanType':
                self.errors.append("Logical operator '%s' on line %d not applied to Boolean values" % (node.operator, node.line))
            self.nodeType[node] = 'BooleanType'
        else:
            self.nodeType[node] = leftExprType

    def check_UnaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        exprType = self.nodeType[node.getExpr()]

        if node.operator == '-' or node.operator == '~':
            if not exprType == 'IntType':
                self.errors.append("Unary operator '%s' on line %d not applied to an integer" % (node.operator, node.line))
            #print 'add', exprType
            self.nodeType[node] = exprType
        elif node.operator == '!':
            if not exprType == 'BooleanType':
                self.errors.append("Unary operator '%s' on line %d is not applied to a boolean" % (node.operator, node.line))
            #print 'add', exprType
            self.nodeType[node] = exprType       

    def check_CallExpr(self, node):
        #print node, '## decl', node.decl.getReturnType(), node.line
        if not isinstance(node.decl, AST.FuncDecl):
            self.errors.append("The call expression to %s on line %d references a procedure, which does not return a value" % (node.name, node.line)) 
            self.nodeType[node] = None
        else:
            self.nodeType[node] = node.decl.getReturnType().nodeType
        Utils.ASTVisitor.check(self, node)
        pass

    def check_ArrExpr(self, node):
        #print node, 'decl', node.decl, node.line

        self.nodeType[node] = node.decl.getBaseType().nodeType
        Utils.ASTVisitor.check(self, node)

    def check_IntExpr(self, node):
        #print 'wtf2', node.nodeType

        self.nodeType[node] = self.convertToType(node.nodeType)
        Utils.ASTVisitor.check(self, node)

    def check_CharExpr(self, node):
        #print 'wtf3', node.nodeType        

        self.nodeType[node] = self.convertToType(node.nodeType)
        Utils.ASTVisitor.check(self, node)
       
    def check_StringExpr(self, node):
        self.nodeType[node] = self.convertToType(node.nodeType)
        Utils.ASTVisitor.check(self, node)

