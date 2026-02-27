import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA - BLACK OPS & NEON
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #0d0d0d; border: 1px solid #333; }
    div[data-testid="stTable"] th { border: 1px solid #444; padding: 12px; background-color: #1a1a1a; color: #00FF88 !important; }
    div[data-testid="stTable"] td { border: 1px solid #333; padding: 10px; text-align: right; color: #FFFFFF !important; }
    .indicator-box { padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: 800; border: 1px solid #222; }
    .soberano-bg { background-color: #005f36; border: 1px solid #00FF88; }
    .alert-card { background: rgba(255, 75, 75, 0.1); border: 1px solid #FF4B4B; padding: 15px; border-radius: 10px; margin: 10px 0; color: #FF4B4B; font-weight: bold; }
    .strategy-card { background: #111; border-left: 5px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .highlight { color: #00FF88; font-weight: bold; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    
    /* Customização Neon da Sidebar */
    div[data-testid="stMultiselect"] > div > div > div { background-color: #1a1a1a !important; border: 1px solid #00FF88 !important; color: #00FF88 !important; }
    </style>
""", unsafe_allow_html=True)

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SEGURANÇA ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal de Comando IA")
    if st.text_input("Chave Soberana:", type="password") == "1234+%":
        if st.button("Acessar"): st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE DADOS DE MERCADO
@st.cache_data(ttl=3600)
def get_market_data():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except: return 13.25, 4.50

selic, ipca = get_market_data()

# 3. 🕹️ SALA DE GUERRA (INTERFACE DE CONTROLE)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0, step=500.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0, step=100.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0, step=100.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Ativos nos seus Bancos")
ativos = [
    {"Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Taxa": 16.80, "Peso": 0.50},
    {"Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Taxa": 12.45, "Peso": 0.30},
    {"Ticker": "FII CVBI11 / KNIP11", "Banco": "ITAÚ/SAN", "Taxa": 13.10, "Peso": 0.20},
    {"Ticker": "CDB Reserva 100% CDI", "Banco": "NUBANK/MP", "Taxa": 11.20, "Peso": 0.0} # Banco para arbitragem
]
escolhidos = st.sidebar.multiselect("Filtrar Títulos Ativos:", [a['Ticker'] for a in ativos if a['Peso'] > 0], default=[a['Ticker'] for a in ativos if a['Peso'] > 0])

# 4. LÓGICA DE ARBITRAGEM (IA ANALISA O PIOR BANCO)
df_total = pd.DataFrame(ativos)
banco_vencedor = df_total.loc[df_total['Taxa'].idxmax()]
banco_perdedor = df_total.loc[df_total['Taxa'].idxmin()]

# 5. CÁLCULO DE ESTRATÉGIA LÍQUIDA
df_sel = df_total[df_total['Ticker'].isin(escolhidos)].copy()
if not df_sel.empty:
    df_sel['Peso_Adj'] = df_sel['Peso'] / df_sel['Peso'].sum()
    taxa_anual = sum(df_sel['Taxa'] * df_sel['Peso_Adj'])
    taxa_mensal = (1 + (taxa_anual/100))**(1/12) - 1
else:
    taxa_anual = taxa_mensal = 0

# 6. PAINEL DE CONTROLE
st.title("🏆 Estrategista IA - Arbitragem Soberana")

# Alerta de Arbitragem se houver gap grande entre bancos
if (banco_vencedor['Taxa'] - banco_perdedor['Taxa']) > 3:
    st.markdown(f"""
    <div class='alert-card'>
        🚨 ALERTA DE ARBITRAGEM: O banco <span style='text-decoration:underline'>{banco_perdedor['Banco']}</span> está rendendo {banco_perdedor['Taxa']}% (Líquido). 
        Recomendação IA: Mover capital para o banco <span style='text-decoration:underline'>{banco_vencedor['Banco']}</span> ({banco_vencedor['Taxa']}%) para ganhar +{(banco_vencedor['Taxa'] - banco_perdedor['Taxa']):.2f}% ao ano.
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box soberano-bg'>TAXA MÉDIA LÍQUIDA<br><h2>{taxa_anual:.2f}% a.a.</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box' style='background:#a33200'>GANHO REAL (VS IPCA)<br><h2>{(taxa_anual - ipca):.2f}%</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box' style='background:#00429d'>CAPITAL INICIAL<br><h2>{real_br(cap_inicial)}</h2></div>", unsafe_allow_html=True)

# 🛡️ VEREDITO DA IA
if not df_sel.empty:
    val_atual = aporte_acel if datetime.now().month in [6, 12] else aporte_base
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
        Capital Inicial de <span class='highlight'>{real_br(cap_inicial)}</span> recalculado. Divisão do aporte de <span class='highlight'>{real_br(val_atual)}</span>:
        <br><br>
    """, unsafe_allow_html=True)
    for _, row in df_sel.iterrows():
        st.markdown(f"• **{int(row['Peso_Adj']*100)}%** em **{row['Ticker']}** no <span class='bank-badge'>{row['Banco']}</span>: <span class='highlight'>{real_br(val_atual * row['Peso_Adj'])}</span><br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 7. TABELAS DE RESULTADOS (EXCEL STYLE)
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 HACKING 10 ANOS"])

with tab1:
    saldo = cap_inicial
    logs = []
    # Log Inicial
    logs.append({"Mês": "Mês 00", "Aporte": real_br(0), "Lucro Líquido": real_br(0), "Patrimônio": real_br(saldo)})
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
    
    saldo_h = cap_inicial
    logs_h = []
    for ano in range(1, 12):
        for m in range(1, 13):
            ap = aporte_acel if m in [6, 12] else aporte_base
            saldo_h += ap + (saldo_h * taxa_mensal)
        
        logs_h.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_h), "Meta (%)": f"{(saldo_h/capital_meta)*100:.1f}%"})
        if saldo_h >= capital_meta:
            st.balloons(); st.warning(f"🎯 META ALCANÇADA NO ANO {ano}!"); break
    st.table(pd.DataFrame(logs_h))
