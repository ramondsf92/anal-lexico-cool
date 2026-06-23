from lexico.lex import tokens, lexer # type: ignore
import ply.yacc as yacc # type: ignore
import sys
from semantico.ast_node import *
from semantico.semantic import SemanticAnalyzer

global erro_sintatico
erro_sintatico = False

def p_program(p):
    '''
    program :   class_list
    '''
    #p[0] = ('program', p[1])
    p[0] = Program(p[1])


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
        p[0] = Classe(nome=p[2], pai=p[4], features=p[6],linha=p.lineno(1))
    else:
        p[0] = Classe(nome=p[2], pai=None, features=p[4],linha=p.lineno(1))



def p_feature_list(p):
    '''
    feature_list    :   feature_list feature
                    |   feature
                    |   epsilon
    '''
    if len(p) == 3 and p[1] is not None:
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
        #p[0] = ('feature_metodo', p[1], p[3], p[6], p[8])
        p[0] = Metodo(nome=p[1],formais=p[3],retorno=p[6],corpo=p[8], linha=p.lineno(1))
    elif len(p) == 7:
        p[0] = Atributo(nome=p[1],tipo=p[3],expr=p[5], linha=p.lineno(1))
    else:
        p[0] = Atributo(nome=p[1],tipo=p[3],expr=None, linha=p.lineno(1))


def p_feature_error(p):
    '''
    feature :   ID ABRE_PARENTESE error FECHA_PARENTESE DOISPONTOS TIPO ABRE_CHAVES expr FECHA_CHAVES PONTOEVIRGULA
            |   ID DOISPONTOS TIPO OP_ATRIBUICAO error PONTOEVIRGULA
    '''
    print(f'Erro em feature na linha {p.lineno(1)}.')



def p_formal_list(p):
    '''
    formal_list :   formal_list VIRGULA formal
                |   formal
                |   epsilon
    '''
    if len(p) == 4 and p[1] is not None:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_formal(p):
    '''
    formal  :   ID DOISPONTOS TIPO
    '''
    #p[0] = (p[1], p[3])
    p[0] = Formal(nome=p[1],tipo=p[3], linha=p.lineno(1))


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
    if len(p) == 4 and p[1] is not None:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_expr_list_error(p):
    '''
    expr_list   :   expr_list VIRGULA error
    '''
    print('Erro de expressão.')


def p_expr_atribuicao(p):
    '''
    expr    :   ID OP_ATRIBUICAO expr
    '''
    #p[0] = ('atribuicao', p[1], p[3])
    p[0] = Atribuicao(nome=p[1],expr=p[3], linha=p.lineno(1))


def p_expr_arroba_metodo(p):
    '''
    expr    :   expr ARROBA TIPO PONTO ID ABRE_PARENTESE expr_list FECHA_PARENTESE
            |   expr PONTO ID ABRE_PARENTESE expr_list FECHA_PARENTESE
    '''
    if len(p) == 9:
        #p[0] = ('expr_arroba_metodo', p[1], p[3], p[5], p[7])
        p[0] = StaticDispatch(expr=p[1],tipo=p[3],metodo=p[5],argumentos=p[7],linha=p.lineno(2))
    else:
        #p[0] = ('expr_no_arroba_metodo', p[1], p[3], p[5])
        p[0] = Dispatch(expr=p[1],metodo=p[3],argumentos=p[5],linha=p.lineno(2))


def p_method(p):
    '''
    expr    :   ID ABRE_PARENTESE expr_list FECHA_PARENTESE
    '''
    #p[0] = ('metodo', p[1], p[3])
    p[0] = SelfDispatch(metodo=p[1],argumentos=p[3],linha=p.lineno(1))


def p_method_error(p):
    '''
    expr    :   ID ABRE_PARENTESE error FECHA_PARENTESE
    '''
    print(f'Erro em no método {p[1]} na linha {p.lineno(4)}')


def p_expr_if(p):
    '''
    expr    :   IF expr THEN expr ELSE expr FI
    '''
    #p[0] = ('if', p[2], p[4], p[6])
    p[0] = If(condicao=p[2],then_expr=p[4],else_expr=p[6], linha=p.lineno(1))


def p_expr_while(p):
    '''
    expr    :   WHILE expr LOOP expr POOL
    '''
    #p[0] = ('while', p[2], p[4])
    p[0] = While(condicao=p[2],corpo=p[4], linha=p.lineno(1))

def p_expr_bloco(p):
    '''
    expr    :   ABRE_CHAVES expr_block_list FECHA_CHAVES
    '''
    #p[0] = ('bloco', p[2])
    p[0] = Bloco(exprs=p[2], linha=p.lineno(1))

def p_expr_block_list(p):
    '''
    expr_block_list :   expr_block_list expr PONTOEVIRGULA
                    |   expr PONTOEVIRGULA
    '''
    if len(p) == 4 and p[1] is not None:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_expr_block_list_error(p):
    '''
    expr_block_list :   expr_block_list error PONTOEVIRGULA
                    |   error PONTOEVIRGULA
    '''
    print(f'Erro no bloco da linha {p.lineno(2)}')


def p_let_in(p):
    '''
    expr    :   LET ID DOISPONTOS TIPO OP_ATRIBUICAO expr expr_id_list IN expr
            |   LET ID DOISPONTOS TIPO expr_id_list IN expr
    '''
    if len(p) == 10:
        #p[0] = ('let_in_declar', p[2], p[4], p[6], p[7], p[9])
        p[0] = Let(declaracoes=[LetDecl(nome=p[2],tipo=p[4],expr=p[6], linha=p.lineno(2))]+p[7],corpo=p[9], linha=p.lineno(1))
    else:
        #p[0] = ('let_in_no_declar', p[2], p[4], p[5], p[7])
        p[0] = Let(declaracoes=[LetDecl(nome=p[2],tipo=p[4],expr=None, linha=p.lineno(2))]+p[5],corpo=p[7], linha=p.lineno(1))


def p_expr_id_list(p):
    '''
    expr_id_list    :   expr_id_list VIRGULA ID DOISPONTOS TIPO OP_ATRIBUICAO expr
                    |   expr_id_list VIRGULA ID DOISPONTOS TIPO
                    |   epsilon
    '''
    if len(p) == 8 and p[1] is not None:
        #p[0] = p[1] + [('id_list', p[3], p[5], p[7])]
        p[0] = p[1] + [LetDecl(nome=p[3],tipo=p[5],expr=p[7], linha=p.lineno(3))]
    elif len(p) == 6 and p[1] is not None:
        p[0] = p[1] + [LetDecl(nome=p[3],tipo=p[5],expr=None, linha=p.lineno(3))]
    else:
        p[0] = []

def p_expr_id_list_error(p):
    '''
    expr_id_list    :   error VIRGULA ID DOISPONTOS TIPO OP_ATRIBUICAO expr
                    |   error VIRGULA ID DOISPONTOS TIPO
    '''
    print(f'Erro de expressão na linha {p.lineno(1)}')


def p_expr_case_of(p):
    '''
    expr    :   CASE expr OF expr_case_list ESAC
    '''
    #p[0] = ('case', p[2], p[4])
    p[0] = Case(expr=p[2],branches=p[4], linha=p.lineno(1))


def p_expr_case_list(p):
    '''
    expr_case_list  :   expr_case_list ID DOISPONTOS TIPO SETA expr PONTOEVIRGULA
                    |   ID DOISPONTOS TIPO SETA expr PONTOEVIRGULA
    '''
    if len(p) == 8:
        #p[0] = p[1] + [('case_item', p[2], p[4], p[6])]
        p[0] = p[1] + [CaseBranch(nome=p[2], tipo=p[4], expr=p[6], linha=p.lineno(4))]
    else:
        p[0] = [CaseBranch(nome=p[1], tipo=p[3], expr=p[5], linha=p.lineno(4))]


def p_expr_case_list_error(p):
    '''
    expr_case_list  :   expr_case_list ID DOISPONTOS TIPO SETA error PONTOEVIRGULA
    '''
    print(f'Erro no Case List na linha {p.lineno(7)}')


def p_expr_new(p):
    '''
    expr    :   NEW TIPO
    '''
    #p[0] = p[2]
    p[0] = New(tipo=p[2],linha=p.lineno(1))

def p_expr_isvoid(p):
    '''
    expr    :   ISVOID expr
    '''
    #p[0] = p[2]
    p[0] = IsVoid(expr=p[2],linha=p.lineno(1))

def p_expr_not(p):
    '''
    expr    :   NOT expr
    '''
    #p[0] = p[2]
    p[0] = UnaryOp(op='not',expr=p[2], linha=p.lineno(1))

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
        #p[0] = ('op', p[2], p[1], p[3])
        p[0] = BinOp(op=p[2],esquerdo=p[1],direito=p[3], linha=p.lineno(2))
    else:
        #p[0] = ('inverso', p[2])
        p[0] = UnaryOp(op='~',expr=p[2], linha=p.lineno(2))


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

    token_type = p.slice[1  ].type
    
    if token_type == 'ID':
        p[0] = Identifier(nome=p[1], linha=p.lineno(1))

    elif token_type == 'INTEIRO':
        p[0] = Integer(p[1], linha=p.lineno(1))

    elif token_type == 'REAL':
        p[0] = Real(p[1], linha=p.lineno(1))

    elif token_type == 'STRING':
        p[0] = String(p[1], linha=p.lineno(1))

    elif token_type == 'TRUE':
        p[0] = Bool(valor=True, linha=p.lineno(1))

    elif token_type == 'FALSE':
        p[0] = Bool(valor=False,linha=p.lineno(1))

    #p[0] = p[1]




def p_epsilon(p):
    'epsilon :'
    pass

def p_error(p):
    global erro_sintatico
    erro_sintatico = True
    if p:
        print(f'Erro sintático - Em "{p.value}" na linha {p.lineno}')
    else:
        print('Erro sintático Fim do Arquivo')

    return   

parser = yacc.yacc()

print(sys.argv)
# print(Program)

if len(sys.argv) != 3 or sys.argv[1] != '-f':
     print("Formato incorreto. Comando: python -m sintatico.yacc -f file")
     quit()

try:
     arquivo = open(sys.argv[2], "r")
except FileNotFoundError:
    print('Erro: arquivo não encontrado. Reveja o nome do arquivo e se o arquivo está no mesmo diretório do programa.')
    quit()

result = parser.parse(arquivo.read(), lexer=lexer)

if result and not erro_sintatico:
    # print(result)
    semantico = SemanticAnalyzer()
    semantico.visit(result)
    print("Código semanticamente correto!")

