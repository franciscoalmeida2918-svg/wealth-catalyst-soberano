import streamlit as st
import pandas as pd
import requests
from datetime import datetime

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
    .allocation-box { background-color: #1a1a1a; padding: 10px; border-radius: 5px; border: 1px dashed #00FF88; margin-top: 10px; }
    .bank-tag { background-color: #333; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; color: #00FF88; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SISTEMA DE SEGURANÇA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Acesso ao Terminal Soberano")
    senha = st.text_input("Insira a Chave de Comando:", type="password")
    if st.button("Desbloquear"):
        if senha == "1234": # Altere aqui sua senha
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Chave incorreta. Acesso negado.")
    st.stop()

# 2. MOTOR DE BUSCA E INTELIGÊNCIA DE MERCADO (XP/BTG/INTER)
@st.cache_data(ttl=3600)
def scanner_estrategico():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        
        # Mapeamento de Instituições por melhor taxa histórica/atual
        radar = [
            {"Ativo": "Ações/CRI (Aceleração)", "Rent_Anual": 17.8, "Peso": 0.50, "Banco": "XP Investimentos"}, 
            {"Ativo": "IFIL (Logística)", "Rent_Anual": round(i + 6.5, 2), "Peso": 0.30, "Banco": "BTG Pactual"}, 
            {"Ativo": "LCI/LCA (Blindagem)", "Rent_Anual": round(i + 6.8, 2), "Peso": 0.20, "Banco": "Banco Inter"} 
        ]
        return s, i, radar
    except: return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = scanner_estrategico()
df_radar = pd.DataFrame(radar_dados)

# 3. SIDEBAR - OPERAÇÕES
st.sidebar.title("🕹️ Operações de Guerra")
if st.sidebar.button("Encerrar Sessão"):
    st.session_state.autenticado = False
    st.rerun()

cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=0.0)
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

st.sidebar.divider()
st.sidebar.markdown("### 🏦 Custódia Estratégica")
for r in radar_dados:
    st.sidebar.write(f"**{r['Ativo']}**: {r['Banco']}")

# 4. CÁLCULO DA TAXA MÉDIA PONDERADA
taxa_ponderada_anual = sum(item['Rent_Anual'] * item['Peso'] for item in radar_dados)
taxa_mensal_soberana = (1 + (taxa_ponderada_anual/100))**(1/12) - 1
valor_atual = aporte_extra if datetime.now().month in [6, 12] else aporte_base

# 5. PAINEL DE CONTROLE TÁTICO
st.title("🏆 Terminal de Minimização de Prazo")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box ifil-bg' style='background-color:#6a1b9a'>MIX SOBERANO: {taxa_ponderada_anual:.2f}%</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='indicator-box alvo-bg'>GANHO REAL: {(taxa_ponderada_anual - ipca_at):.2f}%</div>", unsafe_allow_html=True)

# CARD DE ESTRATÉGIA ATIVA COM INDICAÇÃO DE BANCO
st.markdown(f"""
<div class='strategy-card'>
    <h3 style='color:#00FF88; margin-top:0;'>🛡️ ESTRATÉGIA DE DIVISÃO E LOCALIZAÇÃO</h3>
    Para minimizar o prazo, divida seu aporte de <strong>{real_br(valor_atual)}</strong> conforme abaixo:
    <div class='allocation-box'>
        • 50% em <strong>{radar_dados[0]['Ativo']}</strong> na <span class='bank-tag'>{radar_dados[0]['Banco']}</span>: {real_br(valor_atual * 0.5)} <br>
        • 30% em <strong>{radar_dados[1]['Ativo']}</strong> no <span class='bank-tag'>{radar_dados[1]['Banco']}</span>: {real_br(valor_atual * 0.3)} <br>
        • 20% em <strong>{radar_dados[2]['Ativo']}</strong> no <span class='bank-tag'>{radar_dados[2]['Banco']}</span>: {real_br(valor_atual * 0.2)}
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES (LÍQUIDO)", "🚀 ACELERAÇÃO PARA META"])

with tab1:
    st.subheader("Simulação de Fluxo de Caixa Otimizado")
    saldo = cap_inicial
    logs = []
    for m in range(1, 13):
        aporte = 3000 if m in [6, 12] else 2500
        lucro = saldo * taxa_mensal_soberana
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte Total": real_br(aporte), "Lucro Líquido Mix": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Minimização do Período de 10 Anos")
    renda_alvo = st.number_input("Renda Desejada Mensal (R$):", value=5000.0)
    capital_meta = renda_alvo / taxa_mensal_soberana
    st.success(f"Capital Alvo para Independência: {real_br(capital_meta)}")
    
    saldo_10 = cap_inicial
    logs_10 = []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = 3000 if m in [6, 12] else 2500
            saldo_10 += aporte + (saldo_10 * taxa_mensal_soberana)
        
        progresso = (saldo_10 / capital_meta) * 100
        logs_10.append({
            "Ano": f"Ano {ano:02d}", 
            "Patrimônio Líquido": real_br(saldo_10), 
            "Renda Passiva": real_br(saldo_10 * taxa_mensal_soberana),
            "Meta (%)": f"{progresso:.1f}%"
        })
        if saldo_10 >= capital_meta:
             st.balloons()
             st.warning(f"🎯 Meta alcançada com Maestria no ANO {ano}!")
             break
             
    st.table(pd.DataFrame(logs_10))
