# SQL

SQL (Structured Query Language) é a linguagem utilizada para consultar, manipular e analisar dados em bancos de dados relacionais.

---

## SELECT

O comando SELECT é utilizado para consultar dados de uma ou mais tabelas.

Exemplo:

```sql
SELECT nome, cidade
FROM clientes;
```

---

## WHERE

O comando WHERE é utilizado para filtrar registros de acordo com uma condição.

Exemplo:

```sql
SELECT nome, cidade
FROM clientes
WHERE cidade = 'Joaçaba';
```

---

## JOIN

O comando JOIN combina informações de duas ou mais tabelas utilizando uma coluna em comum.

Os principais tipos de JOIN são:

- INNER JOIN: retorna apenas os registros que possuem correspondência nas duas tabelas.
- LEFT JOIN: retorna todos os registros da tabela da esquerda e os correspondentes da direita. Quando não existe correspondência, os campos da direita recebem NULL.
- RIGHT JOIN: retorna todos os registros da tabela da direita e os correspondentes da esquerda. Quando não existe correspondência, os campos da esquerda recebem NULL.
- FULL JOIN: retorna todos os registros das duas tabelas, mesmo quando não existe correspondência.

---

### INNER JOIN

Exemplo:

```sql
SELECT
    clientes.nome,
    pedidos.valor
FROM clientes
INNER JOIN pedidos
    ON clientes.id = pedidos.cliente_id;
```

---

### LEFT JOIN

Exemplo:

```sql
SELECT
    clientes.nome,
    pedidos.valor
FROM clientes
LEFT JOIN pedidos
    ON clientes.id = pedidos.cliente_id;
```

---

### RIGHT JOIN

Exemplo:

```sql
SELECT
    clientes.nome,
    pedidos.valor
FROM clientes
RIGHT JOIN pedidos
    ON clientes.id = pedidos.cliente_id;
```

---

### FULL JOIN

Exemplo:

```sql
SELECT
    clientes.nome,
    pedidos.valor
FROM clientes
FULL JOIN pedidos
    ON clientes.id = pedidos.cliente_id;
```

---

## GROUP BY

GROUP BY agrupa registros iguais para permitir cálculos como soma, média, quantidade e máximo.

Exemplo:

```sql
SELECT
    cidade,
    COUNT(*) AS total_clientes
FROM clientes
GROUP BY cidade;
```

---

## ORDER BY

ORDER BY organiza o resultado de uma consulta em ordem crescente ou decrescente.

Exemplo:

```sql
SELECT
    nome,
    salario
FROM funcionarios
ORDER BY salario DESC;
```

---

## HAVING

HAVING filtra grupos criados pelo GROUP BY.

Exemplo:

```sql
SELECT
    cidade,
    COUNT(*) AS total_clientes
FROM clientes
GROUP BY cidade
HAVING COUNT(*) > 10;
```

---

## Funções de Agregação

As funções de agregação realizam cálculos sobre um conjunto de registros.

Principais funções:

- COUNT(): conta registros.
- SUM(): soma valores.
- AVG(): calcula a média.
- MAX(): retorna o maior valor.
- MIN(): retorna o menor valor.

Exemplo:

```sql
SELECT
    SUM(valor) AS faturamento
FROM pedidos;
```

---

## JOIN com GROUP BY

JOIN pode ser combinado com GROUP BY para gerar relatórios.

Exemplo:

```sql
SELECT
    clientes.nome,
    SUM(pedidos.valor) AS total_compras
FROM clientes
INNER JOIN pedidos
    ON clientes.id = pedidos.cliente_id
GROUP BY clientes.nome
ORDER BY total_compras DESC;
```

Nesse exemplo:

- INNER JOIN relaciona clientes e pedidos.
- SUM calcula o total das compras.
- GROUP BY agrupa os resultados por cliente.
- ORDER BY organiza o resultado do maior para o menor valor.

---

## JOIN com WHERE

É comum utilizar JOIN junto com WHERE para filtrar registros.

Exemplo:

```sql
SELECT
    clientes.nome,
    pedidos.valor
FROM clientes
INNER JOIN pedidos
    ON clientes.id = pedidos.cliente_id
WHERE pedidos.valor > 500;
```

---

## JOIN com GROUP BY e HAVING

Também é possível combinar vários comandos em uma única consulta.

Exemplo:

```sql
SELECT
    clientes.nome,
    SUM(pedidos.valor) AS total
FROM clientes
INNER JOIN pedidos
    ON clientes.id = pedidos.cliente_id
GROUP BY clientes.nome
HAVING SUM(pedidos.valor) > 1000
ORDER BY total DESC;
```