#!bin/python
import Lexer, Utils, AST
import yacc

class Parser(Utils.Debug):
    tokens = Lexer.Lexer.tokens
    precedence = (('left', 'LOGICAL_OR'),
        ('left', 'LOGICAL_AND'),
        ('left', '|'),
        ('left', '^'),
        ('left', '&'),
        ('left', 'EQUAL', 'NOT_EQUAL'),
        ('left', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'LOGICAL_NOT', '~'),
        ('left', ')'),
        ('right', '('))

    def p_error(self, error):
        self.errors.append("Parse error: '%s'" % error)

    def p_CompilationUnit(self, p):
        """compilationUnit : decls"""
        p[0] = AST.CompilationUnit([p[1]], p.lineno(1), p.lexpos(1))
    

    def p_Decls(self, p):
        """decls : decls decl 
        | decl"""
        if len(p) == 3:
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Decls([p[1]], p.lineno(1), p.lexpos(1))

    def p_Decl(self, p):
        """decl : varDecl 
        | funcDecl 
        | procDecl"""
        p[0] = p[1]
      
    def p_VarDecl(self, p):
        """varDecl : ID WAS A type terminator
        | ID WAS A type TOO terminator"""
        p[0] = AST.VarDecl([p[4]], p.lineno(1), p.lexpos(1), p[1])

    def p_VarDecl2(self, p):
        """varDecl : ID WAS A type OF expr terminator"""
        p[0] = AST.VarDecl([p[4], p[6]], p.lineno(1), p.lexpos(1), p[1])
  
    def p_ArrDecl(self, p):
        """varDecl : ID HAD expr type terminator"""
        p[0] = AST.ArrDecl([p[3], p[4]], p.lineno(1), p.lexpos(1), p[1])
    
    def p_FuncDecl(self, p):
        """funcDecl : THE ROOM ID funParams CONTAINED A type body"""
        p[0] = AST.FuncDecl([p[4], p[7], p[8]], p.lineno(3), p.lexpos(3), p[3])

    def p_ProcDecl(self, p):
        """procDecl : THE LOOKING '-' GLASS ID funParams body"""
        p[0] = AST.ProcDecl([p[6], p[7]], p.lineno(5), p.lexpos(5), p[5])
    
    def p_FunParams(self, p):
        """funParams : '(' ')'
        | '(' funParamsList ')'"""
        if len(p) == 3:
            p[0] = AST.FunParams([], p.lineno(1), p.lexpos(1))
        else:
            p[0] = p[2]

    def p_CallParams(self, p):
        """callParams : '(' ')'
        | '(' callParamsList ')'"""
        if len(p) == 3:
            p[0] = AST.CallParams([], p.lineno(1), p.lexpos(1))
        else:
            p[0] = p[2]

    def p_FunParamList(self, p):
        """funParamsList : funParam 
        | funParamsList ',' funParam"""
        if len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.FunParams([p[1]], p.lineno(1), p.lexpos(1))

    def p_CallParamList(self, p):
        """callParamsList : expr 
        | callParamsList ',' expr"""
        if len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.CallParams([p[1]], p.lineno(1), p.lexpos(1))

    def p_FunParam(self, p):
        """funParam : type ID"""
        p[0] = AST.VarDecl([p[1]], p.lineno(2), p.lexpos(2), p[2])

    def p_FunParam2(self, p):
        """funParam : refType ID"""
        p[0] = AST.VarDecl([p[1]], p.lineno(2), p.lexpos(2), p[2], True)

    def p_body(self, p):
        """body : OPENED decls compStatement CLOSED
        | OPENED compStatement CLOSED
        | OPENED CLOSED"""
        if len(p) == 3:
            p[0] = AST.Body([], p.lineno(1), p.lexpos(1))
        elif len(p) == 4:
            p[0] = AST.Body([p[2]], p.lineno(1), p.lexpos(1))
        else:
            p[0] = AST.Body([p[2], p[3]], p.lineno(1), p.lexpos(1))
    
    def p_CompStatement(self, p):
        """compStatement : stmt 
        | compStatement stmt"""
        if len(p) == 2:
            p[0] = AST.CompoundStatement([p[1]], p.lineno(1), p.lexpos(1))
        else:
            p[1].children.append(p[2])
            p[0] = p[1]

    def p_BodyStatement(self, p):
        """stmt : body"""
        p[0] = p[1]

    def p_NullStatement(self, p):
        """stmt : '.' """
        p[0] = AST.NullStatement([], p.lineno(1), p.lexpos(1))

    def p_AssignStatement(self, p):
        """stmt : expr BECAME expr terminator """
        p[0] = AST.AssignStatement([p[1], p[3]], p.lineno(2), p.lexpos(2))
    
    def p_PrintStatement(self, p):
        """stmt : expr SPOKE terminator
        | expr SAID ALICE terminator"""
        p[0] = AST.PrintStatement([p[1]], p.lineno(2), p.lexpos(2))

    def p_ReadStatement(self, p):
        """stmt : WHAT WAS expr '?'"""
        p[0] = AST.ReadStatement([p[3]], p.lineno(1), p.lexpos(1))

    def p_IncrementStatement(self, p):
        """stmt : expr ATE terminator """
        p[0] = AST.IncrementStatement([p[1]], p.lineno(2), p.lexpos(2))

    def p_DecrementStatement(self, p):
        """stmt : expr DRANK terminator"""
        p[0] = AST.DecrementStatement([p[1]], p.lineno(2), p.lexpos(2))

    def p_ReturnStatement(self, p):
        """stmt : ALICE FOUND  expr"""
        p[0] = AST.ReturnStatement([p[3]], p.lineno(1), p.lexpos(1))
    
    def p_CallStatement(self, p):
        """stmt : ID callParams terminator"""
        p[0] = AST.CallStatement([p[2]], p.lineno(1), p.lexpos(1), p[1])

    def p_LoopStatement(self, p):
        """stmt : EVENTUALLY '(' expr ')' BECAUSE compStatement ENOUGH TIMES"""
        p[0] = AST.LoopStatement([p[3],p[6]], p.lineno(1), p.lexpos(1)) 

    def p_IfStatement(self, p):
        """stmt : EITHER '(' expr ')' SO compStatement OR compStatement BECAUSE ALICE WAS UNSURE WHICH"""
        p[0] = AST.IfStatement([p[3], p[6], p[8]], p.lineno(2), p.lexpos(2))

    def p_IfStatement2(self, p):
        """stmt : condStatement BECAUSE ALICE WAS UNSURE WHICH
        | condStatement OR compStatement BECAUSE ALICE WAS UNSURE WHICH"""
        if len(p) == 7:
            p[0] = p[1]
        else:
            p[1].children.append(p[3])
            p[0] = p[1]

    def p_IfStatement3(self, p):
        """condStatement : PERHAPS '(' expr ')' SO compStatement
        | condStatement OR MAYBE '(' expr ')' SO compStatement"""
        if len(p) == 7:
            p[0] = AST.IfStatement([p[3], p[6]], p.lineno(2), p.lexpos(2))
        else:
            p[1].children += [p[5], p[8]]
            p[0] = p[1]

    def p_IntType(self, p):
        """type : NUMBER"""
        p[0] = AST.IntType([p[1]], p.lineno(1), p.lexpos(1))

    def p_CharType(self, p):
        """type : LETTER"""
        p[0] = AST.CharType([p[1]], p.lineno(1), p.lexpos(1))

    def p_StringType(self, p):
        """type : SENTENCE"""
        p[0] = AST.StringType([p[1]], p.lineno(1), p.lexpos(1))
    
    def p_RefType(self, p):
        """refType : SPIDER type"""
        p[0] = p[2]

    def p_terminator(self, p):
        """terminator : '.'
        | ','
        | AND
        | BUT
        | THEN"""
        pass
    
    def p_BinaryExpr(self, p):
        """expr : expr '+' expr
        | expr '-' expr
        | expr '*' expr
        | expr '/' expr
        | expr '%' expr
        | expr '|' expr
        | expr '&' expr
        | expr '^' expr
        | expr LOGICAL_OR expr
        | expr LOGICAL_AND expr
        | expr EQUAL expr
        | expr NOT_EQUAL expr
        | expr LESS_EQUAL expr
        | expr GREATER_EQUAL expr
        | expr LESS expr
        | expr GREATER expr"""
        p[0] = AST.BinaryExpr([p[1], p[3]], p.lineno(2), p.lexpos(2), p[2])

    def p_UnaryExpr(self, p):
        """expr : LOGICAL_NOT expr
        | '~' expr
        | '-' expr"""
        p[0] = AST.UnaryExpr([p[2]], p.lineno(1), p.lexpos(1), p[1])

    def p_VarExpr(self, p):
        """expr : ID"""
        p[0] = AST.VarExpr([], p.lineno(1), p.lexpos(1), p[1])

    def p_ArrExpr(self, p):
        """expr : ID APOSTROPHE S expr PIECE"""
        p[0] = AST.ArrExpr([p[4]], p.lineno(1), p.lexpos(1), p[1])

    def p_CallExpr(self, p):
        """expr : ID callParams """
        p[0] = AST.CallExpr([p[2]], p.lineno(1), p.lexpos(1), p[1])

    def p_ExprBrackets(self, p):
        """expr : '(' expr ')' """
        p[0] = p[2]

    def p_IntExpr(self, p):
        """expr : INT_LITERAL"""
        p[0] = AST.IntExpr([], p.lineno(1), p.lexpos(1), p[1])

    def p_CharExpr(self, p):
        """expr : CHAR_LITERAL"""
        p[0] = AST.CharExpr([], p.lineno(1), p.lexpos(1), p[1])

    def p_StringExpr(self, p):
        """expr : STRING_LITERAL"""
        p[0] = AST.StringExpr([], p.lineno(1), p.lexpos(1), p[1])

    def parse(self, Input):
        self.ast = self.parser.parse(Input, debug=0)
        self.errors += self.lexer.errors

        data = self.lexer.tokenize(Input)
        #for token in data:
        #   print str(token)
        #print ''
  
    def getAST(self):
        return self.ast

    def hasErrors(self):
        return len(self.errors) > 0    

    def __init__(self):
        Utils.Debug.__init__(self)
        self.lexer = Lexer.Lexer()
        self.parser = yacc.yacc(module=self)
        
