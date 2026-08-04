## Demonstração online

Acesse o projeto: [Data Mentor AI](https://data-mentor-ai-lucas.streamlit.app)

# Data Mentor AI

Assistente educacional para análise de dados, desenvolvido em Python e Streamlit. O projeto combina uma base de conhecimento em Markdown, busca semântica multilíngue, regras especializadas e classificação de intenção para responder perguntas sobre SQL, Python, Excel, Power BI, Estatística e Machine Learning.

Além da base educacional, a aplicação permite enviar documentos PDF, consultar informações encontradas no arquivo e comparar um currículo com os requisitos de uma vaga.

## Funcionalidades

- Interface web em formato de chat com Streamlit.
- Versão alternativa para uso pelo terminal.
- Busca por correspondência exata e busca semântica por seção.
- Modelo multilíngue adequado para perguntas em português.
- Classificação do tipo de pergunta: definição, comparação, exemplo e procedimento.
- Relevancy Booster para reduzir ambiguidades entre assuntos próximos.
- Respostas com explicações, exemplos de código e assuntos relacionados.
- Histórico da conversa durante a sessão.
- Modo desenvolvedor com seção escolhida, origem, confiança e ranking.
- Upload e consulta de documentos PDF.
- Extração estruturada de informações de currículos.
- Comparação estimada entre currículo e descrição de vaga.
- Testes automáticos das seis áreas de conhecimento.

## Áreas de conhecimento

| Área | Exemplos de conteúdo |
|---|---|
| SQL | SELECT, WHERE, JOIN, GROUP BY, HAVING e funções de agregação |
| Python | Pandas, DataFrames, CSV, valores ausentes e Matplotlib |
| Excel | SOMASES, PROCV, PROCX, SEERRO, Tabela Dinâmica e Power Query |
| Power BI | DAX, medidas, CALCULATE, indicadores e inteligência temporal |
| Estatística | tendência central, dispersão, correlação, outliers e probabilidade |
| Machine Learning | classificação, regressão, métricas, pipelines e validação |

## Tecnologias

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- NumPy
- PyPDF
- Markdown

O modelo semântico utilizado é `paraphrase-multilingual-MiniLM-L12-v2`.

## Estrutura do projeto

text
data-mentor-ai/
├── data/                       # Base educacional em Markdown
│   ├── sql.md
│   ├── python.md
│   ├── excel.md
│   ├── powerbi.md
│   ├── estatistica.md
│   ├── machine_learning.md
│   └── keywords.json
├── src/
│   ├── app.py                  # Aplicação de terminal
│   ├── app_streamlit.py        # Interface web
│   ├── chatbot.py              # Orquestração das respostas
│   ├── knowledge.py            # Carregamento da base
│   ├── semantic_search.py      # Busca por embeddings
│   ├── relevancy_booster.py    # Ajustes de relevância
│   ├── intent_classifier.py    # Classificação de intenção
│   ├── response_selector.py    # Seleção do trecho da resposta
│   ├── related_topics.py       # Assuntos relacionados
│   ├── indexer.py              # Correspondências exatas
│   └── pdf_search.py           # Consulta e análise de PDFs
├── tests/
│   └── validar_projeto.py      # Validação geral
├── requirements.txt
├── .gitignore
└── README.md


## Instalação

### 1. Clonar o repositório

bash
git clone URL_DO_REPOSITORIO
cd data-mentor-ai


Substitua `URL_DO_REPOSITORIO` pelo endereço apresentado no GitHub.

### 2. Criar o ambiente virtual

No Windows PowerShell:

powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1


No Linux ou macOS:

bash
python3 -m venv .venv
source .venv/bin/activate


### 3. Instalar as dependências

bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


Na primeira execução, o modelo de embeddings será baixado automaticamente. Esse processo pode demorar alguns minutos.

## Executar a interface web

Na raiz do projeto:

bash
python -m streamlit run src/app_streamlit.py


A interface normalmente ficará disponível em:

text
http://localhost:8501


## Executar pelo terminal

bash
python src/app.py


## Executar os testes

bash
python tests/validar_projeto.py


Resultado esperado:

text
RESULTADO: 35/35 testes aprovados (100.0%)


## Exemplos de perguntas

text
Qual é a diferença entre INNER JOIN e LEFT JOIN?
Como agrupar vendas por categoria no Pandas?
Como calcular o percentual do total em DAX?
Qual é a diferença entre PROCV e PROCX?
Como identificar outliers usando o IQR?
Qual é a diferença entre classificação e regressão?


## Consulta em PDF

1. Abra a barra lateral da interface.
2. Envie um arquivo PDF.
3. Ative a opção para responder usando o documento.
4. Faça perguntas sobre o conteúdo carregado.

Quando o documento é um currículo, a aplicação também consegue apresentar formação, experiências, competências, cursos e informações de contato. A comparação com uma vaga é uma estimativa baseada nos termos encontrados e não substitui a avaliação de um recrutador.

## Como a resposta é selecionada

text
Pergunta do usuário
        ↓
Classificação de intenção
        ↓
Regra especializada ou índice exato
        ↓
Busca semântica por seção
        ↓
Relevancy Booster
        ↓
Seleção do trecho e assuntos relacionados


## Privacidade

Os PDFs enviados pela interface são processados durante a sessão da aplicação. Não publique currículos ou documentos com informações pessoais no repositório.

## Status

- Base educacional: concluída.
- Interface web: concluída.
- Consulta em PDF: concluída.
- Testes principais: 35 de 35 aprovados.
- Próximo passo: publicação e validação da versão online.

