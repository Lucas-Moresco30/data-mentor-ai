import re
import unicodedata


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


class KnowledgeIndexer:
    def __init__(self, base_conhecimento):
        self.indice = {}
        for assunto, secoes in base_conhecimento.items():
            for secao, conteudo in secoes.items():
                chave = f"{assunto}::{secao}"
                self.indice[normalizar(secao)] = chave
                for linha in conteudo.splitlines():
                    if linha.strip().startswith("-") and ":" in linha:
                        termo = linha.split(":", 1)[0].lstrip("- ").strip()
                        self.indice[normalizar(termo)] = chave

    def buscar(self, pergunta):
        pergunta = normalizar(pergunta)
        encontrados = [
            (len(termo), chave)
            for termo, chave in self.indice.items()
            if re.search(rf"(?<!\w){re.escape(termo)}(?!\w)", pergunta)
        ]
        return max(encontrados, default=(0, None))[1]
