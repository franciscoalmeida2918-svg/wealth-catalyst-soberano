import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #0d0d0d; border: 1px solid #333; }
    div[data-testid="stTable"] th { border: 1px solid #444; padding: 12px; background-color: #1a1a1a; color: #00FF88 !important; }
    div[data-testid="stTable"] td { border: 1px solid #333; padding: 10px; text-align: right; color: #FFFFFF !important; }
    .indicator-box { padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: 800; border: 1px solid #222; }
    .soberano-bg { background-color: #005f36; border: 1px solid #00FF88; }
    .strategy-card { background: #111; border-left: 5px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .highlight { color: #00FF88; font-weight: bold; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    
    /* Tags Verde Neon na Sidebar */
    div[data-testid="stMultiselect"] > div > div > div { background-color: #1a1a1a !important; border: 1px solid #00FF88 !important; color: #00FF88 !important; }
    </style>
""", unsafe_allow_html=True)

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# 2. MOTOR DE DADOS EM TEMPO REAL
@st.cache_data(ttl=3600)
def get_market_data():
    try:
        selic = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        ipca = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return selic, ipca
    except: return 13.25, 4.50

selic_at, ipca_at = get_market_data()

# 3. 🕹️ SALA DE GUERRA (SIDEBAR - CONTROLE TOTAL)
st.sidebar.title("🕹️ Sala de Guerra")
# O Recálculo acontece aqui: sempre que o estado desses inputs muda, o script roda de cima a baixo
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0, step=500.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0, step=100.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0, step=100.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Ativos nos seus Bancos")
lista_ativos = [
    {"ID": "ABC_CRI", "Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Taxa": 16.80, "Peso": 0.50},
    {"ID": "INTER_LCI", "Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Taxa": 12.45, "Peso": 0.30},
    {"ID": "ITAU_FII", "Ticker": "FII CVBI11", "Banco": "ITAÚ", "Taxa": 13.10, "Peso": 0.20}
]
escolhidos = st.sidebar.multiselect("Selecione para Ativar:", [a['Ticker'] for a in lista_ativos], default=[a['Ticker'] for a in lista_ativos])

# 4. LÓGICA DE RECÁLCULO DE PERFORMANCE
df_ativos = pd.DataFrame([a for a in lista_ativos if a['Ticker'] in escolhidos])

if not df_ativos.empty:
    # Ajuste de peso proporcional caso tire algum ativo
    df_ativos['Peso_Adj'] = df_ativos['Peso'] / df_ativos['Peso'].sum()
    taxa_anual_liq = sum(df_ativos['Taxa'] * df_ativos['Peso_Adj'])
    taxa_mensal = (1 + (taxa_anual_liq/100))**(1/12) - 1
else:
    taxa_anual_liq = taxa_mensal = 0

# 5. PAINEL DE CONTROLE E VEREDITO
st.title("🏆 Estrategista IA - Performance Soberana")

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box soberano-bg'>TAXA MÉDIA LÍQUIDA<br><h2>{taxa_anual_liq:.2f}% a.a.</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box' style='background:#a33200'>GANHO REAL ACIMA IPCA<br><h2>{(taxa_anual_liq - ipca_at):.2f}%</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box' style='background:#00429d'>CAPITAL INICIAL ATIVO<br><h2>{real_br(cap_inicial)}</h2></div>", unsafe_allow_html=True)

# 🛡️ VEREDITO DA IA COM RECÁLCULO DINÂMICO
if not df_ativos.empty:
    val_atual = aporte_acel if datetime.now().month in [6, 12] else aporte_base
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
        Baseado no seu Capital Inicial de <span class='highlight'>{real_br(cap_inicial)}</span>, execute hoje:
        <br><br>
    """, unsafe_allow_html=True)
    
    for _, row in df_ativos.iterrows():
        st.markdown(f"• **{int(row['Peso_Adj']*100)}%** em **{row['Ticker']}** no <span class='bank-badge'>{row['Banco']}</span>: <span class='highlight'>{real_br(val_atual * row['Peso_Adj'])}</span> <br><br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 6. TABELAS DE RESULTADOS (EXCEL STYLE)
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 HACKING 10 ANOS"])

with tab1:
    saldo = cap_inicial
    logs = []
    for m in range(1, 13):
        ap = aporte_acel if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += ap + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(ap), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    renda_alvo = st.number_input("Renda Mensal Desejada (R$):", value=5000.0)
    capital_meta = renda_alvo / (taxa_mensal if taxa_mensal > 0 else 1)
    st.success(f"Capital Alvo para Independência: {real_br(capital_meta)}")
    
    saldo_meta = cap_inicial
    logs_meta = []
    for ano in range(1, 12):
        for m in range(1, 13):
            ap = aporte_extra if m in [6, 12] else aporte_base # Usando lógica de aceleração
            saldo_meta += ap + (saldo_meta * taxa_mensal)
        
        logs_meta.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_meta), "Progresso Meta": f"{(saldo_meta/capital_meta)*100:.1f}%"})
        if saldo_meta >= capital_meta:
            st.balloons(); st.warning(f"🎯 META ALCANÇADA NO ANO {ano}!"); break
    st.table(pd.DataFrame(logs_meta))
