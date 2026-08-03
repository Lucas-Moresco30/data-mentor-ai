from indexer import KnowledgeIndexer
from knowledge import KnowledgeBase
from related_topics import RelatedTopics
from response_selector import ResponseSelector
from semantic_search import SemanticSearch


class ChatBot:
    def __init__(self, debug=False):
        self.debug = debug
        self.kb = KnowledgeBase()
        self.base_semantica = self.kb.obter_base_semantica()
        self.seletor_resposta = ResponseSelector(debug=debug)
        self.semantic = SemanticSearch(
            self.base_semantica,
            top_k=3,
            limite_confianca=0.45,
            debug=debug,
        )
        self.indexador = KnowledgeIndexer(self.kb.base_conhecimento)
        self.assuntos_relacionados = RelatedTopics()
        self.ultimo_assunto = None
        self.ultima_secao = None
        self.ultima_intencao = None
        self.ultima_chave = None
        self.origem_busca = None
        self.historico = []

    def pergunta_de_continuacao(self, pergunta):
        pergunta = pergunta.lower().strip()
        return any(pergunta.startswith(x) for x in (
            "e ", "qual a diferença", "como funciona", "como usar",
            "me dê um exemplo", "mostre um exemplo", "explique melhor",
        ))

    def atualizar_contexto(self, chave):
        if chave and "::" in chave:
            self.ultimo_assunto, self.ultima_secao = chave.split("::", 1)

    def registrar_historico(self, pergunta, resposta, chave=None):
        self.historico.append({"pergunta": pergunta, "resposta": resposta, "chave": chave})
        self.historico = self.historico[-10:]

    def obter_historico(self):
        return list(self.historico)

    def limpar_historico(self):
        self.historico.clear()
        self.ultimo_assunto = None
        self.ultima_secao = None
        self.ultima_intencao = None
        self.ultima_chave = None
        self.origem_busca = None

    def obter_diagnostico(self):
        return {
            "intencao": self.ultima_intencao,
            "chave": self.ultima_chave,
            "origem": self.origem_busca,
            "resultado": self.semantic.obter_ultimo_resultado(),
            "ranking": self.semantic.obter_ultimo_ranking(3),
        }

    def responder(self, pergunta):
        pergunta = pergunta.strip()
        if not pergunta:
            return "Digite uma pergunta válida."

        intent = self.seletor_resposta.intent_classifier.detectar(pergunta)
        self.ultima_intencao = intent
        self.ultima_chave = None
        self.origem_busca = None
        self.semantic.ultimo_ranking = []
        self.semantic.ultimo_resultado = None
        pergunta_n = pergunta.lower()
        chave = None

        if intent == "comparison" and "join" in pergunta_n:
            chave = "sql::join"
            self.origem_busca = "regra direta"
        elif {"compras", "cliente"}.issubset(set(pergunta_n.split())) and any(
            termo in pergunta_n for termo in ("total", "somar", "soma")
        ):
            chave = "sql::join com group by"
            self.origem_busca = "regra direta"

        # Rotas específicas de Python evitam que termos genéricos como
        # "Pandas" ou "juntar" direcionem a resposta para outra seção.
        elif "csv" in pergunta_n:
            chave = "python::ler arquivo csv"
            self.origem_busca = "regra direta"
        elif any(termo in pergunta_n for termo in (
            "valor nulo", "valores nulos", "valor ausente",
            "valores ausentes", "nan", "fillna", "dropna"
        )):
            chave = "python::valores ausentes"
            self.origem_busca = "regra direta"
        elif (
            any(termo in pergunta_n for termo in ("agrupar", "groupby"))
            and "pandas" in pergunta_n
        ):
            chave = "python::agrupar dados com pandas"
            self.origem_busca = "regra direta"
        elif (
            any(termo in pergunta_n for termo in ("dataframe", "dataframes"))
            and any(termo in pergunta_n for termo in ("juntar", "unir", "combinar", "merge"))
        ):
            chave = "python::juntar dataframes"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and "medida" in pergunta_n
            and "coluna calculada" in pergunta_n
        ):
            chave = "powerbi::medidas e colunas calculadas"
            self.origem_busca = "regra direta"
        elif (
            "medida" in pergunta_n
            and any(termo in pergunta_n for termo in ("faturamento", "somar", "soma"))
            and any(termo in pergunta_n for termo in ("power bi", "dax"))
        ):
            chave = "powerbi::sum"
            self.origem_busca = "regra direta"
        elif (
            "medida" in pergunta_n
            and any(termo in pergunta_n for termo in ("power bi", "dax"))
        ):
            chave = "powerbi::medidas"
            self.origem_busca = "regra direta"
        elif (
            "excel" in pergunta_n
            and any(termo in pergunta_n for termo in ("erro", "erros", "seerro"))
            and any(termo in pergunta_n for termo in ("formula", "fórmula", "tratar"))
        ):
            chave = "excel::seerro"
            self.origem_busca = "regra direta"
        elif (
            any(termo in pergunta_n for termo in ("somar", "soma", "total"))
            and any(termo in pergunta_n for termo in (
                "varios criterios", "vários critérios", "mais de um criterio",
                "mais de um critério", "multiplos criterios", "múltiplos critérios"
            ))
        ):
            chave = "excel::somases"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and any(termo in pergunta_n for termo in ("media", "média"))
            and "mediana" in pergunta_n
        ):
            chave = "estatistica::média, mediana e moda"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and any(termo in pergunta_n for termo in ("variancia", "variância"))
            and "desvio" in pergunta_n
        ):
            chave = "estatistica::variância e desvio padrão"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and "classificacao" in pergunta_n.replace("ç", "c").replace("ã", "a")
            and "regressao" in pergunta_n.replace("ã", "a")
        ):
            chave = "machine_learning::classificação e regressão"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and any(termo in pergunta_n for termo in ("precisao", "precisão"))
            and "recall" in pergunta_n
        ):
            chave = "machine_learning::precisão e recall"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and "overfitting" in pergunta_n
            and "underfitting" in pergunta_n
        ):
            chave = "machine_learning::overfitting e underfitting"
            self.origem_busca = "regra direta"
        elif (
            any(termo in pergunta_n for termo in ("metrica", "métrica", "metricas", "métricas"))
            and any(termo in pergunta_n for termo in ("regressao", "regressão"))
        ):
            chave = "machine_learning::métricas de regressão"
            self.origem_busca = "regra direta"
        elif (
            any(termo in pergunta_n for termo in (
                "avaliar", "avaliacao", "avaliação", "metrica", "métrica", "metricas", "métricas"
            ))
            and any(termo in pergunta_n for termo in ("classificacao", "classificação"))
        ):
            chave = "machine_learning::métricas de classificação"
            self.origem_busca = "regra direta"
        elif (
            "pipeline" in pergunta_n
            and any(termo in pergunta_n for termo in (
                "scikit", "sklearn", "machine learning"
            ))
        ):
            chave = "machine_learning::pipeline"
            self.origem_busca = "regra direta"
        elif (
            intent == "comparison"
            and "procv" in pergunta_n
            and "procx" in pergunta_n
        ):
            chave = "excel::procv e procx"
            self.origem_busca = "regra direta"
        elif "power query" in pergunta_n and "excel" in pergunta_n:
            chave = "excel::power query no excel"
            self.origem_busca = "regra direta"

        if not chave:
            chave = self.indexador.buscar(pergunta)
            if chave:
                self.origem_busca = "índice exato"

        pergunta_busca = pergunta
        if not chave and self.pergunta_de_continuacao(pergunta) and self.ultimo_assunto:
            pergunta_busca = f"{self.ultimo_assunto} {self.ultima_secao or ''} {pergunta}"

        if not chave:
            chave = self.semantic.buscar(pergunta_busca, intent=intent)
            if chave:
                self.origem_busca = "busca semântica"

        conteudo = self.base_semantica.get(chave) if chave else None
        if not conteudo:
            resposta = "Não encontrei uma resposta confiável na base de conhecimento."
            self.registrar_historico(pergunta, resposta)
            return resposta

        resposta = self.seletor_resposta.selecionar(pergunta, conteudo)
        resposta += self.assuntos_relacionados.formatar(
            self.assuntos_relacionados.buscar(chave)
        )
        self.atualizar_contexto(chave)
        self.ultima_chave = chave
        self.registrar_historico(pergunta, resposta, chave)
        return resposta
