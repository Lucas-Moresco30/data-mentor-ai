import re
import unicodedata


class RelevancyBooster:
    REGRAS = {
        "sql::join": [
            "join", "juntar", "unir", "combinar", "relacionar", "cruzar",
            "duas tabelas", "coluna em comum", "clientes e pedidos",
        ],
        "sql::group by": [
            "group by", "agrupar", "agrupamento", "por categoria",
            "por vendedor", "por setor",
        ],
        "sql::join com group by": [
            "total por cliente", "compras por cliente", "somar por",
            "quantidade por", "juntar e agrupar",
        ],
        "sql::join com group by e having": [
            "having", "filtrar grupos", "depois de agrupar", "total acima",
        ],
        "sql::where": ["where", "filtrar", "condicao", "aplicar filtro"],
        "sql::select": ["select", "selecionar", "listar", "consultar"],
        "sql::order by": ["order by", "ordenar", "ordem crescente", "decrescente"],
        "sql::funções de agregação": [
            "sum", "avg", "count", "max", "min", "media", "soma", "contar",
        ],
        "estatistica::média": ["media", "valor medio"],
        "estatistica::mediana": ["mediana", "valor central"],
        "estatistica::moda": ["moda", "mais frequente"],
        "powerbi::dax": ["dax", "medida", "formula"],
        "powerbi::dashboards": ["dashboard", "painel", "visualizacao"],
        "powerbi::power query": [
            "power query", "transformar dados", "limpar dados", "linguagem m"
        ],
        "powerbi::modelo de dados": [
            "modelo de dados", "modelo estrela", "tabela fato", "dimensao"
        ],
        "powerbi::relacionamentos": [
            "relacionamento", "relacionamentos", "cardinalidade", "um para muitos"
        ],
        "powerbi::indicadores": [
            "indicador", "indicadores", "kpi", "meta", "desempenho"
        ],
        "powerbi::medidas": [
            "medida", "medidas", "criar medida", "calculo dax"
        ],
        "powerbi::colunas calculadas": [
            "coluna calculada", "colunas calculadas", "linha por linha"
        ],
        "powerbi::medidas e colunas calculadas": [
            "medida e coluna calculada", "medidas e colunas calculadas",
            "diferenca entre medida", "comparar medida"
        ],
        "powerbi::sum": ["sum", "somar", "soma", "faturamento"],
        "powerbi::average": ["average", "media", "valor medio"],
        "powerbi::countrows": [
            "countrows", "contar linhas", "quantidade de pedidos"
        ],
        "powerbi::calculate": [
            "calculate", "modificar filtro", "calcular com filtro"
        ],
        "powerbi::filter": [
            "filter", "filtrar tabela", "filtro complexo"
        ],
        "powerbi::contexto de filtro": [
            "contexto de filtro", "filtros do relatorio", "segmentacao"
        ],
        "powerbi::divide": [
            "divide", "divisao", "ticket medio"
        ],
        "powerbi::percentual do total": [
            "percentual do total", "participacao", "all"
        ],
        "powerbi::tabela calendário": [
            "tabela calendario", "calendario", "calendar"
        ],
        "powerbi::inteligência temporal": [
            "inteligencia temporal", "ano anterior", "sameperiodlastyear",
            "crescimento percentual"
        ],
        "powerbi::acumulado": [
            "acumulado", "total acumulado", "allselected"
        ],
        "powerbi::meta e atingimento": [
            "meta", "atingimento", "meta atingida"
        ],
        "machine_learning::classificação": ["classificacao", "classificar", "classe"],
        "machine_learning::regressão": ["regressao", "prever valor"],
        "python::pandas": ["pandas", "dataframe", "tabela em python"],
        "python::ler arquivo csv": [
            "csv", "read csv", "ler arquivo", "carregar arquivo"
        ],
        "python::explorar um dataframe": [
            "head", "info", "describe", "explorar dados", "conhecer dados"
        ],
        "python::filtrar dados": [
            "filtrar", "filtro", "selecionar linhas", "condicao"
        ],
        "python::valores ausentes": [
            "valor ausente", "valores ausentes", "nulo", "nulos",
            "null", "nan", "fillna", "dropna"
        ],
        "python::remover duplicados": [
            "duplicado", "duplicados", "drop duplicates"
        ],
        "python::agrupar dados com pandas": [
            "groupby", "agrupar", "agrupar dados", "agrupar vendas"
        ],
        "python::juntar dataframes": [
            "merge", "juntar dataframes", "combinar dataframes", "unir tabelas"
        ],
        "python::trabalhar com datas": [
            "datetime", "data", "datas", "converter data"
        ],
        "python::numpy": ["numpy", "array", "calculo numerico"],
        "python::visualização com matplotlib": [
            "matplotlib", "grafico", "visualizacao", "plot"
        ],
        "excel::se": ["funcao se", "condicao", "meta atingida"],
        "excel::seerro": ["seerro", "tratar erro", "erro na formula"],
        "excel::somase": ["somase", "somar com criterio", "um criterio"],
        "excel::somases": [
            "somases", "somar com criterios", "varios criterios"
        ],
        "excel::cont.se": ["cont se", "cont.se", "contar com criterio"],
        "excel::cont.ses": [
            "cont ses", "cont.ses", "contar com criterios"
        ],
        "excel::mediase": ["mediase", "media com criterio"],
        "excel::procv": ["procv", "busca vertical"],
        "excel::procx": ["procx", "buscar valor", "busca moderna"],
        "excel::procv e procx": [
            "procv e procx", "diferenca entre procv", "comparar procv"
        ],
        "excel::indice e corresp": [
            "indice e corresp", "indice", "corresp", "buscar com indice"
        ],
        "excel::funcoes de texto": [
            "funcao de texto", "arrumar", "texto juntar", "maiuscula"
        ],
        "excel::funcoes de data": [
            "data", "hoje", "ano", "mes", "diferenca de datas"
        ],
        "excel::filtro": ["filtro", "funcao filtro", "filtrar registros"],
        "excel::unico": ["unico", "valores unicos", "sem repeticao"],
        "excel::tabela dinamica": [
            "tabela dinamica", "resumir dados", "pivot table"
        ],
        "excel::dashboard": ["dashboard", "painel", "indicadores"],
        "excel::power query no excel": [
            "power query", "transformar dados", "combinar arquivos"
        ],
        "excel::indicadores no excel": [
            "indicador", "kpi", "ticket medio", "faturamento"
        ],
        "estatistica::media": [
            "media", "media aritmetica", "valor medio", "promedio"
        ],
        "estatistica::mediana": [
            "mediana", "valor central", "dados ordenados"
        ],
        "estatistica::moda": [
            "moda", "valor mais frequente", "maior frequencia"
        ],
        "estatistica::media, mediana e moda": [
            "media mediana moda", "diferenca entre media", "tendencia central"
        ],
        "estatistica::variancia": [
            "variancia", "dispersao", "afastamento da media"
        ],
        "estatistica::desvio padrao": [
            "desvio padrao", "dispersao", "valores proximos da media"
        ],
        "estatistica::variancia e desvio padrao": [
            "variancia e desvio padrao", "diferenca entre variancia", "dispersao"
        ],
        "estatistica::quartis e percentis": [
            "quartil", "quartis", "percentil", "percentis", "q1", "q3"
        ],
        "estatistica::outliers": [
            "outlier", "outliers", "valor atipico", "valor extremo", "iqr"
        ],
        "estatistica::correlacao": [
            "correlacao", "relacao entre variaveis", "coeficiente de correlacao"
        ],
        "estatistica::probabilidade": [
            "probabilidade", "chance", "evento", "casos favoraveis"
        ],
        "estatistica::distribuicao normal": [
            "distribuicao normal", "curva normal", "curva de sino", "regra 68 95 99"
        ],
        "estatistica::intervalo de confianca": [
            "intervalo de confianca", "confianca de 95", "faixa de valores"
        ],
        "estatistica::teste de hipotese": [
            "teste de hipotese", "hipotese nula", "hipotese alternativa"
        ],
        "estatistica::valor p": [
            "valor p", "p valor", "p-value", "significancia"
        ],
        "machine_learning::classificacao": [
            "classificacao", "classificar", "categoria", "classe", "fraude", "spam"
        ],
        "machine_learning::regressao": [
            "regressao", "prever valor", "valor numerico", "preco", "faturamento"
        ],
        "machine_learning::classificacao e regressao": [
            "classificacao e regressao", "diferenca entre classificacao", "tipo da variavel alvo"
        ],
        "machine_learning::separacao entre treino e teste": [
            "treino e teste", "train test split", "dados de treino", "dados de teste"
        ],
        "machine_learning::pre-processamento": [
            "pre processamento", "preparar dados", "tratamento dos dados"
        ],
        "machine_learning::pipeline": [
            "pipeline", "sequencia de transformacoes", "pre processamento e modelo"
        ],
        "machine_learning::overfitting": [
            "overfitting", "sobreajuste", "bom no treino ruim no teste"
        ],
        "machine_learning::underfitting": [
            "underfitting", "subajuste", "modelo simples demais"
        ],
        "machine_learning::overfitting e underfitting": [
            "overfitting e underfitting", "diferenca entre overfitting", "generalizacao"
        ],
        "machine_learning::acuracia": [
            "acuracia", "previsoes corretas", "accuracy"
        ],
        "machine_learning::precisao": [
            "precisao", "falsos positivos", "precision"
        ],
        "machine_learning::recall": [
            "recall", "sensibilidade", "falsos negativos"
        ],
        "machine_learning::precisao e recall": [
            "precisao e recall", "diferenca entre precisao", "falso positivo falso negativo"
        ],
        "machine_learning::f1-score": [
            "f1", "f1 score", "equilibrar precisao e recall"
        ],
        "machine_learning::matriz de confusao": [
            "matriz de confusao", "verdadeiro positivo", "falso positivo"
        ],
        "machine_learning::metricas de classificacao": [
            "metricas de classificacao", "avaliar classificacao", "classification report"
        ],
        "machine_learning::metricas de regressao": [
            "metricas de regressao", "mae", "mse", "rmse", "r2"
        ],
        "machine_learning::validacao cruzada": [
            "validacao cruzada", "cross validation", "cross val score"
        ],
        "machine_learning::vazamento de dados": [
            "vazamento de dados", "data leakage", "informacao do teste"
        ],
        "machine_learning::classes desbalanceadas": [
            "classes desbalanceadas", "desbalanceamento", "classe minoritaria"
        ],
        "machine_learning::clusterizacao": [
            "clusterizacao", "agrupamento nao supervisionado", "kmeans", "clusters"
        ],
    }

    @staticmethod
    def normalizar(texto):
        texto = unicodedata.normalize("NFD", str(texto).lower())
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        return re.sub(r"\s+", " ", texto).strip()

    def calcular_bonus(self, pergunta, assunto=None, intent=None, chave=None):
        assunto = assunto or chave
        if not assunto:
            return 0.0

        pergunta_n = self.normalizar(pergunta)
        assunto_n = self.normalizar(assunto)
        bonus = 0.0

        for termo in self.REGRAS.get(assunto, self.REGRAS.get(assunto_n, [])):
            termo_n = self.normalizar(termo)
            if re.search(rf"(?<!\w){re.escape(termo_n)}(?!\w)", pergunta_n):
                bonus += 0.08 if " " not in termo_n else 0.14

        tem_join = any(x in pergunta_n for x in (
            "join", "juntar", "unir", "combinar", "relacionar", "cruzar"
        ))
        tem_agregacao = any(x in pergunta_n for x in (
            "total", "soma", "somar", "media", "quantidade", "contar"
        ))
        tem_grupo = any(x in pergunta_n for x in (
            "group by", "agrupar", "por cliente", "por categoria", "por vendedor"
        ))
        tem_having = "having" in pergunta_n or "filtrar grupos" in pergunta_n
        tem_dataframe = any(
            termo in pergunta_n for termo in ("dataframe", "dataframes", "pandas")
        )

        if assunto_n == "sql::join":
            bonus += 0.28 if tem_join and not (tem_agregacao or tem_grupo) else 0.05 if tem_join else 0
            if tem_dataframe:
                bonus -= 0.40
        elif assunto_n == "sql::join com group by":
            bonus += 0.30 if (tem_agregacao or tem_grupo) and (tem_join or "cliente" in pergunta_n) else -0.18 if tem_join else 0
        elif assunto_n == "sql::join com group by e having":
            bonus += 0.35 if tem_having else -0.12 if tem_join else 0
        elif assunto_n == "sql::group by":
            bonus += 0.22 if tem_grupo else 0
            bonus -= 0.06 if tem_join else 0
        elif assunto_n == "python::juntar dataframes":
            if tem_dataframe and any(
                termo in pergunta_n for termo in ("juntar", "unir", "combinar", "merge")
            ):
                bonus += 0.30
        elif assunto_n == "python::agrupar dados com pandas":
            if tem_dataframe and any(
                termo in pergunta_n for termo in ("agrupar", "groupby")
            ):
                bonus += 0.28
        elif assunto_n == "excel::somases":
            tem_soma = any(
                termo in pergunta_n for termo in ("somar", "soma", "total")
            )
            tem_varios_criterios = any(termo in pergunta_n for termo in (
                "varios criterios", "mais de um criterio", "multiplos criterios"
            ))
            if tem_soma and tem_varios_criterios:
                bonus += 0.34
        elif assunto_n == "excel::seerro":
            tem_erro_formula = (
                any(termo in pergunta_n for termo in ("erro", "erros", "seerro"))
                and any(termo in pergunta_n for termo in ("formula", "tratar"))
            )
            if tem_erro_formula:
                bonus += 0.34
        elif assunto_n == "excel::formatacao condicional":
            if "criterio" in pergunta_n and any(
                termo in pergunta_n for termo in ("somar", "soma", "total")
            ):
                bonus -= 0.18
        elif assunto_n == "excel::funcoes de data":
            if "erro" in pergunta_n and "formula" in pergunta_n:
                bonus -= 0.18

        return round(max(-0.25, min(bonus, 0.65)), 4)

    def aplicar_bonus(self, pergunta, assunto, similaridade=0.0, intent=None):
        return round(
            float(similaridade)
            + self.calcular_bonus(pergunta, assunto=assunto, intent=intent),
            4,
        )
