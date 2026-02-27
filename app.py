import streamlit as st
import pandas as pd
import requests

# 1. ESTÉTICA SOBERANA - VISIBILIDADE ESTRATÉGICA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] { background-color: #1A1A1A; border: 1px solid #333333; border-radius: 8px; }
    th { color: #FFFFFF !important; background-color: #262626 !important; }
    td { color: #FFFFFF !important; }
    .indicator-box { padding: 25px; border-radius: 15px; text-align: center; color: white; font-weight: 800; font-size: 1.4rem; margin-bottom: 15px; }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .alvo-bg { background-color: #005f36; }  
    .sugestao-card { background-color: #1E1E1E; padding: 20px; border-left: 5px solid #FFD700; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "(12%34)": st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA E INTELIGÊNCIA DE ALOCAÇÃO
@st.cache_data(ttl=3600)
def scanner_soberano():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        radar = [
            {"Ativo": "LCI/LCA (Isento)", "Rent_Anual": i + 6.5, "Risco": "Baixo", "Peso": 0.40},
            {"Ativo": "CDB (120% CDI)", "Rent_Anual": (s * 1.20) * 0.825, "Risco": "Baixo", "Peso": 0.30},
            {"Ativo": "Ações/FIIs", "Rent_Anual": 15.0, "Risco": "Alto", "Peso": 0.30}
        ]
        return s, i, radar
    except: return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = scanner_soberano()

# 3. SIDEBAR
st.sidebar.title("🕹️ Comando")
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)
mes_atual_acel = st.sidebar.checkbox("Mês de Aceleração (R$ 3k)?")
valor_aporte_atual = aporte_extra if mes_atual_acel else aporte_base

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst IA - Estratégia Soberana")

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box alvo-bg'>APORTE: {real_br(valor_aporte_atual)}</div>", unsafe_allow_html=True)

# SEÇÃO DE SUGESTÃO TÁTICA
st.markdown("### 🎯 Plano de Alocação Sugerida (Deste Mês)")
col_a, col_b = st.columns([1, 2])

alocacao = []
for item in radar_dados:
    valor_alocado = valor_aporte_atual * item['Peso']
    alocacao.append({
        "Ativo": item['Ativo'],
        "Sugestão de Compra": real_br(valor_alocado),
        "Peso na Carteira": f"{item['Peso']*100:.0f}%",
        "Risco": item['Risco']
    })

with col_b:
    st.table(pd.DataFrame(alocacao))
with col_a:
    st.markdown(f"""
    <div class='sugestao-card'>
        <strong>INSIGHT DA IA:</strong><br>
        Para bater a inflação de {ipca_at}%, dividimos seu aporte em 
        <strong>40% Proteção</strong>, <strong>30% Renda Fixa</strong> e 
        <strong>30% Aceleração</strong>.
    </div>
    """, unsafe_allow_html=True)

# ABAS
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 PROJEÇÃO 10 ANOS"])

# Cálculo da taxa média ponderada da carteira sugerida
taxa_media_anual = sum([item['Rent_Anual'] * item['Peso'] for item in radar_dados])
taxa_mensal = (1 + (taxa_media_anual/100))**(1/12) - 1

with tab1:
    st.subheader("Evolução Mensal da Carteira Sugerida")
    saldo, logs = 0, []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Rumo à Independência")
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo = renda_alvo / taxa_mensal
    st.markdown(f"**Capital Alvo: {real_br(cap_alvo)}**")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal)
        logs_10.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_10), "Renda Passiva": real_br(saldo_10 * taxa_mensal), "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"})
    st.table(pd.DataFrame(logs_10))
