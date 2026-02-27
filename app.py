import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# 1. ESTÉTICA SOBERANA - ALTA PERFORMANCE
st.set_page_config(page_title="Dr. Strategist IA - AGRESSIVA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .ia-response { background: #001a0d; border: 2px solid #00FF88; padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 0 20px rgba(0,255,136,0.2); }
    .highlight { color: #00FF88; font-weight: 800; }
    .strategy-tag { background: #00FF88; color: #000; padding: 4px 10px; border-radius: 5px; font-weight: bold; font-size: 0.9rem; }
    div[data-testid="stTable"] table { border: 1px solid #1f1f1f; }
    div[data-testid="stTable"] th { background-color: #0d0d0d; color: #00FF88 !important; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURANÇA SOBERANA ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal Dr. Strategist - ACESSO RESTRITO")
    if st.text_input("Senha Mestra:", type="password") == "102&030":
        if st.button("ATIVAR ALAVANCAGEM"): st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE DADOS EM TEMPO REAL (MARKET INTELLIGENCE)
@st.cache_data(ttl=3600)
def get_live_data():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except: return 13.25, 4.50

selic, ipca = get_live_data()

# 3. 🕹️ SALA DE GUERRA (PARÂMETROS SOBERANOS)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=10000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2800.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

# 4. A SENTINELA: IA COM DOUTORADO E ALAVANCAGEM (MODELO FILHA)
def process_sovereign_logic(query, cap, base, acel, selic, ipca):
    # Simulação de carteira agressiva: 60% ABC (CRI/CRA), 40% Inter/Itaú (LCI/FII)
    # Taxa Alvo Agressiva: IPCA + 9% ou 120% CDI
    taxa_alvo = 17.20 
    taxa_mensal = (1 + (taxa_alvo/100))**(1/12) - 1
    
    # Simulação de 10 anos para resposta contextual
    saldo_10y = cap
    for m in range(1, 121):
        ap = acel if m % 12 == 0 else base # Aporte acelerado no fim do ano
        saldo_10y = (saldo_10y + ap) * (1 + taxa_mensal)

    return f"""
    <div class='ia-response'>
        <span class='strategy-tag'>ESTRATÉGIA AGRESSIVA ATIVA</span><br><br>
        <b>PARECER TÉCNICO:</b> Detectei oportunidade de alavancagem disparada. <br>
        Com SELIC a {selic}% e IPCA a {ipca}%, o foco é <b>crédito privado isento</b> no <span class='highlight'>Banco ABC</span>. <br><br>
        <b>CÁLCULO DE ALAVANCAGEM:</b> <br>
        • Valor Futuro (10 anos): <span class='highlight'>R$ {saldo_10y:,.2f}</span> líquido. <br>
        • Ganho Real: <span class='highlight'>{(taxa_alvo - ipca):.2f}% a.a.</span> (Blindagem total contra inflação). <br><br>
        <i>IA Sentinela aprendeu: Você busca o caminho mais rápido para a meta. Sugestão: Reinvestir 100% dos dividendos dos FIIs no Itaú imediatamente para compor o Mês 02.</i>
    </div>
    """

# 5. INTERFACE DO ORÁCULO
st.title("👨‍🔬 Dr. Strategist - IA de Alavancagem Disparada")
st.write(f"Conexão: **Soberana** | Modo: **Agressivo** | Alvo: **Minimizar Tempo**")

comando = st.text_input("Ordene um cálculo ou peça uma estratégia (Ex: Calcule minha alavancagem):")

if comando:
    st.markdown(process_sovereign_logic(comando, cap_inicial, aporte_base, aporte_acel, selic, ipca), unsafe_allow_html=True)

# 6. TABELA EXCEL: O RESULTADO DA TOMADA DE DECISÃO
st.divider()
st.subheader("📊 Cronograma de Alavancagem Disparada (Visão Líquida)")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

t_mensal = (1 + (17.20/100))**(1/12) - 1
saldo_h = cap_inicial
logs = []

# Mês 00
logs.append({"Mês": "Mês 00", "Aporte": real_br(0), "Lucro Líquido": real_br(0), "Patrimônio": real_br(saldo_h)})

for m in range(1, 13):
    # Aporte de aceleração no final do ano (mês 12)
    ap = aporte_acel if m == 12 else aporte_base
    lucro = saldo_h * t_mensal
    saldo_h += ap + lucro
    logs.append({
        "Mês": f"Mês {m:02d}",
        "Aporte": real_br(ap),
        "Lucro Líquido": real_br(lucro),
        "Patrimônio": real_br(saldo_h)
    })

st.table(pd.DataFrame(logs))
