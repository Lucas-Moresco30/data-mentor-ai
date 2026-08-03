from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from relevancy_booster import RelevancyBooster


class SemanticSearch:
    def __init__(
        self,
        base_conhecimento,
        modelo="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        top_k=3,
        limite_confianca=0.45,
        debug=False,
        quantidade_ranking=None,
    ):
        self.base_conhecimento = dict(base_conhecimento)
        self.assuntos = list(self.base_conhecimento)
        if not self.assuntos:
            raise ValueError("A base semântica está vazia.")

        self.top_k = quantidade_ranking or top_k
        self.limite_confianca = limite_confianca
        self.debug = debug
        self.booster = RelevancyBooster()
        self.ultimo_ranking = []
        self.ultimo_resultado = None
        try:
            self.modelo = SentenceTransformer(
                modelo,
                local_files_only=True,
            )
        except OSError:
            self.modelo = SentenceTransformer(modelo)

        textos = [
            self._texto_semantico(chave, self.base_conhecimento[chave])
            for chave in self.assuntos
        ]
        self.vetores = self.modelo.encode(
            textos,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    @staticmethod
    def _texto_semantico(chave, conteudo):
        area, _, secao = chave.partition("::")
        return f"Área: {area}. Conceito: {secao or area}.\n{conteudo}"

    def buscar(self, pergunta, intent=None):
        if not pergunta or not pergunta.strip():
            return None

        vetor = self.modelo.encode(
            [pergunta],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        similaridades = cosine_similarity(vetor, self.vetores)[0]
        ranking = []

        for indice, similaridade in enumerate(similaridades):
            chave = self.assuntos[indice]
            bonus = self.booster.calcular_bonus(
                pergunta=pergunta,
                assunto=chave,
                intent=intent,
            )
            ajustada = float(similaridade) + bonus
            ranking.append({
                "chave": chave,
                "similaridade": round(float(similaridade), 4),
                "bonus": round(bonus, 4),
                "score_ajustado": round(ajustada, 4),
                "confianca": round(max(0.0, min(ajustada, 1.0)) * 100, 2),
            })

        ranking.sort(key=lambda item: item["score_ajustado"], reverse=True)
        self.ultimo_ranking = ranking
        self.ultimo_resultado = ranking[0]

        if self.debug:
            print("\n📊 Melhores resultados semânticos:")
            for posicao, item in enumerate(ranking[: self.top_k], 1):
                print(
                    f"   {posicao}. {item['chave']} | "
                    f"Similaridade: {item['similaridade']:.2f} | "
                    f"Bônus: {item['bonus']:.2f} | "
                    f"Ajustada: {item['score_ajustado']:.2f}"
                )

        if ranking[0]["score_ajustado"] < self.limite_confianca:
            return None
        return ranking[0]["chave"]

    def obter_ultimo_ranking(self, quantidade=None):
        return list(self.ultimo_ranking[:quantidade] if quantidade else self.ultimo_ranking)

    def obter_ultimo_resultado(self):
        return dict(self.ultimo_resultado) if self.ultimo_resultado else None

    def obter_confianca(self):
        return float(self.ultimo_resultado["confianca"]) if self.ultimo_resultado else 0.0
