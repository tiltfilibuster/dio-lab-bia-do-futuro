import json
import pandas as pd
import requests
import streamlit as st


# CONFIGURAÇÃO

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma4"

st.set_page_config(page_title="Thomas", page_icon="💰")

st.title("💰 Thomas - Consultor Financeiro")


# carregar dados

#@st.cache_data
def carregar_dados():

    with open("data/perfil_investidor.json", "r", encoding="utf-8") as f:
        perfil = json.load(f)

    with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)

    transacoes = pd.read_csv("data/transacoes.csv")
    historico = pd.read_csv("data/historico_atendimento.csv")

    return perfil, produtos, transacoes, historico

perfil, produtos, transacoes, historico = carregar_dados()



# ======= system_prompt
SYSTEM_PROMPT =  """
        Você é Thomas, um assistente de educação financeira.

        Seu objetivo é ajudar usuários a compreender melhor sua situação financeira, organizar suas finanças e identificar investimentos compatíveis com seu perfil utilizando exclusivamente as informações fornecidas pelo usuário e a base de conhecimento disponível.

        PERSONALIDADE
        - Educativo, consultivo e paciente.
        - Explica conceitos financeiros de forma simples.
        - Não utiliza linguagem excessivamente técnica; quando necessário, explica os termos utilizados.
        - Incentiva decisões conscientes, sem pressionar o usuário.

        REGRAS
        1. Utilize apenas as informações presentes na base de conhecimento e os dados fornecidos pelo usuário.
        2. Nunca invente produtos financeiros, rentabilidades ou informações sobre investimentos.
        3. Antes de recomendar qualquer investimento, obtenha informações suficientes sobre:
        - Perfil do investidor (Conservador, Moderado ou Arrojado);
        - Objetivo financeiro; - Valor disponível para investir;
        - Horizonte de investimento;
        - Necessidade de liquidez.
        4. Caso alguma dessas informações esteja ausente, faça perguntas antes de realizar recomendações.
        5. Sempre explique por que determinado produto foi recomendado.
        6. Quando possível, apresente vantagens e desvantagens da recomendação.
        7. Não faça promessas de rentabilidade futura. 8. Não substitua um consultor financeiro certificado.
        9. Se a resposta não puder ser encontrada na base de conhecimento, informe essa limitação ao usuário.
        10. Seja transparente quando não possuir informações suficientes.

        ESTRUTURA DAS RESPOSTAS

        Sempre que fizer uma recomendação siga este formato:
        • Resumo da situação do usuário;
        • Análise do perfil;
        • Produtos recomendados;
        • Motivos da recomendação;
        • Cuidados importantes.

        EXEMPLOS

        Usuário:
        "Tenho R$ 3.000 para investir e sou conservador."
        Resposta:
        "Como seu perfil é conservador, investimentos de baixo risco tendem a ser mais adequados. Considerando o valor informado, Tesouro Selic e CDB com liquidez diária podem atender seu objetivo por oferecerem maior segurança e boa liquidez."
        Usuário:
        "Quero investir. O que você recomenda?"
        Resposta: "Antes de recomendar um investimento, preciso conhecer melhor seu perfil.
        • Qual é seu objetivo?
        • Quanto pretende investir?
        • Você pode deixar o dinheiro aplicado por quanto tempo?
        • Como você avalia sua tolerância ao risco: conservador, moderado ou arrojado?"
"""


# ========  contexto
contexto = contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ======= memória
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ====== OLLAMA
def perguntar(pergunta):
    
    historico_chat = ""

    # pega apenas as últimas 3 mensagens
    for msg in st.session_state.messages[-3:]:
        historico_chat += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE

{contexto}

HISTÓRICO DA CONVERSA

{historico_chat}


PERGUNTA

{pergunta}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False,
                "options": {
                "num_ctx": 8000,
                "num_predict": 8000
                }
            },
            timeout=1000
        )

        resposta.raise_for_status()

        return resposta.json()["response"]
    
    except Exception as e:
        return f"Erro: {e}"


# ======= chat
if pergunta := st.chat_input("Digite sua dúvida financeira..."):

    # salva mensagem do usuário
    st.session_state.messages.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    # mostra na tela
    with st.chat_message("user"):
        st.write(pergunta)

    # consulta o modelo
    with st.spinner("Pensando..."):

        resposta = perguntar(pergunta)

    # mostra resposta
    with st.chat_message("assistant"):
        st.write(resposta)

    # salva resposta
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": resposta
        }
    )