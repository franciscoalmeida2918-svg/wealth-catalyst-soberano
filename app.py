import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA - GRID EXCEL & BLACK OPS
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #0d0d0d; border: 1px solid #333; }
    div[data-testid="stTable"] th { border: 1px solid #444; padding: 12px; text-align: center; background-color: #1a1a1a; color: #00FF88 !important; }
    div[data-testid="stTable"] td { border: 1px solid #333; padding: 10px; text-align: right; color: #FFFFFF !important; }
    
    .indicator-box { padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: 800; border: 1px solid #222; }
    .soberano-bg { background-color: #005f36; border: 1px solid #00FF88; }
    .strategy-card { background: #111; border-left: 5px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; }
    .highlight { color: #00FF88; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SEGURANÇA ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal de Comando")
    if st.text_input("Chave:", type="password") == "1234&Y":
        if st.button("Acessar"): st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA DE ATIVOS (BANCOS: ABC, INTER, ITAU, SANTANDER, MP, NUBANK)
@st.cache_data(ttl=3600)
def engine_ativos():
    return [
        {"Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Liq_Anual": 16.80, "Classe": "Renda Fixa"},
        {"Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Liq_Anual": 12.45, "Classe": "Isento"},
        {"Ticker": "FII CVBI11 (Papel)", "Banco": "ITAÚ", "Liq_Anual": 13.10, "Classe": "FII"},
        {"Ticker": "FII KNIP11 (Inflação)", "Banco": "SANTANDER", "Liq_Anual": 12.80, "Classe": "FII"},
        {"Ticker": "Ações Dividendos", "Banco": "SANTANDER", "Liq_Anual": 18.20, "Classe": "Renda Variável"},
        {"Ticker": "CDB 115% CDI", "Banco": "NUBANK", "Liq_Anual": 11.90, "Classe": "Renda Fixa"},
        {"Ticker": "Tesouro IPCA+", "Banco": "MERCADO PAGO", "Liq_Anual": 12.10, "Classe": "Renda Fixa"}
    ]

df_ativos = pd.DataFrame(engine_ativos())

# 3. SIDEBAR - SALA DE GUERRA
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Seleção Ativa")
escolhidos = st.sidebar.multiselect("Selecione os Títulos (IA dividirá em %):", 
                                    df_ativos['Ticker'].tolist(), 
                                    default=[df_ativos['Ticker'].iloc[0], df_ativos['Ticker'].iloc[2], df_ativos['Ticker'].iloc[1]])

# LÓGICA DE ALOCAÇÃO POR PERFORMANCE
df_sel = df_ativos[df_ativos['Ticker'].isin(escolhidos)].copy()
num = len(df_sel)
if num > 0:
    df_sel = df_sel.sort_values(by="Liq_Anual", ascending=False)
    pesos_map = {1: [1.0], 2: [0.6, 0.4], 3: [0.5, 0.3, 0.2]}
    df_sel['Peso'] = pesos_map.get(num, [1/num]*num)
    taxa_media_liq = sum(df_sel['Liq_Anual'] * df_sel['Peso'])
    taxa_mensal = (1 + (taxa_media_liq/100))**(1/12) - 1
else:
    taxa_media_liq = taxa_mensal = 0

# 4. PAINEL DE COMANDO
st.title("🏆 Estrategista IA - Performance Soberana")

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='indicator-box soberano-bg'>TAXA MÉDIA LÍQUIDA<br><h2>{taxa_media_liq:.2f}% a.a.</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='indicator-box' style='background:#a33200'>GANHO REAL (S/ INFLAÇÃO)<br><h2>{(taxa_media_liq - 4.2):.2f}%</h2></div>", unsafe_allow_html=True)
with c3: 
    banco_top = df_sel['Banco'].iloc[0] if num > 0 else "---"
    st.markdown(f"<div class='indicator-box' style='background:#00429d'>ALOCAÇÃO PRIORITÁRIA<br><h2>{banco_top}</h2></div>", unsafe_allow_html=True)

# 🛡️ VEREDITO DA IA
if num > 0:
    val_aporte = aporte_acel if datetime.now().month in [6, 12] else aporte_base
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
        Para o aporte de <span class='highlight'>{real_br(val_aporte)}</span> com capital inicial de <span class='highlight'>{real_br(cap_inicial)}</span>:
    """)
    for _, row in df_sel.iterrows():
        st.markdown(f"• **{int(row['Peso']*100)}%** em **{row['Ticker']}** no <span class='bank-badge'>{row['Banco']}</span>: <span class='highlight'>{real_br(val_aporte * row['Peso'])}</span>")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. TABELAS ESTILO EXCEL
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 PLANO HACKING 10 ANOS"])

with tab1:
    saldo, logs = cap_inicial, []
    for m in range(1, 13):
        ap = aporte_acel if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += ap + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(ap), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    r_alvo = st.number_input("Renda Mensal Alvo (R$):", value=5000.0)
    meta_cap = r_alvo / (taxa_mensal if taxa_mensal > 0 else 1)
    st.success(f"Capital para Independência: {real_br(meta_cap)}")
    
    saldo_h, logs_h = cap_inicial, []
    for ano in range(1, 12):
        for m in range(1, 13):
            ap = aporte_acel if m in [6, 12] else aporte_base
            saldo_h += ap + (saldo_h * taxa_mensal)
        logs_h.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_h), "Meta (%)": f"{(saldo_h/meta_cap)*100:.1f}%"})
        if saldo_h >= meta_cap:
            st.warning(f"🎯 META ATINGIDA NO ANO {ano}!")
            break
    st.table(pd.DataFrame(logs_h))
