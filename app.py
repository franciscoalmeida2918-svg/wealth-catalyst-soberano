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
    senha = st.text_input("Chave:", type="password")
    if st.button("Acessar"):
        if senha == "1234#M": st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA DE ATIVOS REAIS (BANCOS DO USUÁRIO)
@st.cache_data(ttl=3600)
def engine_ativos():
    # Dados baseados na sua carteira de bancos e cenário 2026
    return [
        {"Ticker": "CRI/CRA IPCA+ 8.5%", "Banco": "ABC", "Liq_Anual": 16.80},
        {"Ticker": "LCI/LCA 98% CDI", "Banco": "INTER", "Liq_Anual": 12.45},
        {"Ticker": "FII CVBI11 (Papel)", "Banco": "ITAÚ", "Liq_Anual": 13.10},
        {"Ticker": "FII KNIP11 (Inflação)", "Banco": "SANTANDER", "Liq_Anual": 12.80},
        {"Ticker": "Ações Dividendos", "Banco": "SANTANDER", "Liq_Anual": 18.20},
        {"Ticker": "CDB 115% CDI", "Banco": "NUBANK", "Liq_Anual": 11.90},
        {"Ticker": "Tesouro IPCA+", "Banco": "MERCADO PAGO", "Liq_Anual": 12.10}
    ]

df_ativos = pd.DataFrame(engine_ativos())

# 3. SIDEBAR - SALA DE GUERRA
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal Base (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Seleção Estratégica")
escolhidos = st.sidebar.multiselect("Escolha seus títulos (Foco em 3):", 
                                    df_ativos['Ticker'].tolist(), 
                                    default=df_ativos['Ticker'].iloc[:3].tolist())

# CÁLCULO DINÂMICO DE PESOS (RESOLVE O INDEXERROR)
df_sel = df_ativos[df_ativos['Ticker'].isin(escolhidos)].copy()
num_ativos = len(df_sel)

if num_ativos > 0:
    # IA define: maior rentabilidade ganha maior peso automaticamente
    df_sel = df_sel.sort_values(by="Liq_Anual", ascending=False)
    if num_ativos == 1: df_sel['Peso'] = [1.0]
    elif num_ativos == 2: df_sel['Peso'] = [0.6, 0.4]
    elif num_ativos == 3: df_sel['Peso'] = [0.5, 0.3, 0.2]
    else: df_sel['Peso'] = 1/num_ativos # Distribuição igual se passar de 3

    taxa_media_liq = sum(df_sel['Liq_Anual'] * df_sel['Peso'])
    taxa_mensal = (1 + (taxa_media_liq/100))**(1/12) - 1
else:
    taxa_media_liq = 0
    taxa_mensal = 0

# 4. PAINEL ESTRATÉGICO
st.title("🏆 Estrategista IA - Performance Soberana")

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='indicator-box soberano-bg'>TAXA MÉDIA LÍQUIDA<br><h2>{taxa_media_liq:.2f}% a.a.</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='indicator-box' style='background:#a33200'>GANHO REAL (S/ INFLAÇÃO)<br><h2>{(taxa_media_liq - 4.2):.2f}%</h2></div>", unsafe_allow_html=True)
with c3: 
    banco_lider = df_sel['Banco'].iloc[0] if not df_sel.empty else "N/A"
    st.markdown(f"<div class='indicator-box' style='background:#00429d'>BANCO PRIORITÁRIO<br><h2>{banco_lider}</h2></div>", unsafe_allow_html=True)

# 🛡️ VEREDITO DA IA
if not df_sel.empty:
    valor_total_aporte = aporte_acel if datetime.now().month in [6, 12] else aporte_base
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
        Com capital inicial de <strong>{real_br(cap_inicial)}</strong>, execute esta divisão para o aporte de <strong>{real_br(valor_total_aporte)}</strong>:
    """)
    
    for _, row in df_sel.iterrows():
        valor_aloc = valor_total_aporte * row['Peso']
        st.markdown(f"• **{int(row['Peso']*100)}%** em **{row['Ticker']}** no <span class='bank-badge'>{row['Banco']}</span>: {real_br(valor_aloc)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 5. TABELAS DE EXCEL (LÍQUIDO)
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
    capital_meta = renda_alvo / (taxa_mensal if taxa_mensal > 0 else 1)
    st.success(f"Capital Alvo para Independência: {real_br(capital_meta)}")
    
    saldo_h, logs_h = cap_inicial, []
    for ano in range(1, 12):
        for m in range(1, 13):
            aporte = aporte_acel if m in [6, 12] else aporte_base
            saldo_h += aporte + (saldo_h * taxa_mensal)
        progresso = (saldo_h/capital_meta)*100 if capital_meta > 0 else 0
        logs_h.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_h), "Meta (%)": f"{progresso:.1f}%"})
        if saldo_h >= capital_meta:
            st.balloons()
            st.warning(f"🎯 META ALCANÇADA NO ANO {ano}!")
            break
    st.table(pd.DataFrame(logs_h))
