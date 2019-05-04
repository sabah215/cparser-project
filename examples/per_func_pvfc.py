from __future__ import print_function
import sys


# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_ast, parse_file, c_parser

class RecordArguments(c_ast.NodeVisitor):
    def __init__(self):
        self.vars = []

    def visit_Decl(self, node):
        self.vars.append(node.name)


def get_arguments(node):
    rec = RecordArguments()
    rec.visit(node)
    return rec.vars


class FunctionParameter(c_ast.NodeVisitor):
    def __init__(self, inc): pass
      #  self.inc = []
      #  self.incVal = inc

    def visit_FuncDef(self, node):

        print('\n'+'Function name is %s  ' % (node.decl.name))
        print('Parameters: %s' % get_arguments(node.decl.type))

        # self.visit(node.body)
        #
        print('Function calls: %s' % get_funcCalls(node.body, True))
        print('Variables: %s' % get_arguments(node.body))


    def visit_For(self,node):

        self.visit(node.stmt)
        print('Function calls within For Loop: %s' % get_funcCalls(node.stmt, True))
        self.visit(node.next)
        print('Loop increment: %s' % get_increment(node.next))

    def visit_While(self,node):

        self.visit(node.stmt)
        print('Function calls within While Loop: %s' % get_funcCalls(node.stmt, True))

#class FuncCallsFor



    #Loops(c_ast.NodeVisitor):

    def visit_For(self, node):pass

    def visit_While(self, node): pass

class FunctionCalls(c_ast.NodeVisitor):

    def __init__(self, toplevel):
        self.funcCalls = []
        self.toplevel = toplevel

    def visit_FuncCall(self, node):

        self.funcCalls.append(node.name.name)
        self.visit(node.args)

    # toplevel is true then the FuncCall
    # visitor does not traverse each node of the body

    # def visit_For(self,node):pass
    #
    # def visit_While(self,node):pass

def get_funcCalls(node, toplevel):
    funcCalls = FunctionCalls(toplevel)
    funcCalls.visit(node)
    # Suppose this node is an assignment
    # funcCalls.visit(node) -> NodeVisitor.visit(node) -> FunctionCalls.visit_assignment->NodeVisitor.visit_assignment
    # For each child of node -> funcCalls.visit(child)
    return funcCalls.funcCalls


def get_increment(node):
    increment = FunctionParameter(node)
    increment.visit(node)
    return increment.incVal

def get_ast(filename):
    # Note that cpp is used. Provide a path to your own cpp or
    # make sure one exists in PATH.
    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-IC:/Users/Sabah/PycharmProjects/pycparser-master/utils/fake_libc_include')

    # print(ast)
    p = FunctionParameter(ast)
    p.visit(ast)
    f = FuncCallsForLoops(ast)
    f.visit(ast)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        filename = 'C:/Users/Sabah/PycharmProjects/pycparser-master/examples/c_files/hash.c'

get_ast(filename)



