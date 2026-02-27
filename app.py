import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

# 1. ESTÉTICA SOBERANA - BLACK OPS & GRID EXCEL
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #0d0d0d; border: 1px solid #333; }
    div[data-testid="stTable"] th { border: 1px solid #444; padding: 12px; text-align: center; background-color: #1a1a1a; color: #00FF88 !important; font-weight: bold; }
    div[data-testid="stTable"] td { border: 1px solid #333; padding: 10px; text-align: right; color: #FFFFFF !important; }
    
    .indicator-box { padding: 25px; border-radius: 15px; text-align: center; color: white; font-weight: 800; font-size: 1.2rem; margin-bottom: 15px; border: 1px solid #222; }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .alvo-bg { background-color: #005f36; }
    
    .strategy-card { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 5px solid #00FF88; padding: 20px; border-radius: 5px; margin: 15px 0; }
    .bank-tag { background-color: #222; padding: 3px 10px; border-radius: 6px; font-size: 0.85rem; color: #00FF88; font-weight: bold; border: 1px solid #00FF88; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SISTEMA DE SEGURANÇA REFORÇADO (CYBER DEFENSE) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Terminal Soberano - Acesso Restrito")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.warning("⚠️ Terminal Criptografado")
        user_key = st.text_input("Chave de Comando Nível 1:", type="password")
        if st.button("Validar Identidade"):
            if user_key == "12@3%4":
                with st.spinner("Verificando protocolos de segurança..."):
                    time.sleep(1.5)
                    st.session_state.autenticado = True
                    st.rerun()
            else:
                st.error("ACESSO NEGADO: Chave inválida.")
    st.stop()

# 2. MOTOR DE INTELIGÊNCIA (ALOCAÇÃO BASEADA NOS SEUS BANCOS)
@st.cache_data(ttl=3600)
def scanner_estrategico():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        
        # Estratégia distribuída nos SEUS bancos informados
        radar = [
            {"Ativo": "Crédito Privado (CRI/CRA)", "Rent_Anual": 17.5, "Peso": 0.50, "Banco": "Banco ABC"}, 
            {"Ativo": "LCI/LCA (Isento)", "Rent_Anual": round(i + 6.8, 2), "Peso": 0.30, "Banco": "Banco INTER"}, 
            {"Ativo": "CDB/FIIs", "Rent_Anual": round(s * 1.1, 2), "Peso": 0.20, "Banco": "ITAÚ/SANTANDER"} 
        ]
        return s, i, radar
    except: return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = scanner_estrategico()
df_radar = pd.DataFrame(radar_dados)

# 3. SIDEBAR - CONTROLE DE OPERAÇÕES
st.sidebar.title("🕹️ Comando Central")
if st.sidebar.button("🔴 Bloquear Terminal"):
    st.session_state.autenticado = False
    st.rerun()

cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=0.0)
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown("### 🏦 Ecossistema Bancário")
st.sidebar.info("Bancos Ativos: ABC, INTER, ITAU, SANTANDER, MERCADO PAGO, NUBANK")

# 4. TAXA SOBERANA E ALOCAÇÃO
taxa_ponderada_anual = sum(item['Rent_Anual'] * item['Peso'] for item in radar_dados)
taxa_mensal_soberana = (1 + (taxa_ponderada_anual/100))**(1/12) - 1
valor_atual = aporte_extra if datetime.now().month in [6, 12] else aporte_base

# 5. PAINEL SOBERANO
st.title("🏆 Estratégia de Minimização de Prazo")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box ifil-bg' style='background-color:#6a1b9a'>MIX LÍQUIDO: {taxa_ponderada_anual:.2f}%</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='indicator-box alvo-bg'>GANHO REAL: {(taxa_ponderada_anual - ipca_at):.2f}%</div>", unsafe_allow_html=True)

# CARD TÁTICO DE ALOCAÇÃO
st.markdown(f"""
<div class='strategy-card'>
    <h3 style='color:#00FF88; margin-top:0;'>🛡️ DISTRIBUIÇÃO ESTRATÉGICA DE APORTE</h3>
    Para bater a meta antes de 10 anos, divida seu capital de <strong>{real_br(valor_atual)}</strong>:
    <div style='margin-top:15px;'>
        • 50% em <strong>{radar_dados[0]['Ativo']}</strong> na <span class='bank-tag'>{radar_dados[0]['Banco']}</span>: {real_br(valor_atual * 0.5)} <br><br>
        • 30% em <strong>{radar_dados[1]['Ativo']}</strong> no <span class='bank-tag'>{radar_dados[1]['Banco']}</span>: {real_br(valor_atual * 0.3)} <br><br>
        • 20% em <strong>{radar_dados[2]['Ativo']}</strong> no <span class='bank-tag'>{radar_dados[2]['Banco']}</span>: {real_br(valor_atual * 0.2)}
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 ACELERAÇÃO DE META"])

with tab1:
    saldo = cap_inicial
    logs = []
    for m in range(1, 13):
        aporte = 3000 if m in [6, 12] else 2500
        lucro = saldo * taxa_mensal_soberana
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    capital_meta = renda_alvo / taxa_mensal_soberana
    st.success(f"Capital Alvo: {real_br(capital_meta)}")
    
    saldo_10 = cap_inicial
    logs_10 = []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = 3000 if m in [6, 12] else 2500
            saldo_10 += aporte + (saldo_10 * taxa_mensal_soberana)
        
        logs_10.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_10), "Progresso": f"{(saldo_10/capital_meta)*100:.1f}%"})
        if saldo_10 >= capital_meta:
             st.warning(f"🎯 Meta atingida no ANO {ano}!")
             break
    st.table(pd.DataFrame(logs_10))
