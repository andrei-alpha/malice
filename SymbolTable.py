#!/bin/python
import Utils, AST

# Analyses the abstract syntax tree.
# Inputs are a symbolTable dictionary of form { id : ASTNode  ) },
# the starting AST node and a flags dictionary of form { nodeType : info } where any relevant information
# (isReference, globalSymbol, etc) for the particular node is set.
# Does not return anything. Will throw a semantic error if the code breaks the rules.

class SymbolTable(Utils.ASTVisitor):
    def __init__(self):
        Utils.ASTVisitor.__init__(self)
        self.scopeStack = []
            
    def getCurrentScope(self):
        return self.scopeStack[-1]


    def check_CompilationUnit(self, node):
        newScope = ScopeNode(node)
        self.scopeStack.append(newScope)
        Utils.ASTVisitor.check(self, node)
        self.root = self.getCurrentScope()
        del self.scopeStack[-1]

        count = 0
        programs = self.root.getPrograms()
        for program in programs:
            if not program.name == 'hatta':
                continue

            if isinstance(program, AST.FuncDecl):
                self.errors.append("The main procedure %s is declared as a function rather than a procedure" % ('hatta'))
            else:
                count += 1              

        if count > 1:
            self.errors.append("Multiple definitions of main procedure %s found" % ('hatta'))
        elif count == 0:
            self.errors.append("The main procedure %s was not found" % ('hatta'))            

        pass

    def check_FuncDecl(self, node):
        scope = self.getCurrentScope()
        scope.addSymbol(node, self.errors)        
        
        newScope = ScopeNode(node, scope)
        newScope.addParams(node.children[0], self.errors)
        self.scopeStack.append(newScope)
        
        Utils.ASTVisitor.check(self, node)
        self.root = self.getCurrentScope()
        del self.scopeStack[-1]
       
        if not self.root.hasReturnStatement:
            self.errors.append("The function %s on line %d doesn't have a return statement" % (node.name, node.line))

        pass

    def check_ProcDecl(self, node):
        scope = self.getCurrentScope()
        scope.addSymbol(node, self.errors)
        
        newScope = ScopeNode(node, scope)
        newScope.addParams(node.children[0], self.errors)
        self.scopeStack.append(newScope)
        
        Utils.ASTVisitor.check(self, node)
        self.root = self.getCurrentScope()
        del self.scopeStack[-1]
        pass

    def check_Body(self, node):
        if isinstance(node.parent, AST.FuncDecl) or isinstance(node.parent, AST.ProcDecl):
            Utils.ASTVisitor.check(self, node)
            return
         
        scope = self.getCurrentScope()
                
        newScope = ScopeNode(node, scope)
        self.scopeStack.append(newScope)

        Utils.ASTVisitor.check(self, node)
        self.root = self.getCurrentScope()
        del self.scopeStack[-1]
        pass

    def check_CallStatement(self, node):
        scope = self.getCurrentScope()
        node.decl = scope.resolveSymbol(node, self.errors)
        Utils.ASTVisitor.check(self, node)
        pass

    def check_ReturnStatement(self, node):
        scope = self.getCurrentScope()
        scope.hasReturnStatement = True
        Utils.ASTVisitor.check(self, node)

    def check_VarDecl(self, node):
        scope = self.getCurrentScope()
        scope.addSymbol(node, self.errors)
        Utils.ASTVisitor.check(self, node)
        pass

    def check_ArrDecl(self, node):
        scope = self.getCurrentScope()
        scope.addSymbol(node, self.errors)

        Utils.ASTVisitor.check(self, node)
        pass

    def check_CallExpr(self, node):
        scope = self.getCurrentScope()
        decl = scope.resolveSymbol(node, self.errors)
        node.decl = decl
        Utils.ASTVisitor.check(self, node)
        pass

    def check_VarExpr(self, node):
        scope = self.getCurrentScope()
        decl = scope.resolveSymbol(node, self.errors)

        if decl:
            if isinstance(decl, AST.ArrDecl):
                if not (isinstance(node.parent, AST.FunParams) or isinstance(node.parent, AST.CallParams)):
                    self.errors.append("Reference to %s in line %d is a l-value when an r-value is needed" % (decl.name, node.line) ) 
                else:
                    node.decl = decl
                    node.ref = True    
            elif not isinstance(decl, AST.VarDecl):
                self.errors.append("Reference to %s in line %d is not a r-value as required" % (decl.name, node.line) )      
            else:
                node.decl = decl
                node.ref = decl.ref   

        Utils.ASTVisitor.check(self, node)
        pass

    def check_ArrExpr(self, node):
        scope = self.getCurrentScope()
        decl = scope.resolveSymbol(node, self.errors)

        if decl:
            if isinstance(decl, AST.ArrDecl):
                node.decl = decl
            elif isinstance(decl, AST.VarDecl) and decl.ref == True:
                node.decl = decl
                node.ref = decl.ref
            else:
                self.errors.append("Reference to %s in line %d is a r-value when a l-value is required" % (decl.name, node.line) )

        Utils.ASTVisitor.check(self, node)        
        pass


class ScopeNode(object):
    def __init__(self, node, parent = None):
        self.hasReturnStatement = False
        self.node = node
        self.symbols = {}
        self.maybe = {}
        if parent is not None:
            for key,value in parent.symbols.items():
                self.maybe[key] = value
            for key,value in parent.maybe.items():
                self.maybe[key] = value
    
    def getPrograms(self):
        programs = []
        for key, value in self.symbols.items():
            if isinstance(value, AST.FuncDecl) or isinstance(value, AST.ProcDecl):
                programs.append(value)
        return programs


    def addParams(self, node, stdout):
        if not isinstance(node, AST.FunParams):
            return
        for param in node.children:
            pass

    def addSymbol(self, node, stdout):
        if node.name in self.symbols:
            stdout.append("Symbol '%s' with type '%s' already defined on line %d" % (node.name, node.__class__.__name__, node.line))
        self.symbols[node.name] = node

    def resolveSymbol(self, node, stdout):
        if node.name in self.symbols:
            return self.symbols[node.name]

        if node.name in self.maybe:
            return self.maybe[node.name]
        
        stdout.append("Symbol '%s' with type '%s' undefined on line %d" % (node.name, node.__class__.__name__, node.line))
