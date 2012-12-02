#!/bin/python
import Utils

class SymbolTable(Utils.ASTVisitor):
    def __init__(self):
        self.scopeStack = []
        self.table = {}        


    def check_CompilationUnit(self, node):
        pass


