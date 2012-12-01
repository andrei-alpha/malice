import sys, optparse, os, resource
import Parser, Lexer, SymbolTable, TypeChecker

cmdline = optparse.OptionParser(add_help_option=False)
(opts, args) = cmdline.parse_args(sys.argv[1:])

def runFrontend(fileNameAlice, fileNameStem):
    # Parse Input
    parser = Parser.Parser()
    with open(fileNameAlice, 'r') as fin:
        line = fin.read()
        parser.parse(line)
    # to do check for errors

    # Create Abstract Syntax Tree
    ast = parser.getAST()
    

    # Create symbol Table
    stable = SymbolTable.SymbolTable()

    # Do static type checking  
    typecheck = TypeChecker.Check() 

    #print '------------ AST ------------' 
    #print ast

    return False, None, None

def runBackend(ast, stable, fileNameStem):
    # Do code generation
    pass

def run (fileName):
    print 'Analysing file ', fileName
    fileNameStem = fileName[:-6]
    success, ast, stable = runFrontend(fileName, fileNameStem) 

    if success:
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
        
