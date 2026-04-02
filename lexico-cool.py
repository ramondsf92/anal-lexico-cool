import ply.lex as lex # type: ignore

# Lista de classificadores de Tokens
tokens = ['RESERVADO', 'ID', 'TIPO', 'INTEIRO', 'STRING', 'REAL', 'OP_ATRIBUICAO', 'OP_MENORIGUAL',
        'OP_MENOR', 'OP_IGUAL', 'OP_NEGACAO', 'OP_MAIS', 'OP_MENOS', 
        'OP_MULT', 'OP_DIV', 'PONTO', 'DOISPONTOS', 'PONTOEVIRGULA', 'VIRGULA', 
        'ABRE_PARENTESE', 'FECHA_PARENTESE', 'ABRE_CHAVES', 'FECHA_CHAVES']

# Lista de palavras reservadas
reservada = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
    'isvoid': 'ISVOID',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Adicionando os classificadores de token reservados na lista de tokens
tokens = tokens + list(reservada.values())

# Regras para o PLY - Simbolos
t_OP_ATRIBUICAO = r'<-'
t_OP_MENORIGUAL = r'<='
t_OP_MENOR = r'<'
t_OP_IGUAL = r'='
t_OP_NEGACAO = r'~'
t_OP_MAIS = r'\+'
t_OP_MENOS = r'-'
t_OP_MULT = r'\*'
t_OP_DIV = r'/'
t_PONTO = r'\.'
t_DOISPONTOS = r':'
t_PONTOEVIRGULA = r';'
t_VIRGULA = r','
t_ABRE_PARENTESE = r'\('
t_FECHA_PARENTESE = r'\)'
t_ABRE_CHAVES = r'\{'
t_FECHA_CHAVES = r'\}'

t_ignore = ' \t\r'

# Funções

## Comentário
def t_COMMENT_LINE(t):
    r'--.*\n+'
    pass

## Bloco de comentário - regex \(\*([^*]|)
def t_COMMENT_BLOCK(t):
    r'\(\*([^*]|\*+[^*)])*\*+\)'
    pass

## Deteccao de nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

## Erro
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

## String
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value
    return t

## Real
def t_REAL(t):
    r'(0|[1-9][0-9]*)\.[0-9]+'
    t.value = float(t.value)
    return t

## Inteiro
def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

## Tratar ID e palavras reservadas
def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value in list(reservada.keys()):
        t.type = reservada[t.value]
    else:
        t.type = 'ID'

    return t

## Tratar TIPO
def t_TIPO(t):
    r'[A-Z][a-zA-Z0-9_]*'
    t.value = t.value
    return t



# Inicializando o Lexer
lexer = lex.lex()


# Alguns Cool para serem abertos somente para teste. Arquivos .cl devem estar no mesmo diretório do arquivo lexico-cool.py
arquivo = open('helloWorld2.cl', "r")
# arquivo = open('newComplex.cl', "r")
# arquivo = open('primes.cl', "r")

lexer.input(arquivo.read())

for token in lexer:
    print(token)




    