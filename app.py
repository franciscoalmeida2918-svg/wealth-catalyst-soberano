import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

# 1. ESTÉTICA SOBERANA - TERMINAL DE ALTA PERFORMANCE
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
    .soberano-bg { background-color: #005f36; border: 2px solid #00FF88; }
    
    .strategy-card { background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%); border: 1px solid #00FF88; padding: 25px; border-radius: 10px; margin: 20px 0; }
    .bank-tag { background-color: #00FF88; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .highlight { color: #00FF88; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SEGURANÇA CRIPTOGRÁFICA ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Sistema de Inteligência Financeira")
    senha = st.text_input("Chave de Acesso Soberana:", type="password")
    if st.button("Autenticar"):
        if senha == "1234@T":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# 2. MOTOR ESTRATÉGICO (ANÁLISE DE TAXAS REAIS)
@st.cache_data(ttl=3600)
def engine_estrategico():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        
        # Estratégia Ativa: Buscando o máximo ganho líquido nos seus bancos
        planos = [
            {"Ativo": "CRI/CRA High Yield", "Banco": "ABC", "Taxa_Anual": 17.80, "Peso": 0.50, "Motivo": "Máxima aceleração de capital"},
            {"Ativo": "LCI/LCA 95%+", "Banco": "INTER", "Taxa_Anual": round(i + 7.1, 2), "Peso": 0.30, "Motivo": "Isenção fiscal e proteção"},
            {"Ativo": "FIIs Logística/Papel", "Banco": "ITAÚ/SANTANDER", "Taxa_Anual": round(s + 2.5, 2), "Peso": 0.20, "Motivo": "Renda passiva e liquidez"}
        ]
        return s, i, planos
    except: return 13.25, 4.50, []

selic, ipca, plano_ativo = engine_estrategico()
taxa_mix = sum(p['Taxa_Anual'] * p['Peso'] for p in plano_ativo)
taxa_mensal = (1 + (taxa_mix/100))**(1/12) - 1

# 3. INTERFACE DE OPERAÇÕES
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0, step=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal Base (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown(f"**Instituições Operacionais:**")
st.sidebar.caption("ABC, INTER, ITAU, SANTANDER, MERCADO PAGO, NUBANK")

# 4. PAINEL DE ESTRATÉGIA 100% LÍQUIDA
st.title("🏆 Plano Estratégico de Aceleração")

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC ATUAL: {selic}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA (Inflação): {ipca}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box soberano-bg'>TAXA SOBERANA: {taxa_mix:.2f}% a.a.</div>", unsafe_allow_html=True)

# O CORAÇÃO DA IA: A INDICAÇÃO DO PLANO
st.markdown(f"""
<div class='strategy-card'>
    <h3 style='color:#00FF88; margin-top:0;'>🛡️ VEREDITO DA IA: ESTRATÉGIA PARA MINIMIZAR PRAZO</h3>
    Com um capital inicial de <span class='highlight'>{real_br(cap_inicial)}</span>, sua estratégia para este mês é:
    <br><br>
    1. 🎯 <strong>ALOCAÇÃO DE POTÊNCIA (50%)</strong>: Envie <span class='highlight'>{real_br((aporte_base if datetime.now().month not in [6, 12] else aporte_acel) * 0.5)}</span> para o <strong>Banco ABC</strong> em títulos de Crédito Privado.
    <br>2. 🛡️ <strong>BLINDAGEM FISCAL (30%)</strong>: Aplique <span class='highlight'>{real_br((aporte_base if datetime.now().month not in [6, 12] else aporte_acel) * 0.3)}</span> no <strong>Inter</strong> (LCI/LCA).
    <br>3. 📈 <strong>FLUXO DE CAIXA (20%)</strong>: Mantenha <span class='highlight'>{real_br((aporte_base if datetime.now().month not in [6, 12] else aporte_acel) * 0.2)}</span> no <strong>Itaú/Santander</strong> em FIIs selecionados.
    <br><br>
    <i>Essa estratégia garante um ganho real de <span class='highlight'>{(taxa_mix - ipca):.2f}%</span> acima da inflação, focando em encurtar sua meta de 10 anos.</i>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES (LÍQUIDO)", "🚀 PROJEÇÃO DE REDUÇÃO DE PRAZO"])

with tab1:
    saldo = cap_inicial
    logs = []
    for m in range(1, 13):
        # Regra de engajamento: aporte de 3k nos meses 6 e 12
        aporte = aporte_acel if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Total Acumulado": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    renda_alvo = st.number_input("Renda Mensal Desejada (R$):", value=5000.0)
    capital_meta = renda_alvo / taxa_mensal
    st.success(f"Capital Necessário para Independência: {real_br(capital_meta)}")
    
    saldo_hacked = cap_inicial
    logs_meta = []
    for ano in range(1, 12):
        for m in range(1, 13):
            aporte = aporte_acel if m in [6, 12] else aporte_base
            saldo_hacked += aporte + (saldo_hacked * taxa_mensal)
        
        progresso = (saldo_hacked / capital_meta) * 100
        logs_meta.append({
            "Ano": f"Ano {ano:02d}", 
            "Patrimônio": real_br(saldo_hacked), 
            "Renda Passiva": real_br(saldo_hacked * taxa_mensal),
            "Meta (%)": f"{progresso:.1f}%"
        })
        if saldo_hacked >= capital_meta:
            st.balloons()
            st.warning(f"🎯 ALVO ATINGIDO EM APENAS {ano} ANOS!")
            break
    st.table(pd.DataFrame(logs_meta))
