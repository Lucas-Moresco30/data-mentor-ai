import re
import unicodedata
from io import BytesIO

from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity


class PDFSearch:
    COMPETENCIAS_VAGA = {
        "Python": ("python",),
        "SQL": ("sql",),
        "Excel": ("excel",),
        "Power BI": ("power bi", "powerbi"),
        "Tableau": ("tableau",),
        "Pandas": ("pandas",),
        "NumPy": ("numpy",),
        "Machine Learning": ("machine learning", "aprendizado de maquina"),
        "Estatística": ("estatistica",),
        "Análise de dados": ("analise de dados", "analista de dados"),
        "Banco de dados": ("banco de dados",),
        "ETL": ("etl",),
        "Git": ("git", "github"),
        "HTML": ("html",),
        "CSS": ("css",),
        "JavaScript": ("javascript",),
        "ServiceNow": ("servicenow",),
        "Controladoria": ("controladoria",),
        "Administração": ("administracao",),
        "Comunicação": ("comunicacao", "oratoria"),
        "Inglês": ("ingles", "english"),
        "Graduação": (
            "graduacao", "formacao superior", "ensino superior",
            "superior completo", "bacharelado"
        ),
    }

    def __init__(self, modelo, tamanho_bloco=280):
        self.modelo = modelo
        self.tamanho_bloco = tamanho_bloco
        self.nome_arquivo = None
        self.paginas = {}
        self.blocos = []
        self.vetores = None

    @staticmethod
    def _limpar_texto(texto):
        texto = texto or ""

        # Alguns PDFs usam caracteres privados como marcadores.
        texto = "".join(
            "\n" if unicodedata.category(caractere) == "Co" else caractere
            for caractere in texto
        )
        texto = re.sub(r"[\ue000-\uf8ff]", "\n", texto)
        texto = re.sub(r"[•●▪◦◆✓]", "\n", texto)
        texto = texto.replace("\x00", " ")
        texto = re.sub(r"[ \t]+", " ", texto)
        texto = re.sub(r"\n\s*\n+", "\n", texto)
        return texto.strip()

    def _dividir_texto(self, texto, pagina):
        unidades = []

        for linha in texto.splitlines():
            linha = linha.strip(" -–—;•")
            if not linha:
                continue

            # Divide linhas muito extensas em frases ou itens de currículo.
            partes = re.split(
                r"\s*;\s*|(?<=[.!?])\s+|(?=\b(?:Empresa|Departamento|Função|Curso|Formação|Experiência)\s*:)",
                linha,
                flags=re.IGNORECASE,
            )
            unidades.extend(parte.strip() for parte in partes if parte.strip())

        blocos = []
        atual = ""

        for unidade in unidades:
            candidato = f"{atual} {unidade}".strip()

            if atual and len(candidato) > self.tamanho_bloco:
                blocos.append({"pagina": pagina, "texto": atual})
                atual = unidade
            else:
                atual = candidato

        if atual:
            blocos.append({"pagina": pagina, "texto": atual})

        return [bloco for bloco in blocos if len(bloco["texto"]) >= 40]

    @staticmethod
    def _pergunta_sobre_contato(pergunta):
        pergunta = pergunta.lower()
        return any(
            termo in pergunta
            for termo in (
                "telefone", "e-mail", "email", "contato", "endereço", "endereco"
            )
        )

    @staticmethod
    def _pergunta_sobre_competencias(pergunta):
        pergunta = pergunta.lower()
        return any(
            termo in pergunta
            for termo in (
                "competência", "competencias", "habilidade",
                "qualificação", "qualificacoes", "conhecimento técnico"
            )
        )

    @staticmethod
    def _extrair_competencias(resultados):
        itens = []
        vistos = set()
        separador = re.compile(
            r"(?=Pós-graduação\s+em|Curso\s+de|Algor[ií]tmos|"
            r"HTML\s*5|The Complete|Aprenda\s+a|ServiceNow Fundamentals|"
            r"Micro-Certification)",
            flags=re.IGNORECASE,
        )

        for resultado in resultados:
            texto = re.sub(
                r"^.*?Qualificações\s+",
                "",
                resultado["texto"],
                flags=re.IGNORECASE,
            )

            for item in separador.split(texto):
                item = item.strip(" -–—;,.:")
                if not item or len(item) < 8 or len(item) > 180:
                    continue

                assinatura = re.sub(r"\W+", " ", item.lower()).strip()
                if assinatura in vistos:
                    continue

                vistos.add(assinatura)
                itens.append({
                    "texto": item,
                    "pagina": resultado["pagina"],
                })

        return itens[:12]

    @staticmethod
    def _resumir_competencias(competencias):
        categorias = []
        regras = (
            ("excel", "Excel intermediário"),
            ("tabela dinâmica", "Tabela Dinâmica"),
            ("algor", "lógica de programação"),
            ("html", "desenvolvimento web com HTML, CSS e JavaScript"),
            ("servicenow", "administração e uso da plataforma ServiceNow"),
            ("coaching", "inteligência emocional"),
            ("oratória", "comunicação e oratória"),
            ("desenvolvimento regional", "desenvolvimento regional"),
        )

        for competencia in competencias:
            texto = competencia["texto"].lower()
            for termo, categoria in regras:
                if termo in texto and categoria not in categorias:
                    categorias.append(categoria)

        if not categorias:
            return None

        if len(categorias) == 1:
            lista = categorias[0]
        else:
            lista = ", ".join(categorias[:-1]) + f" e {categorias[-1]}"

        return (
            "O currículo apresenta competências em "
            f"{lista}."
        )

    @staticmethod
    def _contem_dados_pessoais(texto):
        texto = texto.lower()
        return any(
            termo in texto
            for termo in (
                "telefone:", "e-mail:", "email:", "estado civil:",
                "idade:", "rua ", "endereço:", "endereco:"
            )
        )

    @staticmethod
    def _tipo_pergunta(pergunta):
        pergunta = pergunta.lower()

        if any(termo in pergunta for termo in ("telefone", "e-mail", "email", "contato", "endereço")):
            return "contato"
        if any(termo in pergunta for termo in ("experiência", "experiencias", "trabalhou", "empresas", "histórico profissional")):
            return "experiencias"
        if any(termo in pergunta for termo in ("formação", "formacao", "faculdade", "graduação", "pós-graduação", "escolaridade")):
            return "formacao"
        if any(termo in pergunta for termo in ("curso", "certificação", "certificacoes")):
            return "cursos"
        if PDFSearch._pergunta_sobre_competencias(pergunta):
            return "competencias"
        return "geral"

    def _texto_completo(self):
        return "\n".join(self.paginas[numero] for numero in sorted(self.paginas))

    @staticmethod
    def _normalizar_comparacao(texto):
        texto = unicodedata.normalize("NFD", texto.lower())
        texto = "".join(
            caractere
            for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )
        return re.sub(r"\s+", " ", texto).strip()

    def comparar_vaga(self, descricao_vaga):
        vaga = self._normalizar_comparacao(descricao_vaga)
        curriculo = self._normalizar_comparacao(self._texto_completo())

        requisitos = []
        compativeis = []
        ausentes = []

        for competencia, variacoes in self.COMPETENCIAS_VAGA.items():
            exigida = any(variacao in vaga for variacao in variacoes)
            if not exigida:
                continue

            requisitos.append(competencia)
            encontrada = any(variacao in curriculo for variacao in variacoes)
            if encontrada:
                compativeis.append(competencia)
            else:
                ausentes.append(competencia)

        if not requisitos:
            resposta = (
                "Não identifiquei requisitos técnicos suficientes na descrição "
                "da vaga. Cole uma descrição mais completa e tente novamente."
            )
            percentual = 0.0
        else:
            percentual = len(compativeis) / len(requisitos) * 100
            partes = [
                "### Análise de aderência à vaga",
                f"**Aderência estimada: {percentual:.0f}%** "
                f"({len(compativeis)} de {len(requisitos)} requisitos identificados)",
                "#### Competências compatíveis",
            ]
            partes.extend(
                f"- ✅ {competencia}" for competencia in compativeis
            )

            partes.append("#### Requisitos não encontrados no currículo")
            if ausentes:
                partes.extend(f"- ⚠️ {competencia}" for competencia in ausentes)
            else:
                partes.append("- Nenhum entre os requisitos identificados.")

            partes.append("#### Sugestões")
            if ausentes:
                partes.append(
                    "- Se você possuir experiência com os itens ausentes, "
                    "inclua exemplos concretos no currículo."
                )
                partes.append(
                    "- Caso ainda não possua essas competências, priorize "
                    "estudos e projetos relacionados a: " + ", ".join(ausentes) + "."
                )
            else:
                partes.append(
                    "- Destaque resultados e projetos que comprovem essas competências."
                )

            partes.append(
                "\n> A aderência é uma estimativa baseada nos termos encontrados; "
                "ela não substitui a avaliação de um recrutador."
            )
            resposta = "\n\n".join(partes)

        diagnostico = {
            "intencao": "comparacao_vaga",
            "chave": self.nome_arquivo,
            "origem": "análise de aderência",
            "resultado": None,
            "ranking": [],
        }
        return resposta, diagnostico

    def _responder_formacao(self):
        texto = " ".join(self._texto_completo().split())
        correspondencia = re.search(
            r"Formação\s+(.*?)(?=Qualificações|Experiência|$)",
            texto,
            flags=re.IGNORECASE,
        )
        if not correspondencia:
            return None

        formacao = correspondencia.group(1).strip(" -–—;.")
        itens = [
            item.strip(" -–—;.")
            for item in re.split(r"(?=Pós-graduação\s+em)", formacao)
            if item.strip(" -–—;.")
        ]
        linhas = ["### Formação acadêmica"]
        linhas.extend(f"- {item} *(página 1)*" for item in itens)
        return "\n\n".join(linhas)

    def _responder_experiencias(self):
        texto = " ".join(self._texto_completo().split())
        padrao = re.compile(
            r"Empresa:\s*(.*?)\s+Departamento(?:/\s*Seção|/Seção)?:\s*(.*?)\s+"
            r"Função:\s*(.*?)\s+Data de Admissão:\s*(.*?)\s+"
            r"Rescisão:\s*(.*?)(?=\s+Empresa:|$)",
            flags=re.IGNORECASE,
        )
        experiencias = padrao.findall(texto)
        if not experiencias:
            return None

        partes = ["### Experiências profissionais"]
        for empresa, departamento, funcao, admissao, rescisao in experiencias:
            partes.append(
                f"- **{empresa.strip()}** — {funcao.strip()}  \n"
                f"  Departamento: {departamento.strip()}  \n"
                f"  Período: {admissao.strip()} a {rescisao.strip()} *(página 2)*"
            )
        return "\n\n".join(partes)

    def _responder_contato(self, pergunta):
        texto = " ".join(self._texto_completo().split())
        campos = []
        pergunta_normalizada = pergunta.lower()
        contato_geral = "contato" in pergunta_normalizada and not any(
            termo in pergunta_normalizada
            for termo in ("telefone", "e-mail", "email", "endereço", "endereco")
        )
        padroes = (
            ("Telefone", ("telefone",), r"Telefone:\s*(.*?)(?=\s+E-mail:|\s+Email:|$)"),
            ("E-mail", ("e-mail", "email"), r"E-?mail:\s*(\S+)"),
            ("Endereço", ("endereço", "endereco"), r"(?:Curriculum Vitae\s+[^\n]*?\s+)?(Rua\s+.*?)(?=\s+Telefone:|$)"),
        )

        for rotulo, termos, padrao in padroes:
            if not contato_geral and not any(
                termo in pergunta_normalizada for termo in termos
            ):
                continue
            correspondencia = re.search(padrao, texto, flags=re.IGNORECASE)
            if correspondencia:
                campos.append(f"- **{rotulo}:** {correspondencia.group(1).strip()}")

        if not campos:
            return None
        return "### Informações de contato\n\n" + "\n".join(campos)

    def carregar(self, arquivo_bytes, nome_arquivo):
        leitor = PdfReader(BytesIO(arquivo_bytes))
        self.nome_arquivo = nome_arquivo
        self.paginas = {}
        self.blocos = []

        for numero, pagina in enumerate(leitor.pages, start=1):
            texto = self._limpar_texto(pagina.extract_text())
            if texto:
                self.paginas[numero] = texto
                self.blocos.extend(self._dividir_texto(texto, numero))

        if not self.blocos:
            raise ValueError(
                "Não foi possível extrair texto desse PDF. "
                "Ele pode conter somente imagens digitalizadas."
            )

        self.vetores = self.modelo.encode(
            [bloco["texto"] for bloco in self.blocos],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return {
            "arquivo": self.nome_arquivo,
            "paginas": len(leitor.pages),
            "blocos": len(self.blocos),
        }

    def buscar(self, pergunta, limite=5, confianca_minima=0.20):
        if self.vetores is None or not self.blocos:
            return None

        vetor_pergunta = self.modelo.encode(
            [pergunta],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        similaridades = cosine_similarity(vetor_pergunta, self.vetores)[0]
        pergunta_normalizada = pergunta.lower()
        busca_competencias = self._pergunta_sobre_competencias(pergunta)

        pontuacoes = []
        for indice, similaridade in enumerate(similaridades):
            pontuacao = float(similaridade)
            texto_normalizado = self.blocos[indice]["texto"].lower()

            if busca_competencias:
                if any(
                    termo in texto_normalizado
                    for termo in (
                        "qualificações", "curso", "excel", "programação",
                        "servicenow", "html", "javascript", "formação"
                    )
                ):
                    pontuacao += 0.18
                if any(
                    termo in texto_normalizado
                    for termo in ("data de admissão", "rescisão", "empresa:")
                ):
                    pontuacao -= 0.15

            pontuacoes.append(pontuacao)

        permite_contato = self._pergunta_sobre_contato(pergunta)
        resultados = []

        indices_ordenados = sorted(
            range(len(pontuacoes)),
            key=lambda indice: pontuacoes[indice],
            reverse=True,
        )

        for indice in indices_ordenados:
            similaridade = float(similaridades[indice])
            pontuacao = float(pontuacoes[indice])
            bloco = self.blocos[indice]

            if pontuacao < confianca_minima:
                break
            if not permite_contato and self._contem_dados_pessoais(bloco["texto"]):
                continue

            resultados.append({
                **bloco,
                "similaridade": similaridade,
                "pontuacao": min(pontuacao, 1.0),
            })
            if len(resultados) >= limite:
                break

        return resultados or None

    def formatar_resposta(self, pergunta):
        resultados = self.buscar(pergunta)
        tipo_pergunta = self._tipo_pergunta(pergunta)
        resposta_especializada = None

        if tipo_pergunta == "formacao":
            resposta_especializada = self._responder_formacao()
        elif tipo_pergunta == "experiencias":
            resposta_especializada = self._responder_experiencias()
        elif tipo_pergunta == "contato":
            resposta_especializada = self._responder_contato(pergunta)

        if not resultados and not resposta_especializada:
            return (
                "Não encontrei uma informação suficientemente relacionada "
                "à pergunta no PDF enviado.",
                {
                    "intencao": "consulta_pdf",
                    "chave": self.nome_arquivo,
                    "origem": "documento PDF",
                    "resultado": None,
                    "ranking": [],
                },
            )

        if resposta_especializada:
            partes = [resposta_especializada]
        elif tipo_pergunta in {"competencias", "cursos"}:
            titulo = (
                "Cursos e certificações"
                if tipo_pergunta == "cursos"
                else "Competências encontradas"
            )
            partes = [f"### {titulo} em `{self.nome_arquivo}`"]
            competencias = self._extrair_competencias(resultados)

            if competencias:
                resumo = self._resumir_competencias(competencias)
                if resumo:
                    if tipo_pergunta == "cursos":
                        resumo = resumo.replace(
                            "O currículo apresenta competências em",
                            "O currículo apresenta cursos e conhecimentos em",
                        )
                    partes.append(f"**Resumo:** {resumo}")
                    partes.append("#### Evidências no documento")

                for competencia in competencias:
                    partes.append(
                        f"- {competencia['texto']} "
                        f"*(página {competencia['pagina']})*"
                    )
            else:
                partes.extend(
                    f"- {resultado['texto']} *(página {resultado['pagina']})*"
                    for resultado in resultados
                )
        else:
            partes = [f"### Informações encontradas em `{self.nome_arquivo}`"]
            vistos = set()

            for resultado in resultados:
                texto = resultado["texto"].strip()
                assinatura = re.sub(r"\W+", " ", texto.lower())[:120]
                if assinatura in vistos:
                    continue
                vistos.add(assinatura)
                partes.append(f"- {texto} *(página {resultado['pagina']})*")

        partes.append(
            "\n> Resposta extraída do documento. Confira a página indicada "
            "para consultar o contexto completo."
        )

        melhor = resultados[0] if resultados else None
        usa_extracao_estruturada = resposta_especializada is not None
        diagnostico = {
            "intencao": "consulta_pdf",
            "chave": self.nome_arquivo,
            "origem": (
                "extração estruturada"
                if usa_extracao_estruturada
                else "documento PDF"
            ),
            "resultado": (
                None
                if usa_extracao_estruturada
                else {"confianca": melhor["pontuacao"] * 100}
            ),
            "ranking": [] if usa_extracao_estruturada else [
                {
                    "chave": f"Página {item['pagina']}",
                    "similaridade": item["similaridade"],
                    "bonus": item["pontuacao"] - item["similaridade"],
                    "score_ajustado": item["pontuacao"],
                }
                for item in resultados[:3]
            ],
        }
        return "\n\n".join(partes), diagnostico
