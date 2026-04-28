# anal-lexico-cool

## Descrição
Implementação de Analisador Léxico e Analisador Sintático para a linguagem Cool para a disciplina de Compiladores do 
Curso de Ciência da Computação - UFF Rio das Ostras. A implementação foi realizada utilizando a 
linguagem Python e a ferramenta PLY, que simula a ferramenta lex/yacc.

## Execução
Para executar o programa, deve ser executado o comando __no diretório raiz__:

`python -m sintatico.yacc -f file`

A flag `-f` deve ser seguida com o nome do arquivo de texto com o código no qual o programa fará 
a leitura para geração dos tokens.

Exemplo: `python -m sintatico.yacc -f newComplex.cl`

Na execução do arquivo `yacc.py` será feita a leitura do arquivo `newComplex.cl` e a saída será a árvore sintática abstrata gerada pelo parser usando como referência os Tokens que são encontrados no código no formato de objeto `LexToken` no arquivo `lex.py`, junto a uma mensagem de validação, se o código estiver sintaticamente correto. Se existir algum erro de sintaxe no código, a saída será a indicação da cadeia de caracteres que causa o erro de sintaxe e a linha onde se encontra.
