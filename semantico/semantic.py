from semantico.ast_node import *


class TypeEnvironment:

    def __init__(self):

        self.classes = {}


class SemanticAnalyzer:
    def __init__(self):
        self.scope = Scope()
        self.type_env = TypeEnvironment()

        self.current_class = None
        self.current_method = None

    def collect_classes(self, program):

        for classe in program.classes:

            self.type_env.classes[classe.nome] = {
                "parent": classe.pai or "Object",
                "attributes": {},
                "methods": {}
            }

            for feature in classe.features:

                if isinstance(feature, Atributo):

                    self.type_env.classes[classe.nome][
                        "attributes"
                    ][feature.nome] = feature.tipo

                elif isinstance(feature, Metodo):

                    self.type_env.classes[classe.nome][
                        "methods"
                    ][feature.nome] = {

                        "params": feature.formais,
                        "return": feature.retorno
                    }

    def generic_visit(self, node):
        raise Exception(f'Nenhum visit para {type(node).__name__}')

    def visit(self, node):

        # print(f'AAAAAAAAAA  {type(node)}, {node}')
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def visit_Integer(self, node):
        return "Int"
    
    def visit_String(self, node):
        return "String"
    
    def visit_Bool(self, node):
        return "Bool"
    
    def visit_Identifier(self, node):

        tipo = self.scope.lookup(node.nome)

        if tipo is None:
            raise Exception(f'Variável "{node.nome}" não declarada')

        return tipo
    

    def visit_Let(self, node):

        novo_escopo = Scope(self.scope)
        escopo_anterior = self.scope
        self.scope = novo_escopo

        for declaracao in node.declaracoes:

            if declaracao.expr:

                tipo_expr = self.visit(declaracao.expr)

                if tipo_expr != declaracao.tipo:

                    raise Exception(
                        f'Tipo incompatível: '
                        f'{tipo_expr} != {declaracao.tipo}'
                    )

            self.scope.define(
                declaracao.nome,
                declaracao.tipo
            )

        tipo_corpo = self.visit(node.corpo)
        self.scope = escopo_anterior
        return tipo_corpo
        
    
    def visit_BinOp(self, node):

        tipo_esq = self.visit(node.esquerdo)
        tipo_dir = self.visit(node.direito)

        if node.op in ['+', '-', '*', '/']:

            if tipo_esq != "Int" or tipo_dir != "Int":
                raise Exception(
                    'Operações aritméticas precisam ter termos que sejam Int'
                )

            return "Int"
    
    def visit_Program(self, node):

        self.collect_classes(node)

        for classe in node.classes:
            self.visit(classe)

    def visit_Classe(self, node):

        self.current_class = node.nome
        escopo_anterior = self.scope
        self.scope = Scope(self.scope)
        classe_info = self.type_env.classes[node.nome]

        for nome, tipo in classe_info["attributes"].items():
            self.scope.define(nome, tipo)

        for feature in node.features:
            self.visit(feature)

        self.scope = escopo_anterior


    def visit_Metodo(self, node):
        escopo_anterior = self.scope

        self.scope = Scope(self.scope)
        # self.visit(node.corpo)

        for formal in node.formais:

            self.scope.define(
                formal.nome,
                formal.tipo
            )
        
        tipo_corpo = self.visit(node.corpo)
        
        if tipo_corpo != node.retorno:

            raise Exception(
                f'Método {node.nome} retorna '
                f'{tipo_corpo} mas deveria retornar '
                f'{node.retorno}'
            )

        self.scope = escopo_anterior    
        

    def visit_Atributo(self, node):

        if node.expr:
            tipo_expr = self.visit(node.expr)

            if tipo_expr != node.tipo:
                raise Exception(
                    f'Tipo incompatível no atributo {node.nome}'
                )


#Tabela de escopos
class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def define(self, name, typex):
        self.symbols[name] = typex

    # Ele percorre o escopo de dentro pra fora buscando a variável
    def lookup(self, name):

        scope = self

        while scope:

            if name in scope.symbols:
                return scope.symbols[name]

            scope = scope.parent

        return None
    
