import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from strategist_engine import (
    get_market_metrics,
    simular_patrimonio,
    gerar_relatorio_estrategico,
    tabela_12_meses
)

# ============================
# 1. ESTÉTICA SOVEREIGN EDITION
# ============================
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

# ============================
# 2. AUTENTICAÇÃO SOVEREIGN
# ============================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Terminal Dr. Strategist - Autenticação")
    if st.text_input("Chave Mestra:", type="password") == "102030":
        if st.button("INICIALIZAR CÉREBRO"):
            st.session_state.auth = True
            st.rerun()
    st.stop()

# ============================
# 3. DADOS DE MERCADO
# ============================
selic_atual, ipca_atual = get_market_metrics()

# ============================
# 4. SIDEBAR – SALA DE GUERRA
# ============================
st.sidebar.title("🕹️ Sala de Guerra")

cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=1000.0, step=1000.0)
aporte_regular = st.sidebar.number_input("Aporte Base (R$):", value=2500.0)
aporte_acelerador = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)
anos = st.sidebar.slider("Horizonte (anos)", 1, 20, 10)

# ============================
# 5. INTERFACE PRINCIPAL
# ============================
st.title("👨‍🔬 Dr. Strategist – IA de Investimentos")
st.write(f"Conectado ao Dr. IA Central | Status: **Soberano** | Mercado: Selic {selic_atual}% | IPCA {ipca_atual}%")

aba1, aba2, aba3 = st.tabs(["🧠 Estratégia", "📈 Simulação", "📊 Cronograma 12 Meses"])

# ============================
# 6. ABA 1 – ESTRATÉGIA
# ============================
with aba1:
    comando = st.text_input("Insira sua dúvida ou comando técnico:")

    if comando:
        relatorio = gerar_relatorio_estrategico(
            comando, cap_inicial, aporte_regular, aporte_acelerador,
            selic_atual, ipca_atual, anos
        )
        st.markdown(relatorio, unsafe_allow_html=True)

# ============================
# 7. ABA 2 – SIMULAÇÃO
# ============================
with aba2:
    patrimonio_final, curva = simular_patrimonio(
        cap_inicial, aporte_regular, aporte_acelerador, anos, ipca_atual
    )

    st.subheader("📈 Evolução Patrimonial")
    st.line_chart(curva)

    st.metric("Patrimônio Final", f"R$ {patrimonio_final:,.2f}")

# ============================
# 8. ABA 3 – TABELA 12 MESES
# ============================
with aba3:
    st.subheader("📊 Cronograma de Crescimento (12 Meses)")
    tabela = tabela_12_meses(cap_inicial, aporte_regular, aporte_acelerador, ipca_atual)
    st.table(tabela)
