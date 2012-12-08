import AST

class Debug(object):

    def __init__(self):
        self.errors = []
        self.code = []

    def printErrors(self):
        if len(self.errors) > 0:
            header = 'Errors encountered in %s' % self.__class__.__name__
            print '%s %s %s' % ('---------------', header, '---------------')
            for error in self.errors:
                print '%s.' % str(error)

        if len(self.errors) == 0:
            print '<NONE>'

    def hasErrors(self):
        return len(self.errors) > 0


class ASTPrint(object):
    def __init__(self):
        self.edges = []    
        self.nodes = 1    

    def visit(self, node, ind = 1):
        """Visit node children"""
        print ind, node.nodeType        

        for child in node.children:
            if isinstance(child, AST.ASTNode):       
                self.nodes = self.nodes + 1
                self.edges.append( (ind, self.nodes) )
                self.visit(child, self.nodes)
   
    def printEdges(self):
        for edge in self.edges:
            print edge

class ASTVisitor(Debug):
    """Visit an AST tree"""
    def __init__(self):
        Debug.__init__(self)
    
    def visit(self, node):
        """Visit a node"""
        methname = 'check_%s' % node.__class__.__name__
        method = getattr(self, methname, self.check)
        method(node)
    
    def check(self, node):
        #print node.nodeType
        """Visit node children"""
        for child in node.children:
            if isinstance(child, AST.ASTNode):
                child.parent = node
                self.visit(child)

