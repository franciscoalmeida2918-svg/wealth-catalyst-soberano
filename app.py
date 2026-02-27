import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA - GRID EXCEL E VISIBILIDADE
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Tabelas estilo Excel */
    div[data-testid="stTable"] table {
        border-collapse: collapse;
        width: 100%;
        background-color: #1A1A1A;
        border: 1px solid #444444;
    }
    div[data-testid="stTable"] th {
        border: 1px solid #444444;
        padding: 12px;
        text-align: center;
        background-color: #262626;
        color: #00FF88 !important;
    }
    div[data-testid="stTable"] td {
        border: 1px solid #444444;
        padding: 10px;
        text-align: right;
        color: #FFFFFF !important;
    }
    
    .indicator-box { padding: 25px; border-radius: 15px; text-align: center; color: white; font-weight: 800; font-size: 1.2rem; margin-bottom: 15px; border: 1px solid #333; }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .ifil-bg { background-color: #6a1b9a; } 
    .alvo-bg { background-color: #005f36; }  
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal Soberano")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar"):
        if senha == "@12.3-4": st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA AUTOMÁTICO
@st.cache_data(ttl=86400)
def buscar_taxas_vivas():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        taxa_ifil = round(i + 6.35, 2) 
        radar = [
            {"Ativo": "LCI/LCA (Isento)", "Rent_Anual": i + 6.8, "Risco": "Baixo"},
            {"Ativo": "CDB (125% CDI)", "Rent_Anual": (s * 1.25) * 0.825, "Risco": "Baixo"},
            {"Ativo": "IFIL (FIIs Logística)", "Rent_Anual": taxa_ifil, "Risco": "Moderado"},
            {"Ativo": "Ações (Máxima Aceleração)", "Rent_Anual": 16.5, "Risco": "Alto"},
        ]
        return s, i, taxa_ifil, radar
    except: return 13.25, 4.50, 10.85, []

selic_at, ipca_at, taxa_ifil_at, radar_dados = buscar_taxas_vivas()
df_radar = pd.DataFrame(radar_dados)

# 3. SIDEBAR - OPERAÇÕES (AJUSTADO)
st.sidebar.title("🕹️ Operações")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=0.0)
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
ativo_escolhido = st.sidebar.selectbox("Título Selecionado:", df_radar['Ativo'].tolist())
taxa_anual_escolhida = df_radar[df_radar['Ativo'] == ativo_escolhido]['Rent_Anual'].values[0]
taxa_mensal = (1 + (taxa_anual_escolhida/100))**(1/12) - 1

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst IA")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box ifil-bg'>IFIL: {taxa_ifil_at}%</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='indicator-box alvo-bg'>TARGET: {taxa_anual_escolhida:.2f}%</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CRONOGRAMA 1 ANO", "🚀 ACELERAÇÃO 10 ANOS"])

with tab1:
    st.subheader(f"Estratégia: {ativo_escolhido}")
    saldo = cap_inicial
    logs = []
    # O Capital Inicial aparece antes do primeiro aporte no log se houver valor
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({
            "Mês": f"Mês {m:02d}", 
            "Aporte": real_br(aporte), 
            "Lucro Líquido": real_br(lucro), 
            "Patrimônio": real_br(saldo)
        })
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Caminho da Independência")
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo = renda_alvo / taxa_mensal
    st.success(f"Capital Alvo: {real_br(cap_alvo)}")
    
    saldo_10 = cap_inicial
    logs_10 = []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal)
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio": real_br(saldo_10),
            "Renda Passiva": real_br(saldo_10 * taxa_mensal),
            "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"
        })
    st.table(pd.DataFrame(logs_10))
