import CodeGenerator, ThreeAdrCode

class Optimiser():
    
    def __init__(self, code):
        self.code = code

    def flatten(self, param):
        res = []
        for var in param:
            res.extend(var if isinstance(var, list) else [var])
        return res

    def isVar(self, ident):
        if (ident[0] >= 'A' and ident[0] <= 'Z') or (ident[0] >= 'a' and ident[0] <= 'z') or ident[0] == '$':
            return True
        return False

    def isArrName(self, index, children):
        if index == len(children) - 1:
            return False
        if children[index + 1][0] == '[':
            return True
        return False

    def getVar(self, node):
        if node == None:
            return None
        if isinstance(node, CodeGenerator.Var) and node.isVar():
            return node.name
        elif isinstance(node, CodeGenerator.Arr) and node.index.isVar():
            return node.index.name
        return None

    def DataFlowGraph(self):
        self.labels = {}
        self.vars = set()
 
        for node in self.code:
            self.labels[node.label] = self.code.index(node)
            node.pred = []
            node.succ = []
            node.defs = []
            node.use = []
            node.callers = []

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

            # compute node.use
            if isinstance(node, ThreeAdrCode.Assign):
                child0 = node.getVar()
                child1 = self.getVar( node.First() )
                child2 = self.getVar( node.Second() )
                if child0.type == 'arr':
                    node.use.append(child0.index.name)
                if not child1 == None:
                    node.use.append(child1)
                if not child2 == None:
                    node.use.append(child2)
            elif node.single == True:
                var = self.getVar( node.getVar() )
                if not var == None:
                    node.use.append(var)
            elif isinstance(node, ThreeAdrCode.Decl) and node.getVar().type == 'arr':
                node.use.append(node.getVar().index.name)
            map(lambda var: self.vars.add(var), node.use)

            # compute node.def
            if isinstance(node, ThreeAdrCode.Assign) or isinstance(node, ThreeAdrCode.Pop):
                var = self.getVar( node.getVar() )
                if node.getVar().type == 'var' and not var == None:
                    node.defs.append(var)
            
            # compute node.succ and node.pred
            if isinstance(node, ThreeAdrCode.Goto):
                newIndex = self.labels[ node.children[0]]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif isinstance(node, ThreeAdrCode.IfTrue) or isinstance(node, ThreeAdrCode.IfFalse):
                newIndex = self.labels[node.children[2]]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif isinstance(node, ThreeAdrCode.Return):
                for caller in self.code[node.root].callers:
                    node.succ.append(caller + 1)
                    self.code[caller + 1].pred.append(index)

            if node.isFuncCall():
                newIndex = self.labels[ node.getJump() ]
                node.succ.append(newIndex)
                self.code[newIndex].pred.append( index )

            newIndex = index + 1
            if node.isOnlyJump() or newIndex == len(self.code):
                continue
            node.succ.append( newIndex )
            self.code[newIndex].pred.append( index )
            
                
        #for node in self.code:
        #    print '[', self.code.index(node), ']', 'succ', node.succ, 'pred', node.pred, 'use', node.use, 'defs', node.defs
        
    def LivenessAnalysis(self):
        for node in self.code:
            node.liveIn = set([])
            node.liveOut = set([])

        while True:
            for node in self.code:
                node.tempIn = node.liveIn
                node.tempOut = node.liveOut

                node.liveIn = set(node.use) | (node.liveOut - set(node.defs))
                node.liveOut = set([])
                map( lambda index: node.liveOut.update( self.code[index].liveIn ), node.succ)

            setA = map( lambda node: (node.liveIn, node.liveOut), self.code) 
            setB = map( lambda node: (node.tempIn, node.tempOut), self.code)
            converge = reduce( lambda x,y: x & y, map( lambda (x, y): x == y, zip(setA, setB) ) )

            if converge:
                break

        #for node in self.code:
        #    print '[', self.code.index(node), ']', 'in', list(node.liveIn), 'out', list(node.liveOut)

    def GraphColoring(self):
        edges = []    
        visit = {}   
        vars = list(self.vars)
        newVars = [None] * len(vars)
        colors = []
        self.doneColoring = False
        map(lambda var: edges.append(set()), vars)

        for node in self.code:      
            if len(node.defs) == 0:
                continue
           
             # add edges
            for var in node.liveOut:
                index1 = vars.index(var)
                index2 = vars.index(node.defs[0])
                if not index1 == index2:
                    edges[index1].add(index2)   
                    edges[index2].add(index1)

        #for x in xrange(len(vars)):
        #    for y in edges[x]:
        #        if x < y:
        #            print 'edge', vars[x], '->', vars[y]
        
        def DFS(node):
            if node in visit:
                return

            visit[node] = True
            nodes.append(node)
            
            for child in edges[node]:
                DFS(child)
        
        def BackColoring(ind):
            if self.doneColoring:
                return
            if ind == len(nodes):
                self.doneColoring = True
                return

            for color in xrange(1, 30):
                ok = True
                for child in edges[ nodes[ind] ]:
                    if colors[child] == color:
                        ok = False
                        break
                
                if not ok:
                    continue

                colors[ nodes[ind] ] = color 
                BackColoring(ind + 1)   
                if self.doneColoring:
                    return
                colors[ nodes[ind] ] = None          
    
        def Replace(node, map):
            for child in node.children:
                if isinstance(child, CodeGenerator.Var) and child.isVar() and child.name in map:
                    child.name = map[ child.name ]
                elif isinstance(child, CodeGenerator.Arr) and child.index.isVar() and child.index.name in map:
                    child.index.name = map[ child.index.name ] 
         
        for var in xrange( len(vars) ):
            if var in visit:
                continue
            nodes = []    
            DFS(var)
                
            colors = [None] * len(vars)
            self.doneColoring = False
            BackColoring(0)
            
            #print edges[1], edges[2], edges[3], edges[4]
            #print nodes, colors

            for x in nodes:
                newVars[x] = colors[x]

        res = 0
        replace = {}
        for var in xrange( len(vars) ):
            replace[ vars[var] ] = '__$R' + str(newVars[var])
            res = max(res, newVars[var])
            #print 'replace', vars[var], '->', replace[ vars[var] ]

        print ''
        print 'After graph coloring we need at max ', res, ' registers ;)'
      
        for node in self.code:
            Replace(node, replace)
        replace2 = {}
        for key,value in replace.items():
            replace2[value] = value[2:]
        for node in self.code:
            Replace(node, replace2)
            

    def printCode(self):
        print ''
        print '---------------', 'Optimiser', '---------------'
        for line in self.code:
            if line.label == '':
                print ''
            print '>', self.code.index(line), line
            if line.label == '' or line.name == 'end':
                print ''
        print ''

    def getCode(self):
        return self.code
        
            

