import ThreeAdrCode

class Optimiser():
    
    def __init__(self, code):
        self.code = code
        self.labels = {}

        for node in self.code:
            self.labels[node.label] = self.code.index(node)
            node.pred = []
            node.succ = []
            node.defs = []
            node.callers = []

    def DataFlowGraph(self):
        root = None

        for node in self.code:
            if isinstance(node, ThreeAdrCode.Func):
                root = self.code.index(node)
            if node.isFuncCall():
                jump = self.labels[ node.getJump() ]
                self.code[jump].callers.append(self.code.index(node))
            node.root = root

        for node in self.code:
            index = self.code.index(node)

            if node.name == 'assign':
                node.defs.append(node.children[0])
            elif node.name == 'goto':
                newIndex = self.labels[node.children[0]]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif node.name == 'ifTrue' or node.name == 'ifFalse':
                newIndex = self.labels[node.children[2]]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif node.name == 'call':
                newIndex = self.labels.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif node.name == 'return':
                for caller in self.code[node.root].callers:
                    node.succ.append(caller)
                    self.code[caller].pred.append(index)

            newIndex = index + 1
            if node.isOnlyJump() or newIndex <= len(self.code):
                continue
            node.succ.append( newIndex )
            self.code[newIndex].pred.append( index )
            
                
        for node in self.code:
            print node
            print '[', self.code.index(node), ']', 'succ', '{', node.succ, '}', 'pred', '{', node.pred, '}'
        

    
