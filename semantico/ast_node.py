from dataclasses import dataclass
from typing import Optional, Any

# Criando os nodes da AST com classes ao invés de tuplas

class ASTNode:
    pass


class Expr(ASTNode):
    pass


# Programa e Classes
#######################################################

@dataclass
class Program(ASTNode):
    classes: list

@dataclass
class Classe(ASTNode):
    nome: str
    pai: Optional[str]
    features: list


# Features
######################################################
@dataclass
class Metodo(ASTNode):
    nome: str
    formais: list
    retorno: str
    corpo: Expr

@dataclass
class Atributo(ASTNode):
    nome: str
    tipo: str
    expr: Optional[Expr] = None


@dataclass
class Formal(ASTNode):
    nome: str
    tipo: str


# Expressões
#####################################################

@dataclass
class Atribuicao(ASTNode):
    nome: str
    expr: Expr

@dataclass
class If(ASTNode):
    condicao: Expr
    then_expr: Expr
    else_expr: Expr


@dataclass
class While(ASTNode):
    condicao: Expr
    corpo: Expr


@dataclass
class Bloco(ASTNode):
    exprs: list


# Let
###########################################################

@dataclass
class Let(Expr):
    declaracoes: list
    corpo: Expr


@dataclass
class LetDecl(ASTNode):
    nome: str
    tipo: str
    expr: Optional[Expr] = None


# Case
###########################################################

@dataclass
class Case(Expr):
    expr: Expr
    branches: list


@dataclass
class CaseBranch(ASTNode):
    nome: str
    tipo: str
    expr: Expr


# Dispatch
###########################################################

@dataclass
class Dispatch(Expr):
    expr: Expr
    metodo: str
    argumentos: list


@dataclass
class StaticDispatch(Expr):
    expr: Expr
    tipo: str
    metodo: str
    argumentos: list


@dataclass
class SelfDispatch(Expr):
    metodo: str
    argumentos: list


# Operações
###########################################################

@dataclass
class BinOp(Expr):
    op: str
    esquerdo: Expr
    direito: Expr


@dataclass
class UnaryOp(Expr):
    op: str
    expr: Expr


# Literais
###########################################################

@dataclass
class Integer(Expr):
    valor: int


@dataclass
class Real(Expr):
    valor: float


@dataclass
class String(Expr):
    valor: str


@dataclass
class Bool(Expr):
    valor: bool


@dataclass
class Identifier(Expr):
    nome: str


###########################################################
# OUTROS
###########################################################

@dataclass
class New(Expr):
    tipo: str


@dataclass
class IsVoid(Expr):
    expr: Expr

# class Program:
#     def __init__(self, classes):
#         self.classes = classes

#     def __repr__(self):
#         return f'Program({self.classes})'
    

# class Classe:
#     def __init__(self, nome, pai, features):
#         self.nome = nome
#         self.pai = pai
#         self.features = features

#     def __repr__(self):
#         return f'Classe({self.nome})'
    

# class Method:
#     def __init__(self, nome, formais, retorno, corpo):
#         self.nome = nome
#         self.formais = formais
#         self.retorno = retorno
#         self.corpo = corpo

#     def __repr__(self):
#         return f'Method({self.nome})'