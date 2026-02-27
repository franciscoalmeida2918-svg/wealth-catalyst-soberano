import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA E GRID EXCEL
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #1A1A1A; border: 1px solid #444444; }
    div[data-testid="stTable"] th { border: 1px solid #444444; padding: 12px; text-align: center; background-color: #262626; color: #00FF88 !important; }
    div[data-testid="stTable"] td { border: 1px solid #444444; padding: 10px; text-align: right; color: #FFFFFF !important; }
    
    .indicator-box { padding: 25px; border-radius: 15px; text-align: center; color: white; font-weight: 800; font-size: 1.2rem; margin-bottom: 15px; border: 1px solid #333; }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .ifil-bg { background-color: #6a1b9a; } 
    .alvo-bg { background-color: #005f36; }
    .acelera-card { background-color: #1a1a1a; border: 2px solid #00FF88; padding: 20px; border-radius: 10px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal Soberano")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar"):
        if senha == ".123.4": st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA E ACELERAÇÃO
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
            {"Ativo": "Ações (Máxima Aceleração)", "Rent_Anual": 17.5, "Risco": "Alto"},
        ]
        return s, i, taxa_ifil, radar
    except: return 13.25, 4.50, 10.85, []

selic_at, ipca_at, taxa_ifil_at, radar_dados = buscar_taxas_vivas()
df_radar = pd.DataFrame(radar_dados)

# Identificar título foguete
foguete = df_radar.loc[df_radar['Rent_Anual'].idxmax()]

# 3. SIDEBAR - OPERAÇÕES
st.sidebar.title("🕹️ Operações")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=0.0)
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
ativo_escolhido = st.sidebar.selectbox("Título Selecionado:", df_radar['Ativo'].tolist())
taxa_escolhida = df_radar[df_radar['Ativo'] == ativo_escolhido]['Rent_Anual'].values[0]
taxa_mensal_escolhida = (1 + (taxa_escolhida/100))**(1/12) - 1
taxa_mensal_foguete = (1 + (foguete['Rent_Anual']/100))**(1/12) - 1

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst IA - Inteligência de Aceleração")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box ifil-bg'>IFIL: {taxa_ifil_at}%</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='indicator-box alvo-bg'>TARGET: {taxa_escolhida:.2f}%</div>", unsafe_allow_html=True)

# LÓGICA DE INDICAÇÃO DE ACELERAÇÃO
renda_alvo = 5000.0 # Padrão para cálculo rápido
cap_alvo_escolhido = renda_alvo / taxa_mensal_escolhida
cap_alvo_foguete = renda_alvo / taxa_mensal_foguete

# Cálculo simplificado de tempo (meses) para atingir cap_alvo com aporte médio
def estimar_meses(cap_ini, aporte, taxa, alvo):
    if taxa <= 0: return 999
    m = 0
    s = cap_ini
    while s < alvo and m < 360:
        a = 3000 if (m+1) % 6 == 0 else 2500
        s = s * (1 + taxa) + a
        m += 1
    return m

meses_atual = estimar_meses(cap_inicial, aporte_base, taxa_mensal_escolhida, cap_alvo_escolhido)
meses_foguete = estimar_meses(cap_inicial, aporte_base, taxa_mensal_foguete, cap_alvo_foguete)
economia = meses_atual - meses_foguete

if ativo_escolhido != foguete['Ativo'] and economia > 0:
    st.markdown(f"""
    <div class='acelera-card'>
        <h3 style='margin:0; color:#00FF88;'>⚡ ESTRATÉGIA DE ANTECIPAÇÃO</h3>
        O título <strong>{foguete['Ativo']}</strong> está rendendo <strong>{foguete['Rent_Anual']:.2f}%</strong>.<br>
        Ao migrar para esta estratégia, você antecipa sua independência em aproximadamente <strong>{economia} meses</strong>.
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CRONOGRAMA 1 ANO", "🚀 ACELERAÇÃO 10 ANOS"])

with tab1:
    st.subheader(f"Simulação: {ativo_escolhido}")
    saldo = cap_inicial
    logs = []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal_escolhida
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Caminho 10 Anos")
    cap_alvo_input = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo_final = cap_alvo_input / taxa_mensal_escolhida
    st.success(f"Capital Alvo: {real_br(cap_alvo_final)}")
    
    saldo_10 = cap_inicial
    logs_10 = []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal_escolhida)
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio": real_br(saldo_10),
            "Renda Passiva": real_br(saldo_10 * taxa_mensal_escolhida),
            "Progresso": f"{(saldo_10/cap_alvo_final)*100:.1f}%"
        })
    st.table(pd.DataFrame(logs_10))
