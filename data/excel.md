# Excel para Análise de Dados

## O que é Excel

Excel é uma ferramenta utilizada para organizar, calcular, analisar e visualizar dados em planilhas.

Na análise de dados, ele pode ser utilizado para:

- importar e limpar informações;
- criar fórmulas e indicadores;
- resumir dados com Tabelas Dinâmicas;
- produzir gráficos e dashboards;
- automatizar transformações com Power Query.

## Tabelas

Transformar um intervalo em tabela facilita filtros, fórmulas e atualizações.

Atalho:

text
Ctrl + T


As tabelas utilizam referências estruturadas:

excel
=SOMA(Vendas[Valor])


## Fórmulas

Fórmulas começam com o sinal de igual.

excel
=A2+B2


Referência relativa:

excel
=A2*B2


Referência absoluta:

excel
=A2*$F$1


O símbolo `$` mantém a referência fixa ao copiar a fórmula.

## SE

A função `SE` retorna um resultado conforme uma condição.

excel
=SE(B2>=1000;"Meta atingida";"Abaixo da meta")


Ela possui três partes: condição, resultado verdadeiro e resultado falso.

## SEERRO

`SEERRO` substitui mensagens de erro por um resultado definido.

excel
=SEERRO(A2/B2;0)


Também pode ser combinada com funções de busca:

excel
=SEERRO(PROCX(A2;Produtos[ID];Produtos[Nome]);"Não encontrado")


## SOMASE

`SOMASE` soma valores que atendem a um critério.

excel
=SOMASE(A2:A100;"Sul";B2:B100)


Nesse exemplo, a fórmula soma os valores da coluna B quando a região da coluna A é Sul.

## SOMASES

`SOMASES` soma valores utilizando vários critérios.

excel
=SOMASES(
    Vendas[Valor];
    Vendas[Região];"Sul";
    Vendas[Ano];2026
)


A primeira coluna é o intervalo da soma. Depois são informados os intervalos e critérios.

## CONT.SE

`CONT.SE` conta células que atendem a um critério.

excel
=CONT.SE(Clientes[Estado];"SC")


## CONT.SES

`CONT.SES` conta registros utilizando vários critérios.

excel
=CONT.SES(
    Vendas[Região];"Sul";
    Vendas[Valor];">1000"
)


## MÉDIASE

`MÉDIASE` calcula a média dos valores que atendem a um critério.

excel
=MÉDIASE(Vendas[Categoria];"Eletrônicos";Vendas[Valor])


## PROCV

`PROCV` procura um valor na primeira coluna de uma tabela e retorna uma coluna à direita.

excel
=PROCV(A2;Produtos!A:D;3;FALSO)


Limitações:

- busca somente da esquerda para a direita;
- depende do número da coluna;
- pode quebrar quando colunas são inseridas.

## PROCX

`PROCX` é uma alternativa moderna e mais flexível ao `PROCV`.

excel
=PROCX(
    A2;
    Produtos[ID];
    Produtos[Nome];
    "Não encontrado"
)


Ela permite buscas em qualquer direção e possui tratamento para valores não encontrados.

## PROCV e PROCX

As duas funções realizam buscas, mas possuem diferenças importantes:

- PROCV: busca somente para a direita, utiliza um número para indicar a coluna e está disponível em versões antigas do Excel.
- PROCX: busca em qualquer direção, utiliza intervalos explícitos e permite definir o resultado quando o valor não é encontrado.

Em versões recentes do Excel, prefira `PROCX` quando estiver disponível.

## ÍNDICE e CORRESP

`ÍNDICE` retorna um valor de uma posição, enquanto `CORRESP` encontra a posição de um item.

excel
=ÍNDICE(
    Produtos[Nome];
    CORRESP(A2;Produtos[ID];0)
)


Essa combinação é flexível e funciona em versões que não possuem `PROCX`.

## Funções de texto

Funções de texto ajudam a limpar e combinar informações.

Remover espaços excedentes:

excel
=ARRUMAR(A2)


Converter para maiúsculas:

excel
=MAIÚSCULA(A2)


Unir textos:

excel
=TEXTO.JUNTAR(" ";VERDADEIRO;A2;B2)


Extrair caracteres:

excel
=ESQUERDA(A2;3)


## Funções de data

Excel armazena datas como números e permite realizar cálculos.

Data atual:

excel
=HOJE()


Extrair ano e mês:

excel
=ANO(A2)
=MÊS(A2)


Calcular diferença em dias:

excel
=B2-A2


## FILTRO

A função `FILTRO` retorna registros que atendem a uma condição.

excel
=FILTRO(
    Vendas;
    Vendas[Região]="Sul";
    "Nenhum resultado"
)


Ela está disponível em versões com matrizes dinâmicas.

## ÚNICO

`ÚNICO` retorna valores sem repetição.

excel
=ÚNICO(Clientes[Cidade])


Pode ser combinado com `CLASSIFICAR`:

excel
=CLASSIFICAR(ÚNICO(Clientes[Cidade]))


## Formatação condicional

Formatação condicional destaca valores conforme regras.

Exemplos:

- vendas abaixo da meta em vermelho;
- maiores valores com barras de dados;
- registros duplicados;
- datas vencidas;
- escala de cores para desempenho.

Ela altera a aparência, mas não modifica os valores.

## Validação de dados

Validação de dados controla o que pode ser digitado em uma célula.

É possível criar:

- listas suspensas;
- limites para números;
- intervalos de datas;
- mensagens de orientação;
- alertas para entradas inválidas.

## Tabela Dinâmica

Tabela Dinâmica resume grandes volumes de dados sem exigir fórmulas complexas.

Exemplo de configuração:

text
Linhas: Categoria
Colunas: Ano
Valores: Soma de Faturamento
Filtros: Região


Boas práticas:

- organize a origem em formato de tabela;
- evite linhas e colunas vazias;
- use cabeçalhos únicos;
- atualize a Tabela Dinâmica quando a origem mudar.

## Segmentação de dados

Segmentações são filtros visuais para tabelas e Tabelas Dinâmicas.

Elas podem filtrar campos como:

- região;
- vendedor;
- categoria;
- ano;
- status.

Para datas, também é possível utilizar uma linha do tempo.

## Gráficos

Escolha o gráfico conforme o objetivo:

- colunas ou barras: comparar categorias;
- linhas: analisar evolução no tempo;
- pizza ou rosca: mostrar poucas participações;
- dispersão: avaliar relação entre variáveis;
- combinado: comparar valores e percentuais.

Evite excesso de cores, efeitos tridimensionais e informações desnecessárias.

## Dashboard

Um dashboard no Excel pode reunir:

- cartões de indicadores;
- Tabelas Dinâmicas;
- gráficos;
- segmentações;
- comparação com metas;
- informações do período analisado.

Mantenha o layout limpo e destaque as informações mais importantes.

## Power Query no Excel

Power Query permite importar e transformar dados de maneira repetível.

Ele pode:

- combinar vários arquivos de uma pasta;
- remover colunas e duplicados;
- substituir valores;
- dividir e mesclar colunas;
- alterar tipos de dados;
- agrupar registros;
- mesclar consultas.

Depois de configurar as etapas, basta atualizar a consulta quando novos dados forem adicionados.

## Indicadores no Excel

Exemplos de indicadores:

Faturamento total:

excel
=SOMA(Vendas[Valor])


Quantidade de vendas:

excel
=CONT.NÚM(Vendas[IDVenda])


Ticket médio:

excel
=SEERRO(
    SOMA(Vendas[Valor])/CONT.NÚM(Vendas[IDVenda]);
    0
)


Atingimento da meta:

excel
=SEERRO(Faturamento/Meta;0)

