from __future__ import print_function
import sys
import numpy as np
import matplotlib.pyplot as plt


# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_ast, parse_file, c_parser

class FuncDefVisitor(c_ast.NodeVisitor):

   def __init__(self):
       self.allFuncDef = []
       self.callsFromFunc = []
       self.paramsOfFunc = []
       self.vars = []
       self.f_or = []
       self.i_f = []
       self.w_hile = []


   def visit_FuncDef(self, node):

        """ Prints the name of functions defined"""
        funcname = node.decl.name
        if funcname not in self.allFuncDef:
            self.allFuncDef.append(funcname)


        """Gets the function calls within each functions"""
        calls = FuncCallVisitor()
        calls.visit(node.body)
        if calls.funcCalls not in self.callsFromFunc:
            self.callsFromFunc.append(len(calls.funcCalls))

        """node.decl.type is the declaration of parameters.
           Decl under the Paramlist node is the name of 
           the parameter of the function. So to get the paramaeters
           of a function we use the visit_Decl() function"""

        param_decls = DeclVisior()
        param_decls.visit(node.decl.type)


        if param_decls.declName not in self.paramsOfFunc:
            self.paramsOfFunc.append(len(param_decls.declName))

        """Creates a CompoundVisitor"""
        vars = CompoundVisitor()
        vars.visit(node.body)

        if vars.vars not in self.vars:
            self.vars.append(len(vars.vars))

        """Creates a ForVisitor"""
        f_or = ForLoopVisitor()
        f_or.visit(node.body)
        self.f_or.append(len(f_or.f))

        """Creates a IfVisitor"""
        i_f = IfVisitor()
        i_f.visit(node.body)
        self.i_f.append(len(i_f.i))

        """Creates a IfVisitor"""
        w_hile = WhileVisitor()
        w_hile.visit(node.body)
        self.w_hile.append(len(w_hile.w_hile))


        node.body.show()


class DeclVisior(c_ast.NodeVisitor):

    def __init__(self):
        self.declName = []

    def visit_Decl(self, node):
        self.declName.append(node.name)

class FuncCallVisitor(c_ast.NodeVisitor):

    def __init__(self):
        self.funcCalls = []

    def visit_FuncCall(self, node):
        """ node.name.name name of the functions called.
            node.name only prints [ID(name='free')]"""
        f = node.name.name

        """checks if function is called more than once"""
        if f not in self.funcCalls:
            self.funcCalls.append(f)

class CompoundVisitor(c_ast.NodeVisitor):

    def __init__(self):
        self.vars = []

    def visit_Compound(self, node):
        d = DeclVisior()
        d.visit(node)
        self.vars.append(d.declName)

class ForLoopVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.f = []
    def visit_For(self, node):
        c = node.coord
        self.f.append(c)

class IfVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.i = []

    def visit_If(self, node):
        i = node.coord
        self.i.append(i)

class WhileVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.w_hile = []

    def visit_While(self, node):
        w = node.coord
        self.w_hile.append(w)

if __name__ == '__main__':
    if(len(sys.argv)>1):
        filename = sys.argv[1]
    else:
        filename = 'C:/Users/Sabah/PycharmProjects/pycparser-master/examples/c_files/hash.c'

    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-IC:/Users/Sabah/PycharmProjects/pycparser-master/utils/fake_libc_include')

    funcDef = FuncDefVisitor()
    funcDef.visit(ast)

    allFunc = funcDef.allFuncDef
    callsfromFunc = funcDef.callsFromFunc
    paramsOfFunc = funcDef.paramsOfFunc
    variables = funcDef.vars
    f_or = funcDef.f_or
    i_f = funcDef.i_f
    w_hile = funcDef.w_hile

    # Plotting Data
    x_pos = np.arange(len(allFunc))

    # Create bars
    plt.figure(2)
    plt.bar(x_pos-0.3, f_or, width=0.2, color='blue', label="For Loops")
    plt.bar(x_pos+0.1, i_f, width=0.2, color='orange', label="If Statements")
    plt.bar(x_pos-0.1, w_hile, width=0.2, color='red', label="while Statements")


    # Create names on the x-axis
    plt.xticks(x_pos, allFunc)

    # Prints the label and title
    plt.title('AST Nodes for each function')
    plt.ylabel('Counts', fontsize=12, color='red')
    plt.xlabel('Functions', fontsize=12, color='blue')
    plt.legend()

    # Create bars
    plt.figure(1)
    plt.bar(x_pos, callsfromFunc, width=0.3, color='blue', label="Functions Called")
    plt.bar(x_pos - 0.3, paramsOfFunc, width=0.3, color='orange', label="Parameters")
    plt.bar(x_pos + 0.3, variables, width=0.3, color='red', label="Variables")

    # Create names on the x-axis
    plt.xticks(x_pos, allFunc)

    # Prints the label and title
    plt.title('AST Nodes for each function')
    plt.ylabel('Counts', fontsize=12, color='red')
    plt.xlabel('Functions', fontsize=12, color='blue')
    plt.legend()

  # Display graph
  #   plt.show()
  #   plt.show()
