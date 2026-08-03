"""Validação geral do Data Mentor AI sem dependências adicionais.

Execute a partir da raiz do projeto:
    python tests/validar_projeto.py
"""

from __future__ import annotations

import sys
import time
import unicodedata
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
PASTA_SRC = RAIZ / "src"

if str(PASTA_SRC) not in sys.path:
    sys.path.insert(0, str(PASTA_SRC))

from chatbot import ChatBot  # noqa: E402


CASOS = [
    # SQL
    ("SQL", "Qual a diferença entre INNER JOIN e LEFT JOIN?", "sql::join"),
    ("SQL", "Como calcular o total de compras por cliente?", "sql::join com group by"),
    ("SQL", "Como agrupar vendas por categoria?", "sql::group by"),

    # Python e Pandas
    ("Python", "Como ler um arquivo CSV com Pandas?", "python::ler arquivo csv"),
    ("Python", "Como tratar valores nulos em um DataFrame?", "python::valores ausentes"),
    ("Python", "Como agrupar vendas por categoria no Pandas?", "python::agrupar dados com pandas"),
    ("Python", "Como juntar dois DataFrames?", "python::juntar dataframes"),
    ("Python", "Como criar um gráfico de vendas em Python?", "python::visualização com matplotlib"),

    # Power BI e DAX
    ("Power BI", "Como criar uma medida de faturamento no Power BI?", "powerbi::sum"),
    ("Power BI", "Para que serve o CALCULATE?", "powerbi::calculate"),
    ("Power BI", "Como calcular o percentual do total em DAX?", "powerbi::percentual do total"),
    ("Power BI", "Qual a diferença entre medida e coluna calculada?", "powerbi::medidas e colunas calculadas"),
    ("Power BI", "Como comparar o faturamento com o ano anterior?", "powerbi::inteligência temporal"),

    # Excel
    ("Excel", "Como somar vendas usando vários critérios?", "excel::somases"),
    ("Excel", "Qual é a diferença entre PROCV e PROCX?", "excel::procv e procx"),
    ("Excel", "Como tratar erros em uma fórmula do Excel?", "excel::seerro"),
    ("Excel", "Como criar uma Tabela Dinâmica?", "excel::tabela dinâmica"),
    ("Excel", "Como usar Power Query no Excel?", "excel::power query no excel"),

    # Estatística
    ("Estatística", "Qual é a diferença entre média, mediana e moda?", "estatistica::média, mediana e moda"),
    ("Estatística", "Qual é a diferença entre variância e desvio padrão?", "estatistica::variância e desvio padrão"),
    ("Estatística", "Como identificar outliers usando o IQR?", "estatistica::outliers"),
    ("Estatística", "O que significa correlação?", "estatistica::correlação"),
    ("Estatística", "O que é uma distribuição normal?", "estatistica::distribuição normal"),
    ("Estatística", "O que significa o valor p?", "estatistica::valor p"),
    ("Estatística", "Qual é a diferença entre amostra e população?", "estatistica::amostra e população"),

    # Machine Learning
    ("Machine Learning", "Qual é a diferença entre classificação e regressão?", "machine_learning::classificação e regressão"),
    ("Machine Learning", "Como separar os dados entre treino e teste?", "machine_learning::separação entre treino e teste"),
    ("Machine Learning", "Qual é a diferença entre overfitting e underfitting?", "machine_learning::overfitting e underfitting"),
    ("Machine Learning", "Qual é a diferença entre precisão e recall?", "machine_learning::precisão e recall"),
    ("Machine Learning", "Como avaliar um modelo de classificação?", "machine_learning::métricas de classificação"),
    ("Machine Learning", "Quais métricas devo usar em um modelo de regressão?", "machine_learning::métricas de regressão"),
    ("Machine Learning", "O que é vazamento de dados?", "machine_learning::vazamento de dados"),
    ("Machine Learning", "Como criar um pipeline com Scikit-learn?", "machine_learning::pipeline"),
    ("Machine Learning", "O que fazer quando as classes estão desbalanceadas?", "machine_learning::classes desbalanceadas"),
    ("Machine Learning", "O que é clusterização?", "machine_learning::clusterização"),
]


def normalizar(texto: str | None) -> str:
    texto = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    ).strip()


def executar() -> int:
    print("=" * 72)
    print("VALIDAÇÃO GERAL — DATA MENTOR AI")
    print("=" * 72)
    print("Carregando o assistente. A primeira execução pode demorar...\n")

    inicio = time.perf_counter()
    bot = ChatBot(debug=False)
    aprovados = 0
    falhas: list[tuple[str, str, str, str]] = []

    for numero, (area, pergunta, esperado) in enumerate(CASOS, start=1):
        try:
            resposta = bot.responder(pergunta)
            diagnostico = bot.obter_diagnostico()
            obtido = diagnostico.get("chave") or ""
            resposta_valida = bool(str(resposta).strip())
            passou = normalizar(obtido) == normalizar(esperado) and resposta_valida
        except Exception as erro:  # exibe a falha e continua os demais testes
            obtido = f"ERRO: {erro}"
            passou = False

        status = "OK" if passou else "FALHOU"
        print(f"[{numero:02d}/{len(CASOS):02d}] {status:<6} | {area:<17} | {pergunta}")

        if passou:
            aprovados += 1
        else:
            falhas.append((area, pergunta, esperado, obtido))

    duracao = time.perf_counter() - inicio
    percentual = aprovados / len(CASOS) * 100

    print("\n" + "=" * 72)
    print(f"RESULTADO: {aprovados}/{len(CASOS)} testes aprovados ({percentual:.1f}%)")
    print(f"TEMPO: {duracao:.1f} segundos")
    print("=" * 72)

    if falhas:
        print("\nTESTES QUE PRECISAM DE AJUSTE:\n")
        for area, pergunta, esperado, obtido in falhas:
            print(f"Área:     {area}")
            print(f"Pergunta: {pergunta}")
            print(f"Esperado: {esperado}")
            print(f"Obtido:   {obtido}")
            print("-" * 72)
        return 1

    print("\nTodos os testes principais passaram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(executar())
