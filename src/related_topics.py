class RelatedTopics:
    def __init__(self):
        self.relacoes = {
            "sql::join": ["sql::select", "sql::where", "sql::group by"],
            "sql::select": ["sql::where", "sql::join", "sql::order by"],
            "sql::where": ["sql::select", "sql::join"],
            "sql::group by": ["sql::funções de agregação", "sql::having", "sql::join"],
            "sql::join com group by": ["sql::join", "sql::group by", "sql::having"],
            "python::pandas": [
                "python::ler arquivo csv",
                "python::explorar um dataframe",
                "python::filtrar dados",
            ],
            "python::ler arquivo csv": [
                "python::pandas",
                "python::explorar um dataframe",
                "python::valores ausentes",
            ],
            "python::filtrar dados": [
                "python::selecionar colunas",
                "python::pandas",
                "python::agrupar dados com pandas",
            ],
            "python::valores ausentes": [
                "python::remover duplicados",
                "python::explorar um dataframe",
                "python::pandas",
            ],
            "python::agrupar dados com pandas": [
                "python::pandas",
                "python::criar colunas",
                "python::visualização com matplotlib",
            ],
            "python::juntar dataframes": [
                "python::pandas",
                "sql::join",
                "python::filtrar dados",
            ],
            "powerbi::power query": [
                "powerbi::modelo de dados",
                "powerbi::relacionamentos",
                "powerbi::dashboards",
            ],
            "powerbi::modelo de dados": [
                "powerbi::relacionamentos",
                "powerbi::medidas",
                "powerbi::dax",
            ],
            "powerbi::relacionamentos": [
                "powerbi::modelo de dados",
                "powerbi::contexto de filtro",
                "powerbi::medidas",
            ],
            "powerbi::dax": [
                "powerbi::medidas",
                "powerbi::calculate",
                "powerbi::contexto de filtro",
            ],
            "powerbi::medidas": [
                "powerbi::dax",
                "powerbi::calculate",
                "powerbi::colunas calculadas",
            ],
            "powerbi::medidas e colunas calculadas": [
                "powerbi::medidas",
                "powerbi::colunas calculadas",
                "powerbi::dax",
            ],
            "powerbi::calculate": [
                "powerbi::contexto de filtro",
                "powerbi::filter",
                "powerbi::medidas",
            ],
            "powerbi::inteligência temporal": [
                "powerbi::tabela calendário",
                "powerbi::acumulado",
                "powerbi::calculate",
            ],
            "powerbi::indicadores": [
                "powerbi::medidas",
                "powerbi::dashboards",
                "powerbi::meta e atingimento",
            ],
            "excel::procv": [
                "excel::procx",
                "excel::índice e corresp",
                "excel::seerro",
            ],
            "excel::procx": [
                "excel::procv",
                "excel::índice e corresp",
                "excel::seerro",
            ],
            "excel::somases": [
                "excel::cont.ses",
                "excel::médiase",
                "excel::tabela dinâmica",
            ],
            "excel::tabela dinâmica": [
                "excel::segmentação de dados",
                "excel::gráficos",
                "excel::dashboard",
            ],
            "excel::power query no excel": [
                "excel::tabelas",
                "excel::tabela dinâmica",
                "excel::dashboard",
            ],
            "excel::dashboard": [
                "excel::indicadores no excel",
                "excel::gráficos",
                "excel::segmentação de dados",
            ],
            "estatistica::média": [
                "estatistica::mediana",
                "estatistica::moda",
                "estatistica::desvio padrão",
            ],
            "estatistica::mediana": [
                "estatistica::média",
                "estatistica::moda",
                "estatistica::outliers",
            ],
            "estatistica::variância": [
                "estatistica::desvio padrão",
                "estatistica::média",
                "estatistica::distribuição normal",
            ],
            "estatistica::desvio padrão": [
                "estatistica::variância",
                "estatistica::distribuição normal",
                "estatistica::outliers",
            ],
            "estatistica::outliers": [
                "estatistica::quartis e percentis",
                "estatistica::mediana",
                "estatistica::desvio padrão",
            ],
            "estatistica::correlação": [
                "estatistica::covariância",
                "machine_learning::regressão",
                "estatistica::estatística descritiva",
            ],
            "estatistica::distribuição normal": [
                "estatistica::desvio padrão",
                "estatistica::probabilidade",
                "estatistica::teste de hipótese",
            ],
            "estatistica::teste de hipótese": [
                "estatistica::valor p",
                "estatistica::intervalo de confiança",
                "estatistica::estatística inferencial",
            ],
            "machine_learning::classificação": [
                "machine_learning::métricas de classificação",
                "machine_learning::matriz de confusão",
                "machine_learning::classes desbalanceadas",
            ],
            "machine_learning::regressão": [
                "machine_learning::métricas de regressão",
                "machine_learning::separação entre treino e teste",
                "estatistica::correlação",
            ],
            "machine_learning::separação entre treino e teste": [
                "machine_learning::validação cruzada",
                "machine_learning::vazamento de dados",
                "machine_learning::pipeline",
            ],
            "machine_learning::overfitting": [
                "machine_learning::underfitting",
                "machine_learning::validação cruzada",
                "machine_learning::hiperparâmetros",
            ],
            "machine_learning::precisão": [
                "machine_learning::recall",
                "machine_learning::f1-score",
                "machine_learning::matriz de confusão",
            ],
            "machine_learning::recall": [
                "machine_learning::precisão",
                "machine_learning::f1-score",
                "machine_learning::classes desbalanceadas",
            ],
            "machine_learning::matriz de confusão": [
                "machine_learning::acurácia",
                "machine_learning::precisão e recall",
                "machine_learning::f1-score",
            ],
            "machine_learning::pipeline": [
                "machine_learning::pré-processamento",
                "machine_learning::padronização",
                "machine_learning::variáveis categóricas",
            ],
            "machine_learning::clusterização": [
                "machine_learning::aprendizado não supervisionado",
                "machine_learning::pré-processamento",
                "machine_learning::padronização",
            ],
        }

    def buscar(self, chave, limite=3):
        return self.relacoes.get(chave, [])[:limite]

    @staticmethod
    def formatar(chaves):
        if not chaves:
            return ""
        titulos = [chave.split("::", 1)[-1].upper() for chave in chaves]
        return "\n\n📚 Assuntos relacionados:\n" + "\n".join(f"- {titulo}" for titulo in titulos)
