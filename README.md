# anal-lexico-cool

## Descrição
Implementação de Analisador Léxico para a linguagem Cool para a disciplina de Compiladores do 
Curso de Ciência da Computação - UFF Rio das Ostras. A implementação foi realizada utilizando a 
linguagem Python e a ferramenta PLY, que simula a ferramenta lex/yacc.

## Execução
Para executar o programa, deve ser executado o comando:

`python lexico-cool.py -f file`

A flag `-f` deve ser seguida com o nome do arquivo de texto com o código no qual o programa fará 
a leitura para geração dos tokens.

Exemplo: `python lexico-cool.py -f newComplex.cl`

Na execução do arquivo `lexico-cool.py` será feita a leitura do arquivo 
`newComplex.cl` e a saída será a impressão dos Tokens que são encontrados no código no formato de 
objeto `LexToken` com o tipo do Token, o valor dele, o número da linha onde ele foi encontrado e 
a posição absoluta.
