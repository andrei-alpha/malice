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

    def getArr(self, node):
        if node == None:
            return None
        if node.Btype == 'IntType':
            return node.name
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

                arr0 = self.getArr( node.getVar() )
                arr1 = self.getArr( node.First() )
                arr2 = self.getArr( node.Second() )
                if not arr1 == None:
                    node.use.append(arr1)
                if not arr2 == None:
                    node.use.append(arr2)
                if not arr0 == None:
                    node.use.append(arr0)
            elif isinstance(node, ThreeAdrCode.If):
                child0 = self.getVar( node.First() )
                child1 = self.getVar( node.Second() )
                if not child0 == None:
                    node.use.append(child0)
                if not child1 == None:
                    node.use.append(child1)
                arr0 = self.getArr( node.First() )
                arr1 = self.getArr( node.Second() )
                if not arr0 == None:
                    node.use.append(arr0)
                if not arr1 == None:
                    node.use.append(arr1)
            elif node.single == True and not isinstance(node, ThreeAdrCode.Pop): 
                var = self.getVar( node.getVar() )
                if not var == None:
                    node.use.append(var)
                arr = self.getArr( node.getVar() )
                if not arr == None:
                    node.use.append(arr)
            elif isinstance(node, ThreeAdrCode.Decl) and node.getVar().type == 'arr':
                node.use.append(node.getVar().index.name)
            elif isinstance(node, ThreeAdrCode.Read):
                arr = self.getArr( node.getVar() )
                if not arr == None:
                    node.use.append(arr)

            map(lambda var: self.vars.add(var), node.use)

            # compute node.def
            if isinstance(node, ThreeAdrCode.Assign) or isinstance(node, ThreeAdrCode.Read):
                var = self.getVar( node.getVar() )
                if not var == None and node.getVar().type == 'var':
                    node.defs.append(var)
                #arr = self.getArr( node.getVar() )
                #if not arr == None:
                #    node.defs.append(arr)
            elif isinstance(node, ThreeAdrCode.Param):
                var = node.getVarName()
                node.defs.append(var)
            
            # compute node.succ and node.pred
            if isinstance(node, ThreeAdrCode.Goto):
                newIndex = self.labels[ node.children[0] ]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif isinstance(node, ThreeAdrCode.If):
                newIndex = self.labels[ node.getJump() ]
                node.succ.append( newIndex )
                self.code[newIndex].pred.append( index )
            elif isinstance(node, ThreeAdrCode.Return):
                pass
                #for caller in self.code[node.root].callers:
                #    node.succ.append(caller + 1)
                #    self.code[caller + 1].pred.append(index)
            elif isinstance(node, ThreeAdrCode.End):
                pass
                #for caller in self.code[node.root].callers:
                #    node.succ.append(caller + 1)
                #    self.code[caller + 1].pred.append(index)

            if node.isFuncCall():
                pass
                #newIndex = self.labels[ node.getJump() ]
                #node.succ.append(newIndex)
                #self.code[newIndex].pred.append( index )

            newIndex = index + 1
            if node.isOnlyJump() or newIndex == len(self.code):
                continue
            node.succ.append( newIndex )
            self.code[newIndex].pred.append( index )
            
                
        #for node in self.code:
        #    print '[', self.code.index(node), ']', 'succ', node.succ, 'pred', node.pred, 'use', node.use, 'defs', node.defs
        #print self.vars
        

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

    def ConstantAnalysis(self):
        for node in self.code:
            node.defsIn = set([])
            node.defsOut = set([])
            node.defsKill = set([])
            node.defsGen = set([])

    def GraphColoring(self):
        edges = []    
        visit = {}   
        vars = list(self.vars)
        newVars = [None] * len(vars)
        colors = []
        self.doneColoring = False
        map(lambda var: edges.append(set()), vars)

        for node in self.code:      
            if len(node.defs) == 0 or not node.defs[0] in vars:
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

            for color in xrange(8, 40):
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
                if isinstance(child, CodeGenerator.Var) and child.isVar() and child.ref == False and child.name in map:
                    #print 'replace', child.name, map[ child.name ]
                    child.name = map[ child.name ]
                elif isinstance(child, CodeGenerator.Arr) and child.index.isVar() and child.index.name in map:
                    #print 'replace', child.index.name, map[ child.index.name ]
                    child.index.name = map[ child.index.name ] 
    
                #if isinstance(child, CodeGenerator.Arr):
                #    print '#try replace', child, child.Btype, child.name in map
                if (isinstance(child, CodeGenerator.Var) or isinstance(child, CodeGenerator.Arr)) and child.Btype == 'IntType' and child.name in map:
                    #print '#do replace', map[ child.name ]
                    child.name = map[ child.name ]
         
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
            replace[ vars[var] ] = '__r' + str(newVars[var])
            res = max(res, newVars[var])
            #print 'replace', vars[var], '->', replace[ vars[var] ]

        print ''
        print 'After graph coloring we need at max ', (res - 7), ' registers ;)'
      
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
            if isinstance(line, ThreeAdrCode.Func):
                print ''
            print '>', self.code.index(line), line
            if line.name == 'end':
                print ''
        print ''

    def getCode(self):
        return self.code
        
            

