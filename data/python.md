# Python para Análise de Dados

## O que é Python

Python é uma linguagem de programação conhecida pela sintaxe simples e pela grande quantidade de bibliotecas para automação, análise de dados, inteligência artificial e desenvolvimento de aplicações.

```python
mensagem = "Olá, Data Mentor!"
print(mensagem)
```

## Variáveis

Variáveis armazenam valores que podem ser utilizados durante a execução do programa.

```python
nome = "Lucas"
idade = 34
salario = 3500.50
esta_estudando = True
```

Os tipos mais comuns são `str`, `int`, `float` e `bool`.

## Listas

Listas armazenam vários valores em uma única variável.

```python
vendas = [1200, 850, 1430, 990]

print(vendas[0])
print(sum(vendas))
print(len(vendas))
```

## Dicionários

Dicionários armazenam informações no formato chave e valor.

```python
cliente = {
    "nome": "Ana",
    "cidade": "Joaçaba",
    "total_compras": 2500
}

print(cliente["nome"])
```

## Condições

As estruturas `if`, `elif` e `else` permitem executar ações conforme uma condição.

```python
meta = 10000
faturamento = 12500

if faturamento >= meta:
    print("Meta atingida")
else:
    print("Meta não atingida")
```

## Loops

Loops repetem uma operação. O `for` é utilizado para percorrer coleções.

```python
vendas = [1200, 850, 1430]

for valor in vendas:
    print(valor)
```

O `while` repete uma ação enquanto uma condição for verdadeira.

```python
contador = 1

while contador <= 3:
    print(contador)
    contador += 1
```

## Funções

Funções organizam e reutilizam blocos de código.

```python
def calcular_media(valores):
    return sum(valores) / len(valores)

media = calcular_media([10, 8, 9])
print(media)
```

## Tratamento de erros

O bloco `try` e `except` permite tratar erros sem encerrar o programa inesperadamente.

```python
try:
    numero = int(input("Digite um número: "))
    print(100 / numero)
except ValueError:
    print("Digite um número válido.")
except ZeroDivisionError:
    print("Não é possível dividir por zero.")
```

## Bibliotecas

Bibliotecas adicionam funcionalidades ao Python. Na análise de dados, as mais utilizadas incluem:

- Pandas: manipulação de tabelas e arquivos.
- NumPy: cálculos numéricos.
- Matplotlib e Seaborn: visualização de dados.
- Scikit-learn: modelos de Machine Learning.

```python
import pandas as pd
import numpy as np
```

## Pandas

Pandas é uma biblioteca utilizada para carregar, limpar, transformar e analisar dados tabulares.

```python
import pandas as pd

dados = {
    "produto": ["A", "B", "C"],
    "vendas": [1200, 850, 1430]
}

df = pd.DataFrame(dados)
print(df)
```

## Ler arquivo CSV

A função `read_csv` carrega um arquivo CSV em um DataFrame.

```python
import pandas as pd

df = pd.read_csv("vendas.csv")
print(df.head())
```

Para arquivos separados por ponto e vírgula:

```python
df = pd.read_csv("vendas.csv", sep=";")
```

## Explorar um DataFrame

Alguns comandos ajudam a conhecer os dados antes da análise.

```python
print(df.head())
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
print(df.describe())
```

## Selecionar colunas

Uma coluna pode ser selecionada pelo nome.

```python
nomes = df["nome"]
```

Para selecionar várias colunas:

```python
resultado = df[["nome", "cidade", "total_compras"]]
```

## Filtrar dados

Filtros retornam somente as linhas que atendem a uma condição.

```python
clientes_sp = df[df["estado"] == "SP"]
```

Também é possível combinar condições:

```python
resultado = df[
    (df["estado"] == "SP") &
    (df["total_compras"] > 1000)
]
```

## Valores ausentes

Valores ausentes podem ser identificados com `isna`.

```python
print(df.isna().sum())
```

Para preencher valores ausentes:

```python
df["idade"] = df["idade"].fillna(df["idade"].median())
```

Para remover linhas com valores ausentes:

```python
df = df.dropna()
```

## Remover duplicados

O método `drop_duplicates` remove registros repetidos.

```python
df = df.drop_duplicates()
```

É possível considerar apenas algumas colunas:

```python
df = df.drop_duplicates(subset=["id_cliente"])
```

## Criar colunas

Novas colunas podem ser calculadas a partir de colunas existentes.

```python
df["faturamento"] = df["quantidade"] * df["preco"]
```

Também é possível criar classificações condicionais:

```python
df["atingiu_meta"] = df["faturamento"] >= df["meta"]
```

## Agrupar dados com Pandas

O método `groupby` agrupa registros e permite aplicar cálculos.

```python
vendas_por_categoria = (
    df.groupby("categoria", as_index=False)["valor"]
      .sum()
      .rename(columns={"valor": "total_vendas"})
)
```

Para calcular vários indicadores:

```python
resumo = df.groupby("categoria")["valor"].agg(
    total="sum",
    media="mean",
    quantidade="count"
)
```

## Juntar DataFrames

O método `merge` combina DataFrames por uma coluna em comum, de forma semelhante ao JOIN do SQL.

```python
resultado = clientes.merge(
    pedidos,
    on="id_cliente",
    how="left"
)
```

Os valores mais comuns de `how` são `inner`, `left`, `right` e `outer`.

## Ordenar dados

O método `sort_values` ordena os registros.

```python
df = df.sort_values(
    by="faturamento",
    ascending=False
)
```

## Trabalhar com datas

Datas devem ser convertidas para o tipo `datetime`.

```python
df["data_venda"] = pd.to_datetime(
    df["data_venda"],
    dayfirst=True
)

df["ano"] = df["data_venda"].dt.year
df["mes"] = df["data_venda"].dt.month
```

## Exportar resultados

Um DataFrame pode ser exportado para CSV ou Excel.

```python
df.to_csv("resultado.csv", index=False)
df.to_excel("resultado.xlsx", index=False)
```

## NumPy

NumPy fornece estruturas e funções eficientes para cálculos numéricos.

```python
import numpy as np

valores = np.array([10, 15, 20, 25])

print(np.mean(valores))
print(np.median(valores))
print(np.std(valores))
```

## Visualização com Matplotlib

Matplotlib permite criar gráficos em Python.

```python
import matplotlib.pyplot as plt

categorias = ["A", "B", "C"]
vendas = [1200, 850, 1430]

plt.bar(categorias, vendas)
plt.title("Vendas por categoria")
plt.xlabel("Categoria")
plt.ylabel("Vendas")
plt.show()
```

## Projeto de análise de dados

Um fluxo básico de análise pode seguir estas etapas:

1. Carregar os dados.
2. Conhecer as colunas e os tipos.
3. Tratar valores ausentes e duplicados.
4. Criar métricas e agrupamentos.
5. Produzir gráficos.
6. Exportar ou apresentar os resultados.

```python
import pandas as pd

df = pd.read_csv("vendas.csv")
df = df.drop_duplicates()
df["data"] = pd.to_datetime(df["data"])

resumo = (
    df.groupby("categoria", as_index=False)["valor"]
      .sum()
      .sort_values("valor", ascending=False)
)

print(resumo)
```
