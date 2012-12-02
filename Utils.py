class Debug(object):
    pass

class ASTPrint(object):
    def __init__(self):
        self.edges = []    
        self.nodes = 1    

    def visit(self, node, ind = 1):
        """Visit node succ"""
        if isinstance(node, list) or isinstance(node, str) or isinstance(node, int):
            return
        
        print ind, node.nodeType        
    
        for child in node.children:
            self.nodes = self.nodes + 1
            self.edges.append( (ind, self.nodes) )
            self.visit(child, self.nodes)
   
    def printEdges(self):
        for edge in self.edges:
            print edge

class ASTVisitor(Debug):
    """General visitor"""

    def visit(self, node):
        """Visit a node"""
        print 'haha'
        methname = 'check_%s' % node.__class__.__name__
        method = getattr(self, methname, self.visit)
        method(node)
    
    def check(self, node):
        """Visit node succ"""
        print 'haha'
        for child in node.children:
            self.check(child)

class Debug(object):
    
    def __init__(self):
        self.errors = []

    def printErrors():
        if len(self.errors) > 0:
            header = 'Errors encountered in %s' % self.__class__.__name__
            print '%s %s %s' % ('---------------', header, '---------------')
            for error in self.errors:
                print '%s.' % error

        if len(self.errors) == 0:
            print '<NONE>'

    def hasErrors():
        return len(self.errors) > 0

