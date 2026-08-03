import re

from intent_classifier import IntentClassifier


class ResponseSelector:

    def __init__(self, debug=False):
        self.intent_classifier = IntentClassifier()
        self.debug = debug

    def extrair_exemplo_codigo(self, pergunta, conteudo):

        blocos = re.findall(
            r"```[\s\S]*?```",
            conteudo
        )

        if not blocos:
            return None

        pergunta_normalizada = pergunta.lower()

        if (
            any(termo in pergunta_normalizada for termo in (
                "valor nulo", "valores nulos", "valor ausente",
                "valores ausentes", "nan"
            ))
            and any(termo in pergunta_normalizada for termo in (
                "tratar", "preencher", "remover", "como"
            ))
        ):
            blocos_tratamento = [
                bloco
                for bloco in blocos
                if any(comando in bloco.lower() for comando in (
                    "isna", "fillna", "dropna"
                ))
            ]
            if blocos_tratamento:
                return (
                    "Você pode identificar, preencher ou remover valores "
                    "ausentes:\n\n"
                    + "\n\n".join(blocos_tratamento)
                )

        # Adapta o exemplo ao contexto pedido, em vez de retornar
        # automaticamente o primeiro GROUP BY disponível na seção.
        if (
            "agrupar" in pergunta_normalizada
            and "venda" in pergunta_normalizada
            and "categoria" in pergunta_normalizada
            and "pandas" not in pergunta_normalizada
            and "python" not in pergunta_normalizada
        ):
            return (
                "Exemplo de vendas agrupadas por categoria:\n\n"
                "```sql\n"
                "SELECT\n"
                "    categoria,\n"
                "    SUM(valor) AS total_vendas\n"
                "FROM vendas\n"
                "GROUP BY categoria;\n"
                "```"
            )

        # Caso combinado: JOIN com GROUP BY
        if (
            "join" in pergunta_normalizada
            and "group by" in pergunta_normalizada
        ):

            for bloco in blocos:

                bloco_normalizado = bloco.lower()

                if (
                    "join" in bloco_normalizado
                    and "group by" in bloco_normalizado
                ):
                    return (
                        "Exemplo de JOIN com GROUP BY:\n\n"
                        f"{bloco}"
                    )

        conceitos = [
            "left join",
            "right join",
            "inner join",
            "full join",
            "group by",
            "order by",
            "select",
            "where",
            "having",
            "insert",
            "update",
            "delete"
        ]

        conceitos_pergunta = [
            conceito
            for conceito in conceitos
            if conceito in pergunta_normalizada
        ]

        for conceito in conceitos_pergunta:

            for bloco in blocos:

                if conceito in bloco.lower():

                    return (
                        f"Exemplo de {conceito.upper()}:\n\n"
                        f"{bloco}"
                    )

        return f"Exemplo:\n\n{blocos[0]}"

    def extrair_lista(self, conteudo):

        linhas = conteudo.splitlines()

        resposta = []
        capturando = False

        for linha in linhas:

            linha_limpa = linha.strip()

            if (
                "principais tipos" in linha_limpa.lower()
                or "indicadores" in linha_limpa.lower()
            ):
                capturando = True
                resposta.append(linha_limpa)
                continue

            if capturando:

                if linha_limpa.startswith("-"):
                    resposta.append(linha_limpa)

                elif resposta and linha_limpa:
                    break

        if len(resposta) > 1:
            return "\n".join(resposta)

        return None

    def extrair_comparacao(self, pergunta, conteudo):

        pergunta_normalizada = pergunta.lower()

        linhas = conteudo.splitlines()

        conceitos_encontrados = []

        for linha in linhas:

            linha_limpa = linha.strip()

            if not linha_limpa.startswith("-"):
                continue

            if ":" not in linha_limpa:
                continue

            titulo, explicacao = linha_limpa.split(
                ":",
                maxsplit=1
            )

            titulo_limpo = (
                titulo
                .replace("-", "")
                .strip()
            )

            titulo_normalizado = titulo_limpo.lower()

            if titulo_normalizado in pergunta_normalizada:

                conceitos_encontrados.append(
                    f"{titulo_limpo}:\n"
                    f"{explicacao.strip()}"
                )

        if len(conceitos_encontrados) >= 2:

            return "\n\n".join(
                conceitos_encontrados
            )

        return None

    def extrair_paragrafos(self, conteudo):

        conteudo_sem_codigo = re.sub(
            r"```[\s\S]*?```",
            "",
            conteudo
        )

        paragrafos = [
            paragrafo.strip()
            for paragrafo in conteudo_sem_codigo.split("\n\n")
            if paragrafo.strip()
        ]

        return paragrafos

    def palavras_relevantes(self, texto):

        stopwords = {
            "o", "a", "os", "as",
            "um", "uma",
            "de", "do", "da", "dos", "das",
            "e", "em", "no", "na",
            "para", "por",
            "que", "é",
            "como", "qual", "quais",
            "me", "dê",
            "pode", "isso"
        }

        palavras = re.findall(
            r"\b[\wÀ-ÿ]+\b",
            texto.lower()
        )

        return {
            palavra
            for palavra in palavras
            if palavra not in stopwords
            and len(palavra) > 2
        }

    def extrair_subtopico(self, pergunta, conteudo):

        pergunta_normalizada = pergunta.lower()

        linhas = conteudo.splitlines()

        for linha in linhas:

            linha_limpa = linha.strip()

            if not linha_limpa.startswith("-"):
                continue

            if ":" not in linha_limpa:
                continue

            titulo, explicacao = linha_limpa.split(
                ":",
                maxsplit=1
            )

            titulo_limpo = (
                titulo
                .replace("-", "")
                .strip()
            )

            titulo_normalizado = titulo_limpo.lower()

            if titulo_normalizado in pergunta_normalizada:

                return (
                    f"{titulo_limpo}: "
                    f"{explicacao.strip()}"
                )

        return None

    def selecionar_melhor_paragrafo(
        self,
        pergunta,
        conteudo
    ):

        paragrafos = self.extrair_paragrafos(
            conteudo
        )

        if not paragrafos:
            return conteudo

        palavras_pergunta = self.palavras_relevantes(
            pergunta
        )

        melhor_paragrafo = None
        maior_pontuacao = 0

        for paragrafo in paragrafos:

            if paragrafo.startswith("## "):
                continue

            palavras_paragrafo = (
                self.palavras_relevantes(
                    paragrafo
                )
            )

            pontuacao = len(
                palavras_pergunta.intersection(
                    palavras_paragrafo
                )
            )

            if pontuacao > maior_pontuacao:
                maior_pontuacao = pontuacao
                melhor_paragrafo = paragrafo

        if melhor_paragrafo:
            return melhor_paragrafo

        for paragrafo in paragrafos:

            if not paragrafo.startswith("## "):
                return paragrafo

        return conteudo

    def selecionar(self, pergunta, conteudo):

        intent = self.intent_classifier.detectar(
            pergunta
        )

        pergunta_normalizada = pergunta.lower()

        if (
            intent == "definition"
            and any(termo in pergunta_normalizada for termo in (
                "correlacao", "correlação"
            ))
        ):
            return (
                "Correlação mede a força e a direção da relação linear "
                "entre duas variáveis. O coeficiente varia de -1 a 1: "
                "valores próximos de 1 indicam relação positiva forte, "
                "valores próximos de -1 indicam relação negativa forte "
                "e valores próximos de 0 indicam pouca relação linear.\n\n"
                "Correlação não significa causalidade."
            )

        if (
            "desbalancead" in pergunta_normalizada
            and any(termo in pergunta_normalizada for termo in (
                "o que fazer", "como tratar", "resolver", "lidar"
            ))
        ):
            return (
                "Quando as classes estão desbalanceadas, não avalie o modelo "
                "apenas pela acurácia. Analise precisão, recall, F1-score e a "
                "matriz de confusão.\n\n"
                "Também é possível utilizar pesos de classe, coletar mais "
                "exemplos da classe minoritária ou aplicar técnicas de "
                "reamostragem. Faça essas transformações somente nos dados "
                "de treino para evitar vazamento de dados."
            )

        if self.debug:
            print(
                f"\n🎯 Intenção identificada: {intent}"
            )

        if intent == "comparison":

            comparacao = self.extrair_comparacao(
                pergunta,
                conteudo
            )

            if comparacao:
                return comparacao

            # Perguntas como "Como comparar com o ano anterior?"
            # são classificadas como comparação, mas esperam um exemplo.
            exemplo = self.extrair_exemplo_codigo(
                pergunta,
                conteudo
            )

            if exemplo:
                return exemplo

        if intent == "example":

            exemplo = self.extrair_exemplo_codigo(
                pergunta,
                conteudo
            )

            if exemplo:
                return exemplo

        if intent == "how_to":

            exemplo = self.extrair_exemplo_codigo(
                pergunta,
                conteudo
            )

            if exemplo:
                return exemplo

        if intent == "list":

            lista = self.extrair_lista(
                conteudo
            )

            if lista:
                return lista

        subtopico = self.extrair_subtopico(
            pergunta,
            conteudo
        )

        if subtopico:
            return subtopico

        return self.selecionar_melhor_paragrafo(
            pergunta,
            conteudo
        )
