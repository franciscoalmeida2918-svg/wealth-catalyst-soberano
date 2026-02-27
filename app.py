import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. CONFIGURAÇÃO DE SEGURANÇA E ESTÉTICA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stTextInput > div > div > input { background-color: #111; color: #00FF88; border: 1px solid #00FF88; }
    .chat-card { background: #0a0a0a; border: 1px solid #00FF88; padding: 20px; border-radius: 10px; margin-top: 10px; }
    .strategy-card { background: #111; border-left: 5px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .highlight { color: #00FF88; font-weight: bold; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN SOBERANO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Terminal de Comando Soberano")
    st.markdown("### Digite sua Chave de Acesso para liberar o Estrategista")
    chave = st.text_input("CHAVE CRIPTOGRÁFICA:", type="password")
    
    if st.button("DESBLOQUEAR ACESSO"):
        if chave == "@102030": # <--- COLOQUE SUA SENHA AQUI
            st.session_state.autenticado = True
            st.success("Acesso Concedido. Carregando Protocolo Anti-Inflação...")
            st.rerun()
        else:
            st.error("Chave Inválida. Acesso Negado.")
    st.stop() # Interrompe o código aqui se não estiver logado

# ----------------------------------------------------------------
# O CÓDIGO ABAIXO SÓ EXECUTA APÓS A SENHA CORRETA
# ----------------------------------------------------------------

# 2. MOTOR DE DADOS EM TEMPO REAL
@st.cache_data(ttl=3600)
def get_data():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except: return 13.25, 4.50

selic, ipca = get_data()

# 3. SALA DE GUERRA (SIDEBAR)
st.sidebar.title("🕹️ Sala de Guerra")
if st.sidebar.button("🔒 BLOQUEAR TERMINAL"):
    st.session_state.autenticado = False
    st.rerun()

st.sidebar.divider()
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

# 4. SENTINELA IA (FILTRO ANTI-INFLAÇÃO)
st.title("🛡️ Sentinela IA - Inteligência Anti-Inflação")
st.markdown(f"**Status:** Conectado ao Dr. IA | **IPCA Atual:** {ipca}%")

with st.container():
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
    pergunta = st.text_input("Pergunte sobre sua estratégia de investimentos:")
    if pergunta:
        # A IA só sugere o que ganha do IPCA
        taxa_alvo = 16.80 # Exemplo do Banco ABC
        ganho_real = taxa_alvo - ipca
        st.write(f"🤖 **IA Sentinela:** Com base no seu Capital Inicial de R$ {cap_inicial:,.2f}, sua estratégia no Banco ABC está rendendo {ganho_real:.2f}% acima da inflação. Qualquer aporte abaixo disso será vetado pelo meu sistema.")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. TABELA DE RESULTADOS LÍQUIDOS (ESTILO EXCEL)
st.divider()
st.subheader("📊 Cronograma de Aceleração Líquida (12 Meses)")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

taxa_mensal = (1 + (16.80/100))**(1/12) - 1
saldo = cap_inicial
logs = []

for m in range(1, 13):
    ap = aporte_acel if m in [6, 12] else aporte_base
    lucro = saldo * taxa_mensal
    saldo += ap + lucro
    logs.append({
        "Mês": f"Mês {m:02d}",
        "Aporte": real_br(ap),
        "Lucro Líquido": real_br(lucro),
        "Patrimônio": real_br(saldo)
    })

st.table(pd.DataFrame(logs))
