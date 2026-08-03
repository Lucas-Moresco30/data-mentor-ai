# Machine Learning

## O que é Machine Learning

Machine Learning, ou aprendizado de máquina, é uma área da inteligência artificial que permite criar modelos capazes de aprender padrões a partir de dados.

Esses modelos podem classificar registros, prever valores, identificar grupos e detectar comportamentos incomuns.

## Aprendizado supervisionado

No aprendizado supervisionado, o modelo é treinado com exemplos que já possuem a resposta correta, chamada de variável-alvo.

Os principais problemas supervisionados são classificação e regressão.

## Aprendizado não supervisionado

No aprendizado não supervisionado, os dados não possuem uma resposta previamente informada.

O objetivo pode ser identificar grupos, padrões ou estruturas. Clusterização e redução de dimensionalidade são exemplos.

## Classificação

Classificação é utilizada quando a resposta que queremos prever representa uma categoria.

Exemplos:

- cliente vai cancelar ou permanecer;
- transação é fraude ou não fraude;
- mensagem é spam ou não spam.

```python
from sklearn.linear_model import LogisticRegression

modelo = LogisticRegression()
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)
```

## Regressão

Regressão é utilizada quando a resposta que queremos prever é um valor numérico contínuo.

Exemplos: preço de um imóvel, faturamento futuro e tempo de entrega.

```python
from sklearn.linear_model import LinearRegression

modelo = LinearRegression()
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)
```

## Classificação e regressão

Classificação prevê categorias, enquanto regressão prevê valores numéricos contínuos.

- Prever se um cliente cancelará: classificação.
- Prever quanto um cliente gastará: regressão.

A escolha depende do tipo da variável-alvo.

## Variáveis preditoras e variável-alvo

Variáveis preditoras, geralmente representadas por `X`, são as informações usadas pelo modelo para realizar uma previsão.

A variável-alvo, geralmente representada por `y`, é a resposta que desejamos prever.

```python
X = df[["idade", "renda", "tempo_cliente"]]
y = df["cancelou"]
```

## Separação entre treino e teste

Os dados de treino são usados para ajustar o modelo. Os dados de teste são reservados para avaliar seu desempenho em exemplos que não participaram do treinamento.

```python
from sklearn.model_selection import train_test_split

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

Não se deve avaliar o resultado final somente nos dados de treino.

## Pré-processamento

Pré-processamento prepara os dados antes do treinamento. Pode incluir tratamento de valores ausentes, codificação de categorias, padronização e seleção de variáveis.

O pré-processamento deve ser ajustado apenas com os dados de treino para evitar vazamento de dados.

## Padronização

Padronização transforma variáveis numéricas para que apresentem média próxima de zero e desvio padrão próximo de um.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_treino_escalado = scaler.fit_transform(X_treino)
X_teste_escalado = scaler.transform(X_teste)
```

Ela é especialmente importante para algoritmos sensíveis à escala, como KNN e regressão logística.

## Variáveis categóricas

Variáveis categóricas precisam ser convertidas em números para muitos algoritmos.

```python
dados = pd.get_dummies(
    df,
    columns=["estado", "categoria"],
    drop_first=True
)
```

Uma alternativa profissional é usar `OneHotEncoder` dentro de um pipeline.

## Pipeline

Pipeline reúne pré-processamento e modelo em uma única sequência. Isso reduz erros e evita aplicar transformações diferentes nos dados de treino e teste.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("escala", StandardScaler()),
    ("modelo", LogisticRegression())
])

pipeline.fit(X_treino, y_treino)
previsoes = pipeline.predict(X_teste)
```

## Overfitting

Overfitting ocorre quando o modelo aprende excessivamente os dados de treino, inclusive ruídos, mas apresenta desempenho ruim em novos dados.

Sinais comuns são desempenho muito alto no treino e significativamente menor no teste.

Para reduzir overfitting, é possível usar regularização, simplificar o modelo, obter mais dados ou realizar validação cruzada.

## Underfitting

Underfitting ocorre quando o modelo é simples demais para aprender os padrões dos dados.

Nesse caso, o desempenho costuma ser baixo tanto no treino quanto no teste. Pode ser necessário usar um modelo mais flexível, melhores variáveis ou treinamento adequado.

## Overfitting e underfitting

Overfitting representa aprendizado excessivo dos dados de treino. Underfitting representa aprendizado insuficiente.

- Overfitting: bom no treino e ruim no teste.
- Underfitting: ruim tanto no treino quanto no teste.

O objetivo é encontrar um equilíbrio que permita boa generalização.

## Acurácia

Acurácia é a proporção de previsões corretas em um problema de classificação.

```python
from sklearn.metrics import accuracy_score

acuracia = accuracy_score(y_teste, previsoes)
```

Ela pode ser enganosa quando as classes estão muito desbalanceadas.

## Precisão

Precisão responde: entre os registros previstos como positivos, quantos realmente eram positivos?

Ela é importante quando falsos positivos têm custo elevado.

```python
from sklearn.metrics import precision_score

precisao = precision_score(y_teste, previsoes)
```

## Recall

Recall, também chamado de sensibilidade, responde: entre todos os casos realmente positivos, quantos foram identificados pelo modelo?

Ele é importante quando deixar de identificar um caso positivo tem custo elevado.

```python
from sklearn.metrics import recall_score

recall = recall_score(y_teste, previsoes)
```

## Precisão e recall

Precisão avalia a confiabilidade das previsões positivas. Recall avalia a capacidade de encontrar os casos positivos existentes.

- Priorize precisão quando falsos positivos forem mais graves.
- Priorize recall quando falsos negativos forem mais graves.

## F1-score

F1-score é a média harmônica entre precisão e recall. Ele é útil quando se deseja equilibrar as duas métricas.

```python
from sklearn.metrics import f1_score

f1 = f1_score(y_teste, previsoes)
```

## Matriz de confusão

A matriz de confusão mostra acertos e erros de um modelo de classificação por meio de verdadeiros positivos, verdadeiros negativos, falsos positivos e falsos negativos.

```python
from sklearn.metrics import confusion_matrix

matriz = confusion_matrix(y_teste, previsoes)
print(matriz)
```

## Métricas de classificação

As principais métricas de classificação são acurácia, precisão, recall, F1-score e ROC-AUC.

A métrica adequada depende do objetivo do problema e do custo de cada tipo de erro.

```python
from sklearn.metrics import classification_report

print(classification_report(y_teste, previsoes))
```

## MAE

MAE é o erro absoluto médio entre os valores reais e previstos em uma regressão. Ele é expresso na mesma unidade da variável-alvo.

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_teste, previsoes)
```

## MSE e RMSE

MSE calcula a média dos erros elevados ao quadrado. RMSE é a raiz quadrada do MSE e volta à unidade original da variável-alvo.

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_teste, previsoes)
rmse = mean_squared_error(y_teste, previsoes) ** 0.5
```

Essas métricas penalizam erros grandes com maior intensidade.

## R²

R² indica a proporção da variação da variável-alvo explicada pelo modelo de regressão.

```python
from sklearn.metrics import r2_score

r2 = r2_score(y_teste, previsoes)
```

Um R² maior não garante que o modelo seja adequado; os resíduos e o contexto também devem ser avaliados.

## Métricas de regressão

As principais métricas de regressão são MAE, MSE, RMSE e R².

- MAE: erro médio fácil de interpretar.
- RMSE: penaliza mais os erros grandes.
- R²: mede a proporção da variação explicada.

## Validação cruzada

Validação cruzada divide os dados em várias partes e repete o treinamento e a avaliação. Isso produz uma estimativa mais estável do desempenho.

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    modelo,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print(scores.mean())
```

## Hiperparâmetros

Hiperparâmetros são configurações definidas antes do treinamento, como profundidade de uma árvore ou número de vizinhos no KNN.

Eles podem ser ajustados com técnicas como `GridSearchCV` e `RandomizedSearchCV`, utilizando validação cruzada.

## Vazamento de dados

Vazamento de dados ocorre quando informações que não deveriam estar disponíveis durante a previsão acabam sendo usadas no treinamento.

Isso gera resultados artificialmente altos. Para evitar vazamento, separe treino e teste antes de ajustar transformações e use pipelines.

## Classes desbalanceadas

Classes desbalanceadas ocorrem quando uma categoria possui muito mais exemplos que outra.

Nessa situação, avalie precisão, recall, F1-score e matriz de confusão, em vez de depender apenas da acurácia. Também podem ser usados pesos de classe e técnicas de reamostragem.

## Clusterização

Clusterização é uma técnica não supervisionada que agrupa registros semelhantes sem utilizar uma variável-alvo conhecida.

```python
from sklearn.cluster import KMeans

modelo = KMeans(n_clusters=3, random_state=42)
grupos = modelo.fit_predict(X)
```

O número e a interpretação dos grupos devem ser avaliados no contexto do problema.

## Projeto de Machine Learning

Um projeto de Machine Learning normalmente segue estas etapas:

1. definir o problema e a métrica;
2. coletar e compreender os dados;
3. preparar os dados;
4. separar treino e teste;
5. criar um modelo de referência;
6. treinar e avaliar modelos;
7. interpretar os resultados;
8. monitorar o modelo após a implantação.
