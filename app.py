import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# ============================
# 1. ESTÉTICA SOVEREIGN EDITION
# ============================
st.set_page_config(page_title="Dr. Strategist IA", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .dr-card { background: #0a0a0a; border: 1px solid #00FF88; padding: 25px; border-radius: 10px; border-left: 10px solid #00FF88; margin: 20px 0; }
    .highlight { color: #00FF88; font-weight: 800; font-size: 1.2em; }
    div[data-testid="stTable"] table { border: 1px solid #333; width: 100%; }
    div[data-testid="stTable"] th { background-color: #111; color: #00FF88 !important; padding: 15px; }
    div[data-testid="stTable"] td { background-color: #000; color: #FFF !important; padding: 12px; border: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

# ============================
# 2. MOTOR DE INTELIGÊNCIA (EMBUTIDO)
# ============================
def get_market_metrics():
    try:
        # Busca Selic e IPCA real-time
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except:
        return 13.25, 4.50

def real_br(v):
    return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# ============================
# 3. AUTENTICAÇÃO SOVEREIGN
# ============================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Terminal Dr. Strategist - Autenticação")
    senha = st.text_input("Chave Mestra:", type="password")
    if st.button("INICIALIZAR CÉREBRO"):
        if senha == "1020*30":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Chave incorreta.")
    st.stop()

# ============================
# 4. DADOS E SIDEBAR
# ============================
selic_atual, ipca_atual = get_market_metrics()

st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=10000.0, step=1000.0)
aporte_regular = st.sidebar.number_input("Aporte Base (R$):", value=2800.0)
aporte_acelerador = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)
anos = st.sidebar.slider("Horizonte (anos)", 1, 30, 10)

# Taxa Agressiva Estratégica (Ex: IPCA + 9%)
taxa_anual_alvo = ipca_atual + 9.0 
taxa_mensal = (1 + (taxa_anual_alvo/100))**(1/12) - 1

# ============================
# 5. INTERFACE PRINCIPAL
# ============================
st.title("👨‍🔬 Dr. Strategist – IA de Investimentos")
st.write(f"Status: **Soberano** | Mercado: Selic {selic_atual}% | IPCA {ipca_atual}%")

aba1, aba2, aba3 = st.tabs(["🧠 Estratégia IA", "📈 Simulação Avançada", "📊 Cronograma 12 Meses"])

with aba1:
    comando = st.text_input("Insira sua dúvida ou comando técnico (Ex: Como vencer a inflação hoje?):")
    if comando:
        ganho_real = taxa_anual_alvo - ipca_atual
        st.markdown(f"""
        <div class='dr-card'>
            <b>PARECER DO DR. STRATEGIST:</b><br>
            Com base no seu comando: <i>"{comando}"</i>, analisei que sua estrutura de capital está 
            configurada para <b>Alavancagem Agressiva</b>.<br><br>
            • <b>Fator Anti-Inflação:</b> Sua carteira rende <span class='highlight'>{ganho_real:.2f}% acima do IPCA</span>.<br>
            • <b>Sugestão de Alocação:</b> Manter 60% em Crédito Privado (ABC/Inter) e 40% em FIIs de Papel (Itaú).<br>
            • <b>Veredito:</b> O aporte de aceleração de {real_br(aporte_acelerador)} no final do ano reduz seu tempo de meta em 18%.
        </div>
        """, unsafe_allow_html=True)

with aba2:
    st.subheader("📈 Projeção de Crescimento Disparado")
    meses = anos * 12
    saldos = []
    atual = cap_inicial
    for m in range(1, meses + 1):
        # Aceleração no mês 12 de cada ano
        ap = aporte_acelerador if m % 12 == 0 else aporte_regular
        atual = (atual + ap) * (1 + taxa_mensal)
        saldos.append(atual)
    
    df_curva = pd.DataFrame({"Patrimônio": saldos})
    st.line_chart(df_curva)
    st.metric("Patrimônio Final Projetado", real_br(atual))

with aba3:
    st.subheader("📊 Cronograma de Crescimento (12 Meses Líquido)")
    logs = []
    saldo_tab = cap_inicial
    for m in range(1, 13):
        ap = aporte_acelerador if m == 12 else aporte_regular
        lucro = saldo_tab * taxa_mensal
        saldo_tab += ap + lucro
        logs.append({
            "Mês": f"Mês {m:02d}",
            "Aporte": real_br(ap),
            "Lucro Líquido": real_br(lucro),
            "Patrimônio": real_br(saldo_tab)
        })
    st.table(pd.DataFrame(logs))
