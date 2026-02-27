import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA - GRID EXCEL DEFINIDO
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #0d0d0d; border: 1px solid #333; }
    div[data-testid="stTable"] th { border: 1px solid #444; padding: 12px; text-align: center; background-color: #1a1a1a; color: #00FF88 !important; }
    div[data-testid="stTable"] td { border: 1px solid #333; padding: 10px; text-align: right; color: #FFFFFF !important; }
    
    .indicator-box { padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: 800; border: 1px solid #222; }
    .soberano-bg { background-color: #005f36; border: 1px solid #00FF88; }
    .strategy-card { background: #111; border-left: 5px solid #00FF88; padding: 20px; border-radius: 5px; margin: 15px 0; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; }
    </style>
""", unsafe_allow_html=True)

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SEGURANÇA ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal de Comando")
    if st.text_input("Chave:", type="password") == "1234@T":
        if st.button("Acessar"): st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA DE TÍTULOS REAIS (SISTEMA DE INDICAÇÃO)
@st.cache_data(ttl=3600)
def engine_ativos():
    # Simulando busca em tempo real nos bancos do usuário para 2026
    return [
        {"Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Tipo": "CRI/CRA", "Liq_Anual": 16.80},
        {"Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Tipo": "LCI/LCA", "Liq_Anual": 12.45},
        {"Ticker": "CVBI11 / KNIP11", "Banco": "ITAÚ/SANTANDER", "Tipo": "FIIs", "Liq_Anual": 13.10},
        {"Ticker": "Ações Dividendos", "Banco": "SANTANDER/XP", "Tipo": "Ações", "Liq_Anual": 18.20},
        {"Ticker": "CDB 115% CDI", "Banco": "NUBANK/M.PAGO", "Tipo": "CDB", "Liq_Anual": 11.90}
    ]

ativos_disponiveis = engine_ativos()
df_ativos = pd.DataFrame(ativos_disponiveis)

# 3. SIDEBAR - SALA DE GUERRA (INTEGRADA)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal Base (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Seleção de Títulos")
escolhidos = st.sidebar.multiselect("Selecione até 3 Títulos para a Carteira:", 
                                    df_ativos['Ticker'].tolist(), 
                                    default=[df_ativos['Ticker'].iloc[0], df_ativos['Ticker'].iloc[1]])

# Filtro de Estratégia
df_selecionados = df_ativos[df_ativos['Ticker'].isin(escolhidos)]
if not df_selecionados.empty:
    taxa_media_liq = df_selecionados['Liq_Anual'].mean()
    taxa_mensal = (1 + (taxa_media_liq/100))**(1/12) - 1
else:
    taxa_media_liq = 0
    taxa_mensal = 0

# 4. PAINEL ESTRATÉGICO DE GANHOS LÍQUIDOS
st.title("🏆 Estrategista IA - Performance Soberana")

# Indicadores de Topo
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='indicator-box soberano-bg'>TAXA MÉDIA LÍQUIDA<br><h2>{taxa_media_liq:.2f}% a.a.</h2></div>", unsafe_allow_html=True)
with c2: 
    ipca_est = 4.20
    st.markdown(f"<div class='indicator-box' style='background:#a33200'>GANHO REAL (S/ INFLAÇÃO)<br><h2>{(taxa_media_liq - ipca_est):.2f}%</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='indicator-box' style='background:#00429d'>BANCO LÍDER DO MÊS<br><h2>{df_selecionados['Banco'].iloc[0] if not df_selecionados.empty else 'N/A'}</h2></div>", unsafe_allow_html=True)

# 🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO
if not df_selecionados.empty:
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
        Com capital inicial de <strong>{real_br(cap_inicial)}</strong>, sua execução estratégica é:
    """)
    
    # Distribuição Dinâmica baseada nos selecionados
    pesos = [0.5, 0.3, 0.2] if len(df_selecionados) >= 3 else [0.6, 0.4] if len(df_selecionados) == 2 else [1.0]
    valor_total_aporte = aporte_acel if datetime.now().month in [6, 12] else aporte_base
    
    for i, (idx, row) in enumerate(df_selecionados.iterrows()):
        valor_aloc = valor_total_aporte * pesos[i]
        st.markdown(f"• **{int(pesos[i]*100)}%** em **{row['Ticker']}** no <span class='bank-badge'>{row['Banco']}</span>: {real_br(valor_aloc)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 5. TABELAS DE RESULTADOS
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 PLANO HACKING 10 ANOS"])

with tab1:
    saldo, logs = cap_inicial, []
    for m in range(1, 13):
        aporte = aporte_acel if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    capital_meta = renda_alvo / taxa_mensal
    st.success(f"Capital Alvo para Independência: {real_br(capital_meta)}")
    
    saldo_h, logs_h = cap_inicial, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_acel if m in [6, 12] else aporte_base
            saldo_h += aporte + (saldo_h * taxa_mensal)
        progresso = (saldo_h/capital_meta)*100
        logs_h.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_h), "Meta (%)": f"{progresso:.1f}%"})
        if saldo_h >= capital_meta:
            st.balloons()
            st.warning(f"🎯 META ALCANÇADA NO ANO {ano}!")
            break
    st.table(pd.DataFrame(logs_h))
