# --------------------------------------------------------------------
#
#   CS 3180 Comparative Languages
#   Small Project 03
#   by Thomas Platt
#
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.  Modified by Erik M. Buck
# Further modified by Thomas Platt for Small Project 3 
# --------------------------------------------------------------------

## For iteration
from itertools import chain, imap
import math

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

######################################################################
# Scanner generation
tokens = ('NUM', )
literals = ['+','*', '(',')']

# Tokens
def t_NUM(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    t.value = float(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

######################################################################
# Parser generation and parse tree creator
##;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
## Sample BNF Grammar for expressions
##
## <expr> ::= <term> ADD <expr>
## | <term>
##
## <term> ::= <factor> MULTIPLY <term>
## | <factor>
##
## <factor> ::= LPAREN <expr> RPAREN
## | NUM
##;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

class Node:
   def __init__(self):
      self.children = []
      self.text = "invalid"
      self.function = lambda node: node.text

   def interp(self):
      """ Interprets the parse tree rooted at self """
      return self.function(self)

   def hasChildren(self):
       if not self.children:
           return False
       else:
           return True

## Iterator for Parse tree
   def __iter__(self):
       "implement the iterator protocol"
       for v in chain(*imap(iter, self.children)):
           yield v
       yield self.text

def p_expr_a(p):
    'expr : term "+" expr'
    p[0] = Node() # Return a Node instance
    p[0].text = "+"
    p[0].children = [p[1], p[3]]
    p[0].function = lambda node: node.children[0].interp() + node.children[1].interp()

def p_expr_b(p):
    'expr : term'
    p[0] = p[1] # Return a Node instance (p[1] is already a Node)
   
def p_factor_a(p):
    '''factor : "(" expr ")"'''
    p[0] = p[2] # Return a Node instance (p[2] is already a Node)
    
def p_factor_b(p):
    '''factor : NUM'''
    p[0] = Node() # Return a Node instance
    p[0].text = str(p[1])
    tmp = p[1]
    p[0].function = lambda node: tmp

def p_term_a(p):
    '''term : factor '*' term '''
    p[0] = Node() # Return a Node instance
    p[0].text = "*"
    p[0].children = [p[1], p[3]]
    p[0].function = lambda node: node.children[0].interp() * node.children[1].interp()


def p_term_b(p):
    '''term : factor'''
    p[0] = p[1] # Return a Node instance (p[1] is already a Node)

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at end of input")

import ply.yacc as yacc
yacc.yacc()

######################################################################
# Test driver
#
#   Iterator through tree to produce output representing the
#   pre-order traversal of the parse tree.
#
######################################################################
while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    resultNode = yacc.parse(s+'\n') # parse returns None upon error
    if None != resultNode:
       treeString = ""
       for i in list(iter(resultNode)):
           treeString += str(i) + " "
       print treeString
       print "Result: " + str(resultNode.interp())
