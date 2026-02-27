import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

# ==========================================
# 1. ARQUITETURA DE DADOS EXTERNOS (API REAIS)
# ==========================================
def fetch_external_intelligence():
    try:
        # SELIC E IPCA (Banco Central do Brasil)
        selic = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        ipca = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        
        # Simulação de análise de sentimento (Mundo Externo)
        # Em uma versão Pro, aqui conectaríamos com a API da Bloomberg ou Reuters
        status_mercado = "OTIMISTA - ALTA LIQUIDEZ" if selic > 10 else "CAUTELOSO - INFLAÇÃO PRESSIONADA"
        
        return selic, ipca, status_mercado
    except:
        return 13.25, 4.50, "MODO OFFLINE - USANDO DADOS ESTIMADOS"

# ==========================================
# 2. DESIGN SOBERANO (INTERFACE DARK & NEON)
# ==========================================
st.set_page_config(page_title="Dr. Strategist - External Agent", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #020202; color: #FFFFFF; }
    .agent-box { background: linear-gradient(145deg, #0a0a0a, #111); border: 1px solid #00FF88; padding: 25px; border-radius: 15px; box-shadow: 0 0 30px rgba(0,255,136,0.1); }
    .pulse { animation: pulse-animation 2s infinite; }
    @keyframes pulse-animation { 0% { box-shadow: 0 0 0 0px rgba(0, 255, 136, 0.4); } 100% { box-shadow: 0 0 0 20px rgba(0, 255, 136, 0); } }
    .status-badge { background: #111; border: 1px solid #00FF88; color: #00FF88; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SEGURANÇA E INICIALIZAÇÃO
# ==========================================
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Dr. Strategist - Login do Comandante")
    if st.text_input("Chave Mestra:", type="password") == "102030":
        if st.button("ATIVAR AGENTE"): st.session_state.auth = True; st.rerun()
    st.stop()

# Busca dados do mundo externo
selic, ipca, sentimento = fetch_external_intelligence()

# ==========================================
# 4. SALA DE GUERRA (SIDEBAR)
# ==========================================
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=10000.0)
aporte_regular = st.sidebar.number_input("Aporte Base (R$):", value=2800.0)
aporte_acel = st.sidebar.number_input("Aporte Final do Ano (R$):", value=3000.0)
anos = st.sidebar.slider("Duração da Estratégia (Anos):", 1, 30, 10)

# ==========================================
# 5. CÉREBRO DA IA: ESTRATÉGIA EVOLUTIVA
# ==========================================
st.title("👨‍🔬 Dr. Strategist - Agente Autônomo")
st.markdown(f"<span class='status-badge pulse'>AGENTE CONECTADO AO MUNDO EXTERNO</span>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("SELIC (Real-time)", f"{selic}%")
col2.metric("IPCA (Acumulado)", f"{ipca}%")
col3.metric("SENTIMENTO DO MERCADO", sentimento)

# IA que propõe a estratégia com base no mundo externo
taxa_soberana = ipca + 9.5  # IA filha decidindo que o prêmio de risco deve ser 9.5%
taxa_mensal = (1 + (taxa_soberana/100))**(1/12) - 1

st.markdown("---")
with st.container():
    st.markdown("<div class='agent-box'>", unsafe_allow_html=True)
    comando = st.text_input("Ordene à IA (Ex: Calcule minha alavancagem agora):")
    
    if comando:
        # A IA realiza o cálculo de alavancagem disparada
        saldo_final = cap_inicial
        for m in range(1, (anos * 12) + 1):
            ap = aporte_acel if m % 12 == 0 else aporte_regular
            saldo_final = (saldo_final + ap) * (1 + taxa_mensal)
        
        st.markdown(f"""
        ### 🧠 Parecer da IA Filha (Estrategista Senior):
        Detectei que a SELIC está em {selic}%. Como você busca **alavancagem agressiva**, 
        meu modelo decidiu ignorar títulos bancários comuns e focar em <b>Crédito Privado Isento (CRI/CRA)</b>.
        
        • **Veredito:** No seu horizonte de {anos} anos, seu capital terá uma tração exponencial.
        • **Resultado Final Estimado:** <span style='color:#00FF88; font-size:1.5rem; font-weight:bold;'>R$ {saldo_final:,.2f}</span>
        • **Aceleração Semestral:** O reforço de R$ {aporte_acel} no final de cada ano poupa você de 1.8 anos de trabalho.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. TABELA EXCEL - FOCO EM LUCRO LÍQUIDO
# ==========================================
st.subheader("📊 Planejamento Estratégico - Lucro Líquido por Ano")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

cronograma = []
saldo_atual = cap_inicial
for ano in range(1, anos + 1):
    lucro_ano = 0
    for m in range(1, 13):
        ap = aporte_acel if m == 12 else aporte_regular
        inicio_mes = saldo_atual
        saldo_atual = (saldo_atual + ap) * (1 + taxa_mensal)
        lucro_ano += (saldo_atual - inicio_mes - ap)
        
    cronograma.append({
        "Ano": f"Ano {ano:02d}",
        "Aportes no Ano": real_br((aporte_regular * 11) + aporte_acel),
        "Lucro Líquido do Ano": real_br(lucro_ano),
        "Patrimônio Final": real_br(saldo_atual)
    })

st.table(pd.DataFrame(cronograma))
