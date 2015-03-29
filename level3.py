# -----------------------------------------------------------------------------
# This is test code of markdown generating by ply
# -----------------------------------------------------------------------------
import sys

tokens = (
     'H1','H2','H3', 'CR', 'TEXT', 'U1', 'U2', 'S1', 'S2', 'DIV',
     'Parentheses', 'Bracket','CODE','SingleCR','LTB','RTB','NUM',
     'PLUS','POINT','SPACE','TAB','Exclamation','CODEBLOCK',)

# Tokens
t_H1 = r'\#'
t_H2 = r'\#\#'
t_H3 = r'\#\#\#'
t_S1 = r'\*'
t_U1 = r'\_'
t_S2 = r'\*\*'
t_U2 = r'\_\_'
t_TAB = r' \t'
t_SPACE = r'\ '
t_DIV = r'\*\ \*\ \*|\=\=\=|\-\-\-'
t_Parentheses = r'\(|\)'
t_Bracket = r'\[|\]'
t_CODEBLOCK = r'\`\`\`'
t_CODE = r'\`'
t_LTB = r'\<'
t_RTB = r'\>'
t_PLUS = r'\+'
t_POINT = r'\.'
t_Exclamation = r'\!'

def t_NUM(t):
    r'[0-9]+'
    t.value = str(t.value)
    return t

def t_TEXT(t):
	r'[a-zA-Z\'\,\/\:\"]+'
	t.value = str(t.value)
	return t


def t_CR(t):
    r'\n+\n'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_SingleCR(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

 # Build the lexer
import ply.lex as lex
lexer = lex.lex()

# ------------------------------------
# definitions of parsing rules by yacc
# ------------------------------------
precedence = ( ('left','U1','U2','S1','S2','CODE','LTB','RTB','Exclamation'),
    )
names = {}

def p_body(p):
    '''body : subBody
            | subBody CR'''
    print '<body>' + p[1] + '</body>'

def p_subBody(p):
    '''subBody : title
            | paragraph
            | div
            | ol0
            | ul0
            | quotaion
            | codeParagraph
            | subBody SingleCR title
            | subBody SingleCR paragraph
            | subBody SingleCR div
            | subBody SingleCR ol0
            | subBody SingleCR ul0
            | subBody SingleCR quotaion
            | subBody SingleCR codeParagraph
            | subBody CR title
            | subBody CR paragraph
            | subBody CR div
            | subBody CR ol0
            | subBody CR ul0
            | subBody CR quotaion
            | subBody CR codeParagraph
            | subBody SingleCR TAB'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])


def p_paragraph(p):
    '''paragraph : subParagraph''' 
    p[0] = '<p>' + str(p[1]) + '</p>'

def p_codeParagraph(p):
    '''codeParagraph : subCodeParagraph'''
    p[0] = '<pre>' + '<code>' + str(p[1]) + '</code>' + '</pre>'

def p_code_paragraph(p):
    '''subCodeParagraph : CODEBLOCK SingleCR subParagraph CR
                    | CODEBLOCK SingleCR subParagraph SingleCR
                    | CODEBLOCK CR subParagraph CR
                    | CODEBLOCK CR subParagraph SingleCR
                    | subCodeParagraph subParagraph CR
                    | subCodeParagraph subParagraph SingleCR
                    | subCodeParagraph CODEBLOCK'''
    if (len(p)==5):
        p[0] = str(p[2]) + str(p[3]) + str(p[4])
    if (len(p)==4):
        p[0] = str(p[1]) + str(p[2]) + str(p[3])
    if (len(p)==3):
        p[0] = str(p[1])

def p_title_cr(p):
    '''title : H1 subParagraph
                | H2 subParagraph
                | H3 subParagraph'''  

    if p[1] == '#':
        p[0] = '<h1>' + str(p[2]) + '</h1>'
    elif p[1] == '##':
        p[0] = '<h2>' + str(p[2]) + '</h2>'
    elif p[1] == '###': 
        p[0] = '<h3>' + str(p[2]) + '</h3>'
    

def p_quotation(p):
    'quotaion : subQuotation'
    p[0] = '<blockquote> <p>' + p[1] + '</p> </blockquote>'

def p_subQuotation(p):
    '''subQuotation : quotationItem
                | subQuotation SingleCR quotationItem'''
    if (len(p)==2):
        p[0] = str(p[1])
    else:
        p[0] = str(p[1]) + str(p[3])


def p_quotationItem(p):
    '''quotationItem : RTB SPACE subParagraph'''
    p[0] = str(p[3])


def p_ol0(p):
    '''ol0 : subOl0'''
    p[0] = '<ol>' + p[1] + '</ol>'

def p_ol1(p):
    '''ol1 : subOl1'''
    p[0] = '<ol>' + p[1] + '</ol>'

def p_ol2(p):
    '''ol2 : subOl2'''
    p[0] = '<ol>' + p[1] + '</ol>'


def p_ul0(p):
    '''ul0 : subUl0'''
    p[0] = '<ul>' + p[1] + '</ul>'

def p_ul1(p):
    '''ul1 : subUl1'''
    p[0] = '<ul>' + p[1] + '</ul>'

def p_ul2(p):
    '''ul2 : subUl2'''
    p[0] = '<ul>' + p[1] + '</ul>'

def p_subOl0(p):
    '''subOl0 : olItem0
                | subOl0 SingleCR olItem0
                | subOl0 SingleCR ol1
                | subOl0 SingleCR ul1'''

    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]

def p_subOl1(p):
    '''subOl1 : olItem1
                | subOl1 SingleCR olItem1
                | subOl1 SingleCR ol2
                | subOl1 SingleCR ul2'''

    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]


def p_subOl2(p):
    '''subOl2 : olItem2
                | subOl2 SingleCR olItem2'''

    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]

def p_subUl0(p):
    '''subUl0 : ulItem0
                | subUl0 SingleCR ulItem0
                | subUl0 SingleCR ul1
                | subUl0 SingleCR ol1'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]

def p_subUl1(p):
    '''subUl1 : ulItem1
                | subUl1 SingleCR ulItem1
                | subUl1 SingleCR ul2
                | subUl1 SingleCR ol2'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]

def p_subUl2(p):
    '''subUl2 : ulItem2
                | subUl2 SingleCR ulItem2'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p)==4):
        p[0] = p[1] + p[3]

def p_divide(p):
    '''div : DIV'''
    p[0] = '<hr>'



def p_marked_text(p):
    '''marked : S1 subParagraph S1
            | U1 subParagraph U1
            | S2 subParagraph S2
            | U2 subParagraph U2
            | CODE subParagraph CODE
            | Bracket subParagraph Bracket Parentheses subParagraph Parentheses
            | Exclamation Bracket subParagraph Bracket Parentheses subParagraph Parentheses
            | LTB subParagraph RTB'''
    
    if (p[1]=='*' and p[3]=='*'):
        p[0] = '<em>' + str(p[2]) + '</em>'

    elif (p[1]=='__' and p[3]=='__'):
        p[0] = '<strong>' + str(p[2]) + '</strong>'

    elif (p[1]=='_' and p[3]=='_'):
        p[0] = '<em>' + str(p[2]) + '</em>'

    elif (p[1]=='**' and p[3]=='**'):
        p[0] = '<strong>' + str(p[2]) + '</strong>'

    elif (p[1]=='`' and p[3]=='`'):
        p[0] = '<code>' + str(p[2]) + '</code>'

    elif (p[1]=='[' and p[3]==']' and p[4]=='(' and p[6]==')'):
        p[0] = '<a href="' + str(p[5]) + '">' + str(p[2]) + '</a>'

    elif (p[1]=='!' and p[2]=='[' and p[4]==']' and p[5]=='(' and p[7]==')'):
        p[0] = '<img src="' + str(p[6]) + '" alt="' + str(p[3]) + '">'

    elif (p[1]=='<' and p[3]=='>'):
        p[0] = '<a href="' + str(p[2]) + '">' + str(p[2]) + '</a>'



def p_olItem0(p):
    'olItem0 : NUM POINT SPACE subParagraph '
    p[0] = '<li>' + str(p[4]) + '</li>'

def p_olItem1(p):
    'olItem1 : TAB NUM POINT SPACE subParagraph '
    p[0] = '<li>' + str(p[5]) + '</li>'

def p_olItem2(p):
    'olItem2 : TAB TAB NUM POINT SPACE subParagraph '
    p[0] = '<li>' + str(p[6]) + '</li>'

def p_ulItem0(p):
    '''ulItem0 : PLUS SPACE subParagraph
                | S1 SPACE subParagraph'''
    p[0] = '<li>' + str(p[3]) + '</li>'

def p_ulItem1(p):
    '''ulItem1 : TAB PLUS SPACE subParagraph
                | TAB S1 SPACE subParagraph'''
    p[0] = '<li>' + str(p[4]) + '</li>'

def p_ulItem2(p):
    '''ulItem2 : TAB TAB PLUS SPACE subParagraph
                | TAB TAB S1 SPACE subParagraph'''
    p[0] = '<li>' + str(p[5]) + '</li>'



def p_subParagraph(p):
    '''subParagraph : TEXT 
            | NUM
            | POINT
            | SPACE
            | marked
            | subParagraph TEXT 
            | subParagraph NUM
            | subParagraph POINT
            | subParagraph SPACE
            | subParagraph marked'''
    
    if (len(p)==2):
        p[0] = p[1]
        
    elif(len(p)==3):
        p[0] = p[1] + p[2]


def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")


import ply.yacc as yacc
parser = yacc.yacc()

if __name__ == '__main__':
    filename = 'test03.md'
    yacc.parse(open(filename).read())


# lexer.input(open(filename).read())
# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     print tok


