import streamlit as st
import oracledb
import pandas as pd
import time
import queries

st.set_page_config(page_title="Assistente ÔMEGA", page_icon="Ω")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #1C1C28;
    }
    .stApp, .stApp h1, .stApp h2, .st.App h3, .stApp p, .stApp label {
        color: #FFFFFF;
    }
    div[data-testid="chat-bubble-assistant"] {
        background-color: #F97316 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="chat-bubble-user"] {
        background-color: #FFFFFF !important;
        color: #1C1C28 !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: white;'>Assistente de Dados ÔMEGA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA;'>Consulte relatórios de Vendedores, Supervisores e Coordenadores.</p>", unsafe_allow_html=True)

@st.cache_resource
def setup_database():
    try:
        oracledb.init_oracle_client(lib_dir=r"C:\instantclient_19_26")
        user = st.secrets["oracle"]["user"]
        password = st.secrets["oracle"]["password"]
        dsn = st.secrets["oracle"]["dsn"]
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao Oracle: {e}")
        return None

conn = setup_database()

report_query_map = {
    "listar todos rcas": queries.query_rca_todos,
    "relatório geral de vendedores": queries.query_rca_todos,
    "listar rcas ativos": queries.query_rca_ativos,
    "vendedores ativos": queries.query_rca_ativos,
    "listar rcas inativos": queries.query_rca_inativos,
    "vendedores bloqueados": queries.query_rca_inativos,
    "listar todos supervisores": queries.query_supervisores_todos,
    "relatório de supervisores": queries.query_supervisores_todos,
    "listar supervisores ativos": queries.query_supervisores_ativos,
    "supervisores ativos": queries.query_supervisores_ativos,
    "listar supervisores inativos": queries.query_supervisores_inativos,
    "supervisores inativos": queries.query_supervisores_inativos,
    "listar todos coordenadores": queries.query_coordenadores_todos,
    "relatório de coordenadores": queries.query_coordenadores_todos,
    "listar coordenadores ativos": queries.query_coordenadores_ativos,
    "coordenadores ativos": queries.query_coordenadores_ativos,
    "listar coordenadores inativos": queries.query_coordenadores_inativos,
    "coordenadores inativos": queries.query_coordenadores_inativos,
}
count_query_map = {}

def executar_consulta(pergunta_usuario):
    if not conn:
        st.error("Não foi possível conectar ao banco de dados.")
        return None

    pergunta_lower = pergunta_usuario.lower()
    
    palavra_chave_encontrada = None
    for palavra_chave in sorted(report_query_map.keys(), key=len, reverse=True):
        if palavra_chave in pergunta_lower:
            palavra_chave_encontrada = palavra_chave
            break

    if palavra_chave_encontrada:
        sql_query = report_query_map[palavra_chave_encontrada]
        try:
            df = pd.read_sql_query(sql_query, conn)
            st.dataframe(df)
            return f"Relatório de '{palavra_chave_encontrada}' gerado com **{len(df)}** registros."
        except Exception as e:
            return f"Erro ao gerar relatório: {e}"

    for palavra_chave, sql_query in count_query_map.items():
        if palavra_chave in pergunta_lower:
            try:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                resultado = cursor.fetchone()[0]
                cursor.close()
                return f"O resultado para '{palavra_chave}' é: **{resultado}**."
            except Exception as e:
                return f"Erro ao buscar contagem: {e}"

    return "Desculpe, não entendi. Tente 'listar rcas', 'supervisores' ou 'coordenadores' (ativos ou inativos)."

if "messages" not in st.session_state:
    if conn:
        st.success("Conectado ao banco de dados Oracle com sucesso!")
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Posso gerar relatórios de Vendedores, Supervisores e Coordenadores por status."}]
    else:
        st.session_state.messages = []

for message in st.session_state.messages:
    if isinstance(message["content"], str):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ex: 'listar supervisores ativos'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if conn:
            time.sleep(0.5)
            response = executar_consulta(prompt)
            if isinstance(response, str):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Sem conexão com o banco de dados.")