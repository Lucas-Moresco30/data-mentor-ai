import streamlit as st

from chatbot import ChatBot
from pdf_search import PDFSearch


st.set_page_config(
    page_title="Data Mentor AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Carregando o modelo semântico...")
def criar_chatbot():
    return ChatBot(debug=False)


def formatar_secao(chave):
    if not chave:
        return "Não identificada"

    if "::" not in chave:
        return chave

    area, separador, secao = chave.partition("::")
    nomes_areas = {
        "sql": "SQL",
        "python": "Python",
        "excel": "Excel",
        "powerbi": "Power BI",
        "estatistica": "Estatística",
        "machine_learning": "Machine Learning",
    }

    area_formatada = nomes_areas.get(area, area.replace("_", " ").title())
    secao_formatada = (secao if separador else area).replace("_", " ").upper()
    return f"{area_formatada} — {secao_formatada}"


def formatar_intencao(intencao):
    nomes = {
        "definition": "Definição",
        "comparison": "Comparação",
        "example": "Exemplo",
        "list": "Lista",
        "how_to": "Como fazer",
        "consulta_pdf": "Consulta ao PDF",
        "comparacao_vaga": "Comparação com vaga",
    }
    return nomes.get(intencao, intencao or "Não identificada")


def formatar_origem(origem):
    nomes = {
        "regra direta": "Regra especializada",
        "índice exato": "Correspondência exata",
        "busca semântica": "Busca semântica",
        "documento PDF": "Documento PDF",
        "extração estruturada": "Extração estruturada",
        "análise de aderência": "Análise de aderência",
    }
    return nomes.get(origem, origem or "Não identificada")


if "chatbot" not in st.session_state:
    st.session_state.chatbot = criar_chatbot()
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "pdf_search" not in st.session_state:
    st.session_state.pdf_search = None
if "pdf_id" not in st.session_state:
    st.session_state.pdf_id = None


def perguntar(pergunta):
    if consultar_pdf and st.session_state.pdf_search is not None:
        resposta, diagnostico = (
            st.session_state.pdf_search.formatar_resposta(pergunta)
        )
    else:
        resposta = st.session_state.chatbot.responder(pergunta)
        diagnostico = st.session_state.chatbot.obter_diagnostico()
    st.session_state.mensagens.extend([
        {"papel": "user", "conteudo": pergunta},
        {"papel": "assistant", "conteudo": resposta, "diagnostico": diagnostico},
    ])


def analisar_aderencia(descricao_vaga):
    resposta, diagnostico = st.session_state.pdf_search.comparar_vaga(
        descricao_vaga
    )
    st.session_state.mensagens.extend([
        {
            "papel": "user",
            "conteudo": "Analisar a aderência do currículo à vaga informada.",
        },
        {
            "papel": "assistant",
            "conteudo": resposta,
            "diagnostico": diagnostico,
        },
    ])


with st.sidebar:
    st.title("🤖 Data Mentor AI")
    st.caption("Assistente educacional para análise de dados e BI.")
    st.subheader("📚 Base de conhecimento")
    st.markdown("✅ SQL\n\n✅ Python\n\n✅ Excel\n\n✅ Power BI\n\n✅ Estatística\n\n✅ Machine Learning")
    st.divider()

    st.subheader("📄 Consultar documento")
    arquivo_pdf = st.file_uploader(
        "Envie um arquivo PDF",
        type=["pdf"],
        help="O texto do arquivo será processado apenas nesta sessão.",
    )

    if arquivo_pdf is not None:
        arquivo_bytes = arquivo_pdf.getvalue()
        identificador = f"{arquivo_pdf.name}:{len(arquivo_bytes)}"

        if st.session_state.pdf_id != identificador:
            with st.spinner("Processando o PDF..."):
                buscador_pdf = PDFSearch(
                    st.session_state.chatbot.semantic.modelo
                )
                try:
                    resumo_pdf = buscador_pdf.carregar(
                        arquivo_bytes,
                        arquivo_pdf.name,
                    )
                except Exception as erro:
                    st.session_state.pdf_search = None
                    st.session_state.pdf_id = None
                    st.error(f"Não foi possível processar o PDF: {erro}")
                else:
                    st.session_state.pdf_search = buscador_pdf
                    st.session_state.pdf_id = identificador
                    st.success(
                        f"{resumo_pdf['paginas']} páginas e "
                        f"{resumo_pdf['blocos']} trechos indexados."
                    )

    consultar_pdf = st.toggle(
        "Responder usando o PDF",
        value=st.session_state.pdf_search is not None,
        disabled=st.session_state.pdf_search is None,
    )

    if st.session_state.pdf_search is not None:
        st.divider()
        st.subheader("🎯 Comparar com uma vaga")
        descricao_vaga = st.text_area(
            "Cole a descrição da vaga",
            height=180,
            placeholder=(
                "Exemplo: Procuramos Analista de Dados com conhecimentos "
                "em SQL, Python, Excel e Power BI..."
            ),
        )
        if st.button(
            "Analisar aderência",
            use_container_width=True,
            disabled=not descricao_vaga.strip(),
        ):
            analisar_aderencia(descricao_vaga.strip())
            st.rerun()

    st.divider()
    perguntas = sum(m["papel"] == "user" for m in st.session_state.mensagens)
    st.metric("Perguntas nesta conversa", perguntas)
    modo_dev = st.toggle("🛠️ Modo desenvolvedor")

    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state.mensagens = []
        st.session_state.chatbot.limpar_historico()
        st.rerun()


st.title("🤖 Data Mentor AI")
st.caption("Pergunte sobre SQL, Python, Excel, Power BI, Estatística e Machine Learning.")
st.success("Sistema carregado e pronto para responder.", icon="✅")

if not st.session_state.mensagens:
    st.subheader("💡 Experimente perguntar")
    sugestoes = [
        "O que é GROUP BY?",
        "Qual a diferença entre INNER JOIN e LEFT JOIN?",
        "Como calcular o total de compras por cliente?",
        "Como criar indicadores no Power BI?",
    ]
    colunas = st.columns(2)
    for indice, sugestao in enumerate(sugestoes):
        with colunas[indice % 2]:
            if st.button(sugestao, key=f"sugestao_{indice}", use_container_width=True):
                perguntar(sugestao)
                st.rerun()

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["papel"]):
        st.markdown(mensagem["conteudo"])
        diagnostico = mensagem.get("diagnostico")
        if modo_dev and diagnostico:
            with st.expander("🧠 Detalhes da busca"):
                coluna_1, coluna_2 = st.columns(2)
                with coluna_1:
                    st.caption("Seção escolhida")
                    st.code(formatar_secao(diagnostico.get("chave")))
                with coluna_2:
                    st.caption("Tipo de pergunta")
                    st.code(formatar_intencao(diagnostico.get("intencao")))

                st.caption(
                    "Origem da resposta: "
                    f"**{formatar_origem(diagnostico.get('origem'))}**"
                )

                resultado = diagnostico.get("resultado")
                if resultado:
                    confianca = float(resultado["confianca"])
                    st.metric("Confiança semântica", f"{confianca:.1f}%")
                    st.progress(min(max(confianca / 100, 0.0), 1.0))
                else:
                    st.info(
                        "Esta resposta foi encontrada por uma regra ou "
                        "correspondência exata; por isso não possui confiança semântica."
                    )

                ranking = diagnostico.get("ranking", [])
                if ranking:
                    st.caption("Três melhores resultados")
                    st.dataframe(
                        [
                            {
                                "Seção": formatar_secao(item["chave"]),
                                "Similaridade": f"{item['similaridade']:.2f}",
                                "Bônus": f"{item['bonus']:+.2f}",
                                "Pontuação final": f"{item['score_ajustado']:.2f}",
                            }
                            for item in ranking
                        ],
                        hide_index=True,
                        use_container_width=True,
                    )

pergunta = st.chat_input("Digite sua pergunta sobre dados...")
if pergunta:
    perguntar(pergunta.strip())
    st.rerun()