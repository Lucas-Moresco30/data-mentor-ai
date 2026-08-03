# Estatística

## O que é Estatística

Estatística é a área que reúne métodos para coletar, organizar, analisar e interpretar dados.

Ela ajuda a resumir informações, identificar padrões, comparar grupos e apoiar decisões baseadas em evidências.

## Média

A média aritmética é calculada somando todos os valores e dividindo o resultado pela quantidade de observações.

Exemplo:

```python
valores = [10, 20, 30, 40]
media = sum(valores) / len(valores)
print(media)  # 25.0
```

A média é sensível a valores extremos.

## Mediana

A mediana é o valor central de um conjunto de dados ordenado.

Quando existe uma quantidade par de valores, ela é a média dos dois valores centrais.

Exemplo:

```python
from statistics import median

valores = [10, 15, 20, 100]
print(median(valores))  # 17.5
```

A mediana é indicada quando existem valores extremos ou distribuições assimétricas.

## Moda

A moda é o valor que aparece com maior frequência.

Exemplo:

```python
from statistics import mode

valores = [1, 2, 2, 3, 4]
print(mode(valores))  # 2
```

Um conjunto pode não possuir moda ou pode possuir mais de uma moda.

## Média, mediana e moda

Média, mediana e moda são medidas de tendência central.

- Média: soma dos valores dividida pela quantidade de observações.
- Mediana: valor central após a ordenação dos dados.
- Moda: valor mais frequente.

Use a média em dados equilibrados, a mediana quando houver valores extremos e a moda para identificar o valor ou a categoria mais frequente.

## Variância

A variância mede quanto os valores se afastam da média. Quanto maior a variância, maior é a dispersão dos dados.

Exemplo:

```python
import numpy as np

valores = [10, 12, 14, 16]
variancia = np.var(valores, ddof=1)
print(variancia)
```

`ddof=1` calcula a variância amostral.

## Desvio padrão

O desvio padrão mede a dispersão dos valores na mesma unidade dos dados originais. Ele corresponde à raiz quadrada da variância.

Exemplo:

```python
import numpy as np

valores = [10, 12, 14, 16]
desvio = np.std(valores, ddof=1)
print(desvio)
```

Um desvio padrão pequeno indica valores mais próximos da média.

## Variância e desvio padrão

A variância e o desvio padrão medem a dispersão dos dados.

- Variância: utiliza unidades elevadas ao quadrado.
- Desvio padrão: utiliza a mesma unidade dos valores originais.

Por ser mais fácil de interpretar, o desvio padrão costuma ser mais usado na apresentação de resultados.

## Amostra e população

População é o conjunto completo que se deseja estudar. Amostra é uma parte dessa população utilizada na análise.

Exemplo: todos os clientes de uma empresa formam a população; 500 clientes selecionados para uma pesquisa formam uma amostra.

Uma boa amostra deve representar adequadamente a população.

## Quartis e percentis

Quartis dividem os dados ordenados em quatro partes. Percentis dividem os dados em cem partes.

- Q1: 25% dos valores estão abaixo dele.
- Q2: corresponde à mediana.
- Q3: 75% dos valores estão abaixo dele.

Exemplo:

```python
import numpy as np

valores = [10, 20, 30, 40, 50]
q1, q2, q3 = np.percentile(valores, [25, 50, 75])
```

## Outliers

Outliers são valores muito distantes do comportamento predominante dos dados.

Uma forma comum de identificá-los utiliza o intervalo interquartil, chamado IQR.

```python
q1 = df["valor"].quantile(0.25)
q3 = df["valor"].quantile(0.75)
iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = df[
    (df["valor"] < limite_inferior)
    | (df["valor"] > limite_superior)
]
```

Um outlier deve ser investigado antes de ser removido, pois pode representar erro ou informação importante.

## Correlação

Correlação mede a força e a direção da relação entre duas variáveis.

O coeficiente varia de -1 a 1:

- próximo de 1: relação positiva forte;
- próximo de -1: relação negativa forte;
- próximo de 0: pouca relação linear.

```python
correlacao = df["investimento"].corr(df["vendas"])
print(correlacao)
```

Correlação não significa causalidade.

## Covariância

Covariância indica se duas variáveis tendem a variar na mesma direção.

Uma covariância positiva indica movimento semelhante; uma negativa indica movimento em direções opostas. Diferentemente da correlação, sua escala depende das unidades das variáveis.

## Probabilidade

Probabilidade representa a chance de um evento acontecer e varia entre 0 e 1, ou entre 0% e 100%.

Para eventos igualmente prováveis:

```text
probabilidade = casos favoráveis / total de casos possíveis
```

Exemplo: a probabilidade de obter um número par em um dado comum é 3/6, ou 50%.

## Distribuição normal

A distribuição normal é uma distribuição simétrica em formato de sino, na qual média, mediana e moda ficam no centro.

Na distribuição normal, aproximadamente:

- 68% dos valores ficam até um desvio padrão da média;
- 95% ficam até dois desvios padrões;
- 99,7% ficam até três desvios padrões.

Nem todo conjunto de dados segue uma distribuição normal.

## Assimetria

Assimetria descreve a falta de simetria de uma distribuição.

- Assimetria positiva: cauda maior à direita.
- Assimetria negativa: cauda maior à esquerda.
- Assimetria próxima de zero: distribuição aproximadamente simétrica.

Em distribuições muito assimétricas, a mediana pode representar melhor o centro que a média.

## Erro padrão

O erro padrão estima quanto uma estatística amostral, como a média, varia entre diferentes amostras.

Ele diminui quando o tamanho da amostra aumenta.

```text
erro padrão = desvio padrão / raiz quadrada do tamanho da amostra
```

## Intervalo de confiança

O intervalo de confiança fornece uma faixa de valores plausíveis para um parâmetro da população.

Um intervalo de confiança de 95% não significa que há 95% de probabilidade de o parâmetro estar naquele intervalo específico. Ele descreve a confiabilidade do método utilizado em várias amostras.

## Teste de hipótese

Teste de hipótese é um procedimento para avaliar uma afirmação sobre uma população utilizando dados amostrais.

- Hipótese nula: representa a ausência de efeito ou diferença.
- Hipótese alternativa: representa o efeito ou a diferença investigada.

O resultado deve ser interpretado junto com o contexto e o tamanho do efeito.

## Valor p

O valor p mede quão compatíveis os dados observados são com a hipótese nula.

Um valor p pequeno indica evidência contra a hipótese nula, considerando as suposições do teste. Ele não mede a importância prática do resultado e não é a probabilidade de a hipótese nula ser verdadeira.

## Estatística descritiva

Estatística descritiva resume os dados observados por meio de tabelas, gráficos e medidas como média, mediana, frequência e desvio padrão.

Exemplo com Pandas:

```python
print(df.describe())
```

## Estatística inferencial

Estatística inferencial utiliza dados de uma amostra para produzir estimativas ou conclusões sobre uma população.

Intervalos de confiança, testes de hipótese e modelos estatísticos são exemplos de técnicas inferenciais.
