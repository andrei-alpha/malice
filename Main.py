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

    return True, ast, stable

def runBackend(ast, stable, fileNameStem):
    # Do code generation
    codeGenerator = CodeGenerator.CodeGenerator()
    codeGenerator.visit(ast)
    code = codeGenerator.getCode()
    #codeGenerator.printCode()

    optimiser = Optimiser.Optimiser(code)
    for times in xrange(1):
        optimiser.DataFlowGraph()
        optimiser.LivenessAnalysis()
        optimiser.ConstantAnalysis()
        optimiser.GraphColoring()
        #optimiser.printCode()

    code = optimiser.getCode()
 
    # Remove this comment if you want to test inside an emulator
    #emulator = Emulator.Emulate()
    #emulator.emulate(code)

    assembler = Assembler.Assembler(code)
    assembler.generate()
    #assembler.printCode()

    filename = os.path.basename(fileNameStem)
    assembler.writeToFile(filename + '.asm')
    os.system('nasm -f elf64 %s.asm' % filename)
    os.system('gcc -c extern.c')
    os.system('gcc -o %s extern.o %s.o' % (filename, filename) )
    print 'Code generation successful to "%s"' % filename

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
        
