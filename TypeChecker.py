import AST, Utils

class TypeChecker(Utils.ASTVisitor):

    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.nodeType = {}
   
    def seeType(self, nodeType):
        if isinstance(nodeType, AST.IntType):
            return 'number'
        elif isinstance(nodeType, AST.CharType):
            return 'letter'
        elif isinstance(nodeType, AST.StringType):
            return 'sentence'
        elif isinstance(nodeType, AST.BooleanType):
            return 'boolean'
 
    def check_FunParams(self, node):
        Utils.ASTVisitor.check(self, node)  
        pass

    def check_ActualParams(self, node):
        Utils.ASTVisitor.check(self, node)
        pass

    #def check_VarDecl(self, node):
     #   Utils.ASTVisitor.check(self, node)
     #   if len(node.children) > 1:
      #      leftExprType = self.nodeType[node.children[0]]
       #     rightExprType = self.nodeType[node.children[1]]
        #    if leftExprType != rightExprType:
         #       self.errors.append("Type clash in assignment on line %d. One type is '%s' and the other is '%s'." % (node, line, leftExprType, rightExprType))

    #def check_VarExpr(self, node):
     #   Utils.ASTVisitor.check(self, node)
      #  self.nodeType[node] =  

    def check_VarDecl(self, node):
        Utils.ASTVisitor.check(self, node)
        if (len(node.children) > 1):
            typeExpr = node.getType()
            expr = self.nodeType[node.getExpr()]
            if typeExpr != expr:
                self.errors.append("Type clash in assignment on line %d. One type is '%s' and the other is '%s'" % (node.line, self.seeType(typeExpr), self.seeType(expr)))
            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            print self.seeType(typeExpr)
            print self.seeType(expr)    
            print node.nodeType 
            print "ddddddddddddddddddddddddddddddddddddddddddddddd"
        else:
            self.nodeType[node] = node.getType()

    def check_VarExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.nodeType[node] = AST.IntType #TODO

    def check_ReadStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        pass

    def check_AssignStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        leftExprType = self.nodeType[node.getLeftExpr()]
        rightExprType = self.nodeType[node.getRightExpr()]
        if leftExprType != rightExprType:
            self.errors.append("Type clash in assignment on line %d. One type is '%s' and the other is '%s'" % (node.line, leftExprType, rightExprType))
        pass

    def check_IncrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        exprType = self.nodeType[node.getExpr()]
        if not isinstance(exprType, AST.IntType):
            self.errors.append("Increment statement on line %d is not applied to an integer" % node.line)

    def check_DecrementStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        exprType = self.nodeType[node.getExpr]
        if not isinstance(exprType, AST.IntType):
            self.errors.append("Decrement statement on line %d is not applied to an integer" % node.line)

    def check_CallStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        self.check_ActualParams(node, node.getFunParams())
        pass

    def check_LoopStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        condType = self.nodeType[node.getExpr()]
        if not isinstance(condType, AST.BooleanType):
            self.errors.append("Loop header conditional on line %d does not evaluate to a Boolean" % node.line)

    def check_IfStatement(self, node):
        Utils.ASTVisitor.check(self, node)
        pass

    def check_BinaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        leftExprType = self.nodeType[node.getLeftExpr()]
        rightExprType = self.nodeType[node.getRightExpr()]
        if leftExprType != rightExprType:
            self.error.append("Type clash for binary operator '%s' in line %d. One type is '%s' and the other is '%s'." % (node.operator,
                                node.line, self.seeType(leftExprType), self.seeType(rightExprType)))
        if AST.BinaryExpr.isRelational(node.operator):
            if (not(isinstance(leftExprType, AST.IntType) and isinstance(rightExprType, AST.IntType))) and (not(isinstance(leftExprType, AST.CharType) and isinstance(rightExprType, AST.CharType))):
                self.errors.append("Relational operator '%s' on line %d not applied to integer or character values." % (node.operator, node.line))
            self.nodeType[node] = AST.BooleanType
        if AST.BinaryExpr.isBoolean(node.operator):
            if not(isinstance(leftExprType, AST.BooleanType) and isinstance(rightExprType, AST.BooleanType)):
                self.errors.append("Logical operator '%s' on line %d not applied to Boolean values" % (node.operator, node.line))
            self.nodeType[node] = AST.BooleanType
        else:
            self.nodeType[node] = leftExprType

    def check_UnaryExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        exptType = self.nodeType[node.getExpr()]
        if node.operator == '+' or node.operator == '-' or node.operator == '~':
            if not isinstance(exprType, AST.IntType):
                self.errors.append("Unary operator '%s' on line %d not applied to an integer" % (node.operator, node.line))
            self.nodeType[node] = exprType
        elif node.operator == '!':
            if not isinstance(exprType, AST.BooleanType):
                self.errors.append("Unary operator '%s' on line %d is not applied to a boolean" % (node.operator, node.line))
            self.nodeType[node] = exprType       

    def check_CallExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        pass

    def check_IntExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.nodeType[node] = AST.IntType

    def check_CharExpr(self, node):
        Utils.ASTVisitor.check(self, node)
        self.nodeType[node] = AST.CharType

    def check_StringType(self, node):
        Utils.ASTVisitor.check(self, node)
        self.nodeType[npde] = AST.StringType()
