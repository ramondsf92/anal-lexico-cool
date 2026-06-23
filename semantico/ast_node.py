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
    linha: int


# Features
######################################################
@dataclass
class Metodo(ASTNode):
    nome: str
    formais: list
    retorno: str
    linha: int
    corpo: Expr

@dataclass
class Atributo(ASTNode):
    nome: str
    tipo: str
    linha: int
    expr: Optional[Expr] = None


@dataclass
class Formal(ASTNode):
    nome: str
    tipo: str
    linha: int


# Expressões
#####################################################

@dataclass
class Atribuicao(ASTNode):
    nome: str
    expr: Expr
    linha: int

@dataclass
class If(ASTNode):
    condicao: Expr
    then_expr: Expr
    else_expr: Expr
    linha: int


@dataclass
class While(ASTNode):
    condicao: Expr
    corpo: Expr
    linha: int


@dataclass
class Bloco(ASTNode):
    exprs: list
    linha: int


# Let
###########################################################

@dataclass
class Let(Expr):
    declaracoes: list
    corpo: Expr
    linha: int


@dataclass
class LetDecl(ASTNode):
    nome: str
    tipo: str
    linha: int
    expr: Optional[Expr] = None


# Case
###########################################################

@dataclass
class Case(Expr):
    expr: Expr
    branches: list
    linha: int


@dataclass
class CaseBranch(ASTNode):
    nome: str
    tipo: str
    expr: Expr
    linha: int


# Dispatch
###########################################################

@dataclass
class Dispatch(Expr):
    expr: Expr
    metodo: str
    argumentos: list
    linha: int


@dataclass
class StaticDispatch(Expr):
    expr: Expr
    tipo: str
    metodo: str
    argumentos: list
    linha: int


@dataclass
class SelfDispatch(Expr):
    metodo: str
    argumentos: list
    linha: int


# Operações
###########################################################

@dataclass
class BinOp(Expr):
    op: str
    esquerdo: Expr
    direito: Expr
    linha: int


@dataclass
class UnaryOp(Expr):
    op: str
    expr: Expr
    linha: int


# Literais
###########################################################

@dataclass
class Integer(Expr):
    valor: int
    linha: int


@dataclass
class Real(Expr):
    valor: float
    linha: int


@dataclass
class String(Expr):
    valor: str
    linha: int


@dataclass
class Bool(Expr):
    valor: bool
    linha: int


@dataclass
class Identifier(Expr):
    nome: str
    linha: int


###########################################################
# OUTROS
###########################################################

@dataclass
class New(Expr):
    tipo: str
    linha: int


@dataclass
class IsVoid(Expr):
    expr: Expr
    linha: int

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