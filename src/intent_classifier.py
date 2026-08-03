import re
import unicodedata


class IntentClassifier:
    INTENCOES = {
        "comparison": ["diferenca", "comparar", "comparacao", " versus ", " vs "],
        "example": ["exemplo", "codigo", "consulta sql", "mostre como"],
        "list": ["quais sao", "quais os", "tipos de", "liste", "lista de"],
        "how_to": ["como ", "passo a passo"],
        "definition": ["o que e", "o que sao", "significa", "defina", "conceito"],
    }

    @staticmethod
    def normalizar(texto):
        texto = unicodedata.normalize("NFD", texto.lower())
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        return re.sub(r"\s+", " ", texto).strip()

    def detectar(self, pergunta):
        pergunta = f" {self.normalizar(pergunta)} "
        for intencao in ("comparison", "example", "list", "how_to", "definition"):
            if any(expressao in pergunta for expressao in self.INTENCOES[intencao]):
                return intencao
        return "definition"
