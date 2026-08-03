# Power BI e DAX

## O que é Power BI

Power BI é uma plataforma de Business Intelligence utilizada para conectar, transformar, modelar e visualizar dados.

Um projeto normalmente passa por quatro etapas:

1. Importar e transformar os dados no Power Query.
2. Criar relacionamentos no modelo de dados.
3. Construir medidas com DAX.
4. Criar relatórios e dashboards.

## Power Query

Power Query é utilizado para importar, limpar e transformar dados antes que eles sejam carregados no modelo.

Operações comuns:

- alterar tipos de dados;
- remover colunas e duplicados;
- substituir valores;
- tratar valores nulos;
- dividir e mesclar colunas;
- combinar arquivos;
- acrescentar ou mesclar consultas.

Exemplo em linguagem M:

```powerquery
Table.SelectRows(
    Vendas,
    each [Valor] > 1000
)
```

## Modelo de dados

O modelo de dados organiza tabelas e relacionamentos. Uma estrutura recomendada é o modelo estrela:

- tabelas dimensão: clientes, produtos, vendedores e calendário;
- tabela fato: vendas, pedidos ou movimentações;
- relacionamentos de um para muitos entre dimensões e fatos.

Um bom modelo reduz ambiguidades e facilita a criação de medidas.

## Relacionamentos

Relacionamentos permitem que filtros de uma tabela sejam aplicados em outra.

Exemplo:

```text
Clientes[IdCliente] 1 ─── * Vendas[IdCliente]
```

Recomendações:

- utilize chaves únicas nas tabelas dimensão;
- prefira direção de filtro única;
- evite relacionamentos muitos para muitos quando não forem necessários;
- mantenha uma tabela calendário para análises por data.

## Dashboards

Um dashboard apresenta indicadores importantes de maneira visual e objetiva.

Boas práticas:

- destaque os KPIs principais;
- use poucas cores e mantenha consistência;
- escolha o gráfico conforme o tipo de análise;
- evite excesso de informações;
- utilize filtros e segmentações úteis;
- apresente contexto, meta e comparação.

## Indicadores

Indicadores ou KPIs acompanham resultados importantes do negócio.

Exemplos:

- faturamento;
- quantidade de vendas;
- ticket médio;
- margem;
- crescimento percentual;
- atingimento de meta;
- clientes ativos.

## DAX

DAX é a linguagem utilizada para criar medidas, colunas calculadas e tabelas calculadas no Power BI.

Uma medida simples:

```dax
Faturamento =
SUM(Vendas[Valor])
```

DAX trabalha com o modelo de dados e responde aos filtros aplicados no relatório.

## Medidas

Medidas são cálculos avaliados conforme o contexto dos filtros do relatório.

```dax
Quantidade de Vendas =
COUNTROWS(Vendas)
```

Medidas são recomendadas para indicadores, totais, médias, percentuais e comparações.

## Colunas calculadas

Colunas calculadas são processadas linha por linha e ficam armazenadas no modelo.

```dax
Valor Total =
Vendas[Quantidade] * Vendas[PrecoUnitario]
```

Use colunas calculadas quando o resultado precisar existir em cada linha. Para agregações e indicadores, prefira medidas.

## Medidas e colunas calculadas

Medidas e colunas calculadas possuem comportamentos diferentes no Power BI:

- Medida: é calculada conforme os filtros do relatório, não fica armazenada linha por linha e é indicada para totais, médias, percentuais e indicadores.
- Coluna calculada: é processada para cada linha, fica armazenada no modelo e pode ser utilizada em eixos, filtros, segmentações e relacionamentos.

Na maioria dos indicadores, prefira uma medida. Use uma coluna calculada quando precisar de um valor persistente em cada registro.

## SUM

`SUM` soma os valores de uma coluna numérica.

```dax
Faturamento =
SUM(Vendas[Valor])
```

## AVERAGE

`AVERAGE` calcula a média dos valores de uma coluna.

```dax
Valor Médio =
AVERAGE(Vendas[Valor])
```

## COUNTROWS

`COUNTROWS` conta as linhas de uma tabela.

```dax
Quantidade de Pedidos =
COUNTROWS(Vendas)
```

Para contar clientes diferentes:

```dax
Clientes Ativos =
DISTINCTCOUNT(Vendas[IdCliente])
```

## CALCULATE

`CALCULATE` avalia uma expressão modificando o contexto de filtro.

```dax
Vendas São Paulo =
CALCULATE(
    [Faturamento],
    Clientes[Estado] = "SP"
)
```

Ele é uma das funções mais importantes de DAX e pode combinar medidas com filtros.

## FILTER

`FILTER` retorna uma tabela contendo somente as linhas que atendem a uma condição.

```dax
Vendas de Alto Valor =
CALCULATE(
    [Faturamento],
    FILTER(
        Vendas,
        Vendas[Valor] > 1000
    )
)
```

Use `FILTER` quando a condição precisar ser avaliada linha por linha ou for mais complexa.

## Contexto de filtro

O contexto de filtro é formado pelos filtros do relatório, pelas segmentações e pelos campos utilizados em um visual.

Por exemplo, a medida:

```dax
Faturamento =
SUM(Vendas[Valor])
```

mostra valores diferentes quando o relatório é filtrado por ano, produto, cliente ou região.

`CALCULATE` pode modificar esse contexto.

## DIVIDE

`DIVIDE` realiza divisões e trata denominadores iguais a zero.

```dax
Ticket Médio =
DIVIDE(
    [Faturamento],
    [Quantidade de Pedidos],
    0
)
```

É preferível a utilizar diretamente o operador `/` em medidas.

## Percentual do total

Para calcular a participação de cada categoria no total:

```dax
Percentual do Total =
DIVIDE(
    [Faturamento],
    CALCULATE(
        [Faturamento],
        ALL(Produtos[Categoria])
    )
)
```

`ALL` remove o filtro da categoria para obter o total geral.

## Tabela calendário

Uma tabela calendário é essencial para análises temporais.

```dax
Calendario =
ADDCOLUMNS(
    CALENDAR(
        MIN(Vendas[Data]),
        MAX(Vendas[Data])
    ),
    "Ano", YEAR([Date]),
    "Mes", MONTH([Date]),
    "Nome Mes", FORMAT([Date], "MMMM")
)
```

Depois, relacione `Calendario[Date]` com a coluna de data da tabela de vendas.

## Inteligência temporal

Funções de inteligência temporal permitem comparar períodos.

Vendas do ano anterior:

```dax
Faturamento Ano Anterior =
CALCULATE(
    [Faturamento],
    SAMEPERIODLASTYEAR(Calendario[Date])
)
```

Crescimento percentual:

```dax
Crescimento Percentual =
DIVIDE(
    [Faturamento] - [Faturamento Ano Anterior],
    [Faturamento Ano Anterior]
)
```

## Acumulado

Um acumulado soma os valores até a data atual do contexto.

```dax
Faturamento Acumulado =
CALCULATE(
    [Faturamento],
    FILTER(
        ALLSELECTED(Calendario[Date]),
        Calendario[Date] <= MAX(Calendario[Date])
    )
)
```

## Meta e atingimento

Uma medida pode comparar o resultado com uma meta.

```dax
Percentual da Meta =
DIVIDE(
    [Faturamento],
    [Meta de Faturamento],
    0
)
```

Também é possível criar uma classificação:

```dax
Status da Meta =
IF(
    [Percentual da Meta] >= 1,
    "Meta atingida",
    "Abaixo da meta"
)
```

## Publicação e atualização

Após criar o relatório no Power BI Desktop, ele pode ser publicado no Power BI Service.

No serviço online, é possível:

- compartilhar relatórios;
- criar dashboards;
- configurar atualização agendada;
- controlar acesso;
- criar espaços de trabalho;
- acompanhar métricas de uso.

Para fontes locais, pode ser necessário configurar um gateway de dados.