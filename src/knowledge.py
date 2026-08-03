import json
import re
from pathlib import Path


class KnowledgeBase:
    def __init__(self, pasta_data=None):
        self.pasta_data = (
            Path(pasta_data)
            if pasta_data
            else Path(__file__).resolve().parent.parent / "data"
        )
        self.base_conhecimento = {}
        self.palavras_chave = {}
        self.carregar_conhecimento()
        self.carregar_palavras_chave()

    def carregar_conhecimento(self):
        self.base_conhecimento.clear()

        for arquivo in sorted(self.pasta_data.glob("*.md")):
            conteudo = arquivo.read_text(encoding="utf-8").strip()
            secoes = {}

            for trecho in re.split(r"(?m)^##\s+", conteudo)[1:]:
                linhas = trecho.strip().splitlines()
                if not linhas:
                    continue
                titulo = linhas[0].strip().lower()
                secoes[titulo] = f"## {trecho.strip()}"

            if secoes:
                self.base_conhecimento[arquivo.stem.lower()] = secoes

        if not self.base_conhecimento:
            raise ValueError(f"Nenhuma seção Markdown encontrada em {self.pasta_data}.")

    def carregar_palavras_chave(self):
        caminho = self.pasta_data / "keywords.json"
        if caminho.exists():
            self.palavras_chave = json.loads(caminho.read_text(encoding="utf-8"))

    def obter_base_semantica(self):
        return {
            f"{assunto}::{titulo}": conteudo
            for assunto, secoes in self.base_conhecimento.items()
            for titulo, conteudo in secoes.items()
        }

    def obter_conteudo_assunto(self, assunto):
        secoes = self.base_conhecimento.get(assunto.lower(), {})
        return "\n\n".join(secoes.values()) if secoes else None
