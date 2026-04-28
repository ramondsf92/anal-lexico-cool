from lexico.lex import tokens, lexer # type: ignore
import ply.yacc as yacc # type: ignore
import sys

def p_program(p):
    '''
    program :   class_list
    '''
    p[0] = ('program', p[1])



def p_class_list(p):
    '''
    class_list  :   class_list class
                |   class
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]



def p_class(p):
    '''
    class   :   CLASS TIPO INHERITS TIPO ABRE_CHAVES feature_list FECHA_CHAVES PONTOEVIRGULA
            |   CLASS TIPO ABRE_CHAVES feature_list FECHA_CHAVES PONTOEVIRGULA
    '''
    if len(p) == 9:
        p[0] = ('class', p[2], p[4], p[6])
    else:
        p[0] = ('class', p[2], None, p[4])



def p_feature_list(p):
    '''
    feature_list    :   feature_list feature
                    |   feature
                    |   epsilon
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_feature(p):
    '''
    feature :   ID ABRE_PARENTESE formal_list FECHA_PARENTESE DOISPONTOS TIPO ABRE_CHAVES expr FECHA_CHAVES PONTOEVIRGULA
            |   ID DOISPONTOS TIPO OP_ATRIBUICAO expr PONTOEVIRGULA
            |   ID DOISPONTOS TIPO PONTOEVIRGULA
    '''
    if len(p) == 11:
        p[0] = ('feature_com_argumentos', p[1], p[3], p[6], p[8])
    elif len(p) == 7:
        p[0] = ('feature_sem_argumentos', p[1], p[3], p[5])
    else:
        p[0] = ('feature_no_block', p[1], p[3])



def p_formal_list(p):
    '''
    formal_list :   formal_list VIRGULA formal
                |   formal
                |   epsilon
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_formal(p):
    '''
    formal  :   ID DOISPONTOS TIPO
    '''
    p[0] = (p[1], p[3])


######################################################################
# A partir daqui, as regras para expressões são feitas separadamente por conta de 
# legibilidade e facilidade de tratamento no posterior contexto semântico
######################################################################


def p_expr_list(p):
    '''
    expr_list   :   expr_list VIRGULA expr
                |   expr
                |   epsilon
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_expr_atribuicao(p):
    '''
    expr    :   ID OP_ATRIBUICAO expr
    '''
    p[0] = ('atribuicao', p[1], p[3])


def p_expr_arroba_metodo(p):
    '''
    expr    :   expr ARROBA TIPO PONTO ID ABRE_PARENTESE expr_list FECHA_PARENTESE
            |   expr PONTO ID ABRE_PARENTESE expr_list FECHA_PARENTESE
    '''
    if len(p) == 9:
        p[0] = ('expr_arroba_metodo', p[1], p[3], p[5], p[7])
    else:
        p[0] = ('expr_no_arroba_metodo', p[1], p[3], p[5])


def p_method(p):
    '''
    expr    :   ID ABRE_PARENTESE expr_list FECHA_PARENTESE
    '''
    p[0] = ('metodo', p[1], p[3])


def p_expr_if(p):
    '''
    expr    :   IF expr THEN expr ELSE expr FI
    '''
    p[0] = ('if', p[2], p[4], p[6])


def p_expr_while(p):
    '''
    expr    :   WHILE expr LOOP expr POOL
    '''
    p[0] = ('while', p[2], p[4])


def p_expr_bloco(p):
    '''
    expr    :   ABRE_CHAVES expr_block_list FECHA_CHAVES
    '''
    p[0] = ('bloco', p[2])

def p_expr_block_list(p):
    '''
    expr_block_list :   expr_block_list expr PONTOEVIRGULA
                    |   expr PONTOEVIRGULA
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_let_in(p):
    '''
    expr    :   LET ID DOISPONTOS TIPO OP_ATRIBUICAO expr expr_id_list IN expr
            |   LET ID DOISPONTOS TIPO expr_id_list IN expr
    '''
    if len(p) == 10:
        p[0] = ('let_in_declar', p[2], p[4], p[6], p[7], p[9])
    else:
        p[0] = ('let_in_no_declar', p[2], p[4], p[5], p[7])


def p_expr_id_list(p):
    '''
    expr_id_list    :   expr_id_list VIRGULA ID DOISPONTOS TIPO OP_ATRIBUICAO expr
                    |   expr_id_list VIRGULA ID DOISPONTOS TIPO
                    |   epsilon
    '''
    if len(p) == 8:
        p[0] = p[1] + [('id_list', p[3], p[5], p[7])]
    elif len(p) == 6 and p[1] is not None:
        p[0] = [('id_list', p[1], p[3], p[5])]
    else:
        p[0] = []


def p_expr_case_of(p):
    '''
    expr    :   CASE expr OF expr_case_list ESAC
    '''
    p[0] = ('case', p[2], p[4])


def p_expr_case_list(p):
    '''
    expr_case_list  :   expr_case_list ID DOISPONTOS TIPO SETA expr PONTOEVIRGULA
                    |   ID DOISPONTOS TIPO SETA expr PONTOEVIRGULA
    '''
    if len(p) == 8:
        p[0] = p[1] + [('case_item', p[2], p[4], p[6])]
    else:
        p[0] = [('case_item', p[1], p[3], p[5])]


def p_expr_new(p):
    '''
    expr    :   NEW TIPO
    '''
    p[0] = p[2]

def p_expr_isvoid(p):
    '''
    expr    :   ISVOID expr
    '''
    p[0] = p[2]

def p_expr_not(p):
    '''
    expr    :   NOT expr
    '''
    p[0] = p[2]

def p_expr_operacoes(p):
    '''
    expr    :   expr OP_MAIS expr
            |   expr OP_MENOS expr
            |   expr OP_MULT expr
            |   expr OP_DIV expr
            |   OP_NEGACAO expr
            |   expr OP_MENOR expr
            |   expr OP_MENORIGUAL expr
            |   expr OP_IGUAL expr
    '''
    if len(p) == 4:
        p[0] = ('op', p[2], p[1], p[3])
    else:
        p[0] = ('inverso', p[2])


def p_expr_parentese(p):
    '''
    expr    :   ABRE_PARENTESE expr FECHA_PARENTESE
    '''
    p[0] = p[2]


def p_expr_valores(p):
    '''
    expr    :   ID
            |   INTEIRO
            |   STRING
            |   TRUE
            |   FALSE
            |   REAL
    '''
    p[0] = p[1]


def p_epsilon(p):
    'epsilon :'
    pass

def p_error(p):
    if p:
        print(f'Erro sintático - Em "{p.value}" na linha {p.lineno}')
    else:
        print('Erro sintático Fim do Arquivo')

    return   

parser = yacc.yacc()

print(sys.argv)

if len(sys.argv) != 3 or sys.argv[1] != '-f':
     print("Formato incorreto. Comando: python -m sintatico.yacc -f file")
     quit()

try:
     arquivo = open(sys.argv[2], "r")
except FileNotFoundError:
    print('Erro: arquivo não encontrado. Reveja o nome do arquivo e se o arquivo está no mesmo diretório do programa.')
    quit()

result = parser.parse(arquivo.read(), lexer=lexer)

if result:
    print(result)
    print("Código sintaticamente correto!")

