import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# 1. ESTÉTICA DE ALTA FIDELIDADE (CÉREBRO DR. IA)
st.set_page_config(page_title="Dr. Strategist IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .dr-card { background: #0a0a0a; border: 1px solid #00FF88; padding: 25px; border-radius: 10px; border-left: 10px solid #00FF88; margin: 20px 0; }
    .metric-box { background: #111; border: 1px solid #222; padding: 20px; border-radius: 10px; text-align: center; }
    .highlight { color: #00FF88; font-weight: 800; font-size: 1.2em; }
    div[data-testid="stTable"] table { border: 1px solid #333; width: 100%; }
    div[data-testid="stTable"] th { background-color: #111; color: #00FF88 !important; padding: 15px; }
    div[data-testid="stTable"] td { background-color: #000; color: #FFF !important; padding: 12px; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURANÇA SOBERANA ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Terminal Dr. Strategist - Autenticação")
    if st.text_input("Chave Mestra:", type="password") == "102030":
        if st.button("INICIALIZAR CÉREBRO"): st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE CÁLCULO E DADOS (API BANCO CENTRAL)
@st.cache_data(ttl=3600)
def get_market_metrics():
    try:
        selic = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        ipca = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return selic, ipca
    except: return 13.25, 4.50

selic_atual, ipca_atual = get_market_metrics()

# 3. SALA DE GUERRA (PARÂMETROS DE ENTRADA)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=1000.0, step=1000.0)
aporte_regular = st.sidebar.number_input("Aporte Base (R$):", value=2500.0)
aporte_acelerador = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

# 4. A SENTINELA: MOTOR DE ESTRATÉGIA E MATEMÁTICA AVANÇADA
def solver_ia(comando, cap, base, acel, selic, ipca):
    comando = comando.lower()
    # Simulação de Taxa Soberana (Alvo: Sempre IPCA + 8% ou 115% CDI)
    taxa_alvo_anual = 16.85 
    taxa_mensal = (1 + (taxa_alvo_anual/100))**(1/12) - 1
    ganho_real = taxa_alvo_anual - ipca
    
    if "calcul" in comando or "quanto" in comando or "projeção" in comando:
        # Cálculo Aritmético Avançado de Juros Compostos
        meses = 120 # Foco na meta de 10 anos
        patrimonio = cap
        for m in range(1, meses + 1):
            ap = acel if m % 6 == 0 else base # Aceleração semestral
            patrimonio = (patrimonio + ap) * (1 + taxa_mensal)
        
        return f"""
        <div class='dr-card'>
            <b>VEREDITO DO DR. STRATEGIST:</b><br>
            Executando cálculos de aritmética financeira avançada... <br><br>
            • <b>Estratégia:</b> Alavancagem disparada via <span class='highlight'>Crédito Privado (ABC) e FIIs de Papel (Itaú)</span>.<br>
            • <b>Taxa Soberana:</b> {taxa_alvo_anual}% a.a. | <b>Ganho Real:</b> <span class='highlight'>{ganho_real:.2f}% acima da inflação</span>.<br>
            • <b>Projeção 10 Anos:</b> Seu patrimônio líquido final estimado é de <span class='highlight'>R$ {patrimonio:,.2f}</span>.<br><br>
            <i>Informação limpa: O mercado hoje favorece o prefixado longo devido à curva futura da Selic.</i>
        </div>
        """
    return "<div class='dr-card'>Aguardando comando técnico para processamento de dados.</div>"

# 5. INTERFACE DE COMANDO
st.title("👨‍🔬 Dr. Strategist - IA de Investimentos")
st.write(f"Conectado ao Dr. IA Central | Status: **Soberano** | Ganho Real Alvo: **> 10% a.a.**")

comando_user = st.text_input("Insira sua dúvida ou solicitação de cálculo (Ex: Calcule minha alavancagem para 5 anos):")

if comando_user:
    st.markdown(solver_ia(comando_user, cap_inicial, aporte_regular, aporte_acel, selic_atual, ipca_atual), unsafe_allow_html=True)

# 6. TABELA DE TOMADA DE DECISÃO (EXCEL STYLE)
st.divider()
st.subheader("📊 Cronograma de Crescimento Disparado (Net Value)")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

t_anual = 16.85
t_mensal = (1 + (t_anual/100))**(1/12) - 1
saldo = cap_inicial
data_table = []

for m in range(1, 13):
    ap = aporte_acelerador if m in [6, 12] else aporte_regular
    lucro = saldo * t_mensal
    saldo += ap + lucro
    data_table.append({
        "Mês": f"Mês {m:02d}",
        "Aporte Líquido": real_br(ap),
        "Lucro Real (Líquido)": real_br(lucro),
        "Patrimônio Acumulado": real_br(saldo)
    })

st.table(pd.DataFrame(data_table))
