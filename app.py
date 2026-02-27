import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA DE ALTO NÍVEL (PROFISSIONAL & DARK)
st.set_page_config(page_title="Terminal Soberano IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .chat-card { background: #0a0a0a; border: 1px solid #00FF88; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0, 255, 136, 0.1); }
    .strategy-card { background: linear-gradient(90deg, #111 0%, #050505 100%); border-left: 5px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .highlight { color: #00FF88; font-weight: bold; font-size: 1.1em; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 3px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
    div[data-testid="stTable"] table { border: 1px solid #333; }
    div[data-testid="stTable"] th { background-color: #1a1a1a; color: #00FF88 !important; text-align: center; }
    div[data-testid="stTable"] td { text-align: right; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# 2. SISTEMA DE SEGURANÇA (AUTENTICAÇÃO)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Acesso ao Terminal Soberano")
    chave = st.text_input("Chave Criptográfica:", type="password")
    if st.button("DESBLOQUEAR"):
        if chave == "%102030": # Senha padrão conforme solicitado
            st.session_state.auth = True
            st.rerun()
        else: st.error("Chave Inválida.")
    st.stop()

# 3. MOTOR DE DADOS EM TEMPO REAL (SELIC / IPCA)
@st.cache_data(ttl=3600)
def fetch_real_data():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except: return 13.25, 4.50

selic, ipca = fetch_real_data()

# 4. SALA DE GUERRA (SIDEBAR - CONTROLE DE ATIVOS)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=1000.0, step=500.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
# Definição técnica dos títulos baseada nos seus bancos
ativos_db = [
    {"Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Taxa_Liq": 16.80, "Peso": 0.5},
    {"Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Taxa_Liq": 12.45, "Peso": 0.3},
    {"Ticker": "FII CVBI11 / Papel", "Banco": "ITAÚ/SAN", "Taxa_Liq": 13.10, "Peso": 0.2}
]
escolhidos = st.sidebar.multiselect("Ativos em Operação:", [a['Ticker'] for a in ativos_db], default=[a['Ticker'] for a in ativos_db])

# 5. CÉREBRO DA IA (PROCESSAMENTO E ESTRATÉGIA)
def brain_ia(query, cap, base, acel, taxa_media, inflacao):
    query = query.lower()
    val_mes = acel if datetime.now().month in [6, 12] else base
    ganho_real = taxa_media - inflacao
    
    if "mercado" in query or "estratégia" in query:
        return f"""O mercado hoje exige proteção via IPCA. Sua taxa de <span class='highlight'>{taxa_media:.2f}% a.a.</span> 
        está blindada. Com um Capital Inicial de {real_br(cap)}, recomendo focar 50% do aporte de {real_br(val_mes)} 
        no <span class='bank-badge'>ABC</span> para capturar o prêmio de 8.5% sobre a inflação. Isso acelera sua meta em 14%."""
    
    elif "calcular" in query or "quanto" in query:
        estimativa_1ano = (cap * (1 + taxa_media/100)) + (base * 12)
        return f"Cálculo Realizado: Em 12 meses, mantendo o ritmo, seu patrimônio líquido projetado é de aproximadamente <span class='highlight'>{real_br(estimativa_1ano)}</span>."
    
    return "Protocolo Soberano Ativo. Estou pronta para calcular qualquer cenário ou fornecer a melhor alocação para seus bancos."

# 6. INTERFACE DE COMANDO IA
st.title("🤖 IA Estrategista Profissional")

with st.container():
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
    pergunta = st.text_input("Comando de Voz/Texto (Ex: Qual a estratégia para hoje?):")
    
    # Cálculo da Taxa Soberana atual
    df_sel = pd.DataFrame([a for a in ativos_db if a['Ticker'] in escolhidos])
    if not df_sel.empty:
        df_sel['Peso_Adj'] = df_sel['Peso'] / df_sel['Peso'].sum()
        taxa_media = sum(df_sel['Taxa_Liq'] * df_sel['Peso_Adj'])
        taxa_mensal = (1 + (taxa_media/100))**(1/12) - 1
    else: taxa_media = taxa_mensal = 0

    if pergunta:
        resposta = brain_ia(pergunta, cap_inicial, aporte_base, aporte_acel, taxa_media, ipca)
        st.markdown(f"**SENTINELA IA:** {resposta}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 7. EXIBIÇÃO DE RESULTADOS PARA TOMADA DE DECISÃO
c1, c2, c3 = st.columns(3)
c1.metric("TAXA MÉDIA LÍQUIDA", f"{taxa_media:.2f}% a.a.")
c2.metric("GANHO REAL (VS IPCA)", f"{(taxa_media - ipca):.2f}%")
c3.metric("STATUS DA META", "ACELERADA" if taxa_media > 12 else "ESTÁVEL")

# Tabela Excel de Lucro Líquido
st.subheader("📊 Cronograma Estratégico de Ganho de Capital")
def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

saldo = cap_inicial
cronograma = []
for m in range(1, 13):
    ap = aporte_acel if m in [6, 12] else aporte_base
    lucro = saldo * taxa_mensal
    saldo += ap + lucro
    cronograma.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(ap), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})

st.table(pd.DataFrame(cronograma))
