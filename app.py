import streamlit as st
import time

st.set_page_config(page_title="Assistente ÔMEGA", page_icon="Ω")

st.markdown(
    """
    <style>
    /* Cor de fundo principal da página */
    .stApp {
        background-color: #0B102A;
    }
    /* Cor do texto principal */
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
        color: #FFFFFF;
    }
    /* Contêiner da área do chat */
    .st-emotion-cache-r421ms {
        background-color: #12183D; /* Um tom de azul um pouco mais claro para contraste */
        border-radius: 10px;
    }
    /* Caixa de mensagem do ASSISTENTE (cor laranja da marca) */
    div[data-testid="chat-bubble-assistant"] {
        background-color: #FF5F1F !important;
        color: #FFFFFF !important;
    }
    /* Caixa de mensagem do USUÁRIO (branco para contraste) */
    div[data-testid="chat-bubble-user"] {
        background-color: #FFFFFF !important;
        color: #0B102A !important; /* Texto com o azul da marca */
    }
    /* Título principal */
    h1 {
        text-align: center;
    }
    /* Caption abaixo do título */
    .st-emotion-cache-1x40k2j p {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Assistente Virtual ÔMEGA")
st.caption("Estou aqui para ajudar com suas dúvidas!")

respostas_predefinidas = {
    "olá": "Olá! Boas-vindas ao assistente virtual da ÔMEGA Distribuidora. Como posso ajudar? 😊",
    "oi": "Oi! Que bom te ver por aqui. Em que a ÔMEGA pode ser útil?",
    "preço": "Para qual de nossos produtos você gostaria de saber o preço?",
    "entrega": "A ÔMEGA realiza entregas em toda a região. Para calcular o frete e o prazo, por favor, informe sua cidade.",
    "pagamento": "Aceitamos Pix, boleto bancário e os principais cartões de crédito e débito.",
    "horário": "Nosso horário de atendimento é de segunda a sexta, das 8h às 18h, e aos sábados, das 8h ao meio-dia.",
    "endereço": "Nossa distribuidora fica na Rua das Oportunidades, 123 - Bairro Central, Fortaleza-CE.",
    "contato": "Você pode nos contatar pelo telefone (85) 3333-4444 ou pelo email contato@omegadistribuidora.com.br.",
    "ajuda": "Claro! Posso te dar informações sobre: **preço**, **entrega**, **pagamento**, **horário**, **endereço** e **contato**.",
    "obrigado": "De nada! A ÔMEGA Distribuidora agradece o seu contato. Se precisar de mais algo, é só chamar! 😄"
}

def encontrar_resposta(entrada_usuario):
    entrada_lower = entrada_usuario.lower()
    for palavra_chave, resposta in respostas_predefinidas.items():
        if palavra_chave in entrada_lower:
            return resposta
    return "Desculpe, não entendi. Poderia reformular sua pergunta? Digite 'ajuda' para ver os tópicos que conheço."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bem-vindo(a) à ÔMEGA Distribuidora! Como posso ajudar?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        time.sleep(0.5)
        response = encontrar_resposta(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})