import sys, optparse, os, resource
import Parser, Lexer, SymbolTable, TypeChecker, Utils
import CodeGenerator, Optimiser, ThreeAdrCode, Emulator, Assembler

cmdline = optparse.OptionParser(add_help_option=False)
(opts, args) = cmdline.parse_args(sys.argv[1:])

def runFrontend(fileNameAlice, fileNameStem):
    # Parse Input
    parser = Parser.Parser()
    with open(fileNameAlice, 'r') as fin:
        line = fin.read()
        parser.parse(line)
    # Check for errors
    if parser.hasErrors():
        parser.printErrors()
        return False, None, None

    # Create Abstract Syntax Tree
    ast = parser.getAST()
    #print ast    

    # Create symbol Table
    stable = SymbolTable.SymbolTable()
    stable.visit(ast)

    if stable.hasErrors():
        stable.printErrors()
        return False, None, None

    #  Do static type checking  
    typecheck = TypeChecker.TypeChecker() 
    typecheck.visit(ast)

    if typecheck.hasErrors():
        typecheck.printErrors()
        return False, None, None

    #visitor = Utils.ASTPrint()
    #print '------------ AST ------------' 
    #visitor.visit(ast)
    #visitor.printEdges()
    
    return True, ast, stable

def runBackend(ast, stable, fileNameStem):
    # Do code generation
    codeGenerator = CodeGenerator.CodeGenerator()
    codeGenerator.visit(ast)
    code = codeGenerator.getCode()
    codeGenerator.printCode()

    #for test in code:
    #    if isinstance(test, ThreeAdrCode.Assign):
    #        print test.Second(), test.Second().type 

    optimiser = Optimiser.Optimiser(code)
    for times in xrange(1):
        optimiser.DataFlowGraph()
        optimiser.LivenessAnalysis()
        #optimiser.C
        optimiser.GraphColoring()
        optimiser.printCode()

    code = optimiser.getCode()
 
    emulator = Emulator.Emulate()
    emulator.emulate(code)

    assembler = Assembler.Assembler(code)
    assembler.generate()
    #assembler.printCode()
    assembler.writeToFile('test.asm')

    #Not working yet
    #test = Utils.Test()
    #result = test.SendRunCheck('test.asm')

def run (fileName):
    print 'Analysing file ', fileName
    fileNameStem = fileName[:-6]
    success, ast, stable = runFrontend(fileName, fileNameStem) 

    if success:
        print 'Compilation Successful'
        runBackend(ast, stable, fileNameStem)
    print ''

if __name__ == "__main__":
   
	# take some arguments
    for i in range(0, len(args)):
        abspath = os.path.abspath(args[i])
        if not os.path.isfile(abspath):
            print 'Argument', args[i], 'is not a file'
        else:
            run(abspath)
        
