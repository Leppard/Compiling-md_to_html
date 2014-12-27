# -----------------------------------------------------------------------------
# @author Leppard
# This is not the template code of markdown generating by ply
# @update 2014-12-27
# -----------------------------------------------------------------------------
import sys

tokens = (
    'H1','H2','H3', 'CR', 'TEXT', 'STAR', 'DSTAR', 'NEWPAR'   
    )

# Tokens
t_H1 = r'\#'
t_H2 = r'\#\#'
t_H3 = r'\#\#\#'
t_STAR = r'\*'
t_DSTAR = r'\*\*' 

def t_TEXT(t):
    r'[_a-zA-Z0-9\,\.\-\'\=\_]+'
    t.value = str(t.value)
    return t

t_ignore = " \t"

def t_NEWPAR(t):
    r'\n\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_CR(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# ------------------------------------
# definitions of parsing rules by yacc
# ------------------------------------
precedence = (
    )
names = {}

def p_body(p):
    '''body : statement'''
    print '<body>' + p[1] + '</body>'

def p_state_newpar(p):
    '''statement : paragraph
            | statement NEWPAR paragraph'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])

def p_state(p):
    '''paragraph : expression
                | title
                | paragraph CR expression'''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])

def p_exp_par(p):
    '''expression : factor'''
    p[0] = '<p>' + str(p[1]) + '</p>'

def p_exp_title(p): 
    '''title : H1 factor
            | H2 factor
            | H3 factor'''
    if p[1] == '#':
        p[0] = '<h1>' + str(p[2]) + '</h1>'
    elif p[1] == '##':
        p[0] = '<h2>' + str(p[2]) + '</h2>'
    elif p[1] == '###': 
        p[0] = '<h3>' + str(p[2]) + '</h3>'



def p_factor_text(p):
    '''factor : TEXT
            | factor TEXT'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = str(p[1]) + ' ' + str(p[2])

def p_factor_em(p):
    '''factor : STAR TEXT STAR'''
    p[0] = '<em>' + str(p[2]) + '</em>'

def p_factor_stg(p):
    '''factor : DSTAR TEXT DSTAR'''
    p[0] = '<strong>' + str(p[2]) + '</strong>'


def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    filename = 'test01.md'
    yacc.parse(open(filename).read())
