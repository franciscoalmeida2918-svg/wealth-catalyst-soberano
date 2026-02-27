import streamlit as st
import pandas as pd
import requests

# 1. ESTÉTICA E SEGURANÇA SOBERANA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

# Estilização para indicadores com cores de fundo sólidas e texto claro
st.markdown("""
    <style>
    .indicator-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .selic-bg { background-color: #2e5cb8; } /* Azul Sólido */
    .ipca-bg { background-color: #d9480f; }  /* Laranja Sólido */
    .alvo-bg { background-color: #087f5b; }  /* Verde Sólido */
    
    .stTable { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "$12*34":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Acesso Negado.")
    st.stop()

# 2. MOTOR DE BUSCA EM TEMPO REAL
@st.cache_data(ttl=3600)
def scanner_soberano():
    try:
        selic = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        ipca = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        
        radar = [
            {"Ativo": "LCI/LCA (Melhor Taxa)", "Rent_Anual": ipca + 6.5, "Categoria": "Renda Fixa Isenta", "Risco": "Baixo"},
            {"Ativo": "CDB (120% CDI)", "Rent_Anual": (selic * 1.20) * 0.825, "Categoria": "Renda Fixa Tributada", "Risco": "Baixo"},
            {"Ativo": "FIIs (Dividend Yield)", "Rent_Anual": 11.5, "Categoria": "Fundo Imobiliário", "Risco": "Moderado"},
            {"Ativo": "Ações (Crescimento/Div)", "Rent_Anual": 15.8, "Categoria": "Renda Variável", "Risco": "Alto"},
            {"Ativo": "CRI/CRA (Premium)", "Rent_Anual": ipca + 7.5, "Categoria": "Crédito Privado", "Risco": "Moderado"}
        ]
        return selic, ipca, radar
    except: return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = scanner_soberano()

# 3. SIDEBAR E SELEÇÃO
st.sidebar.title("🕹️ Central de Comando")
df_radar = pd.DataFrame(radar_dados)
ativo_sel = st.sidebar.selectbox("🎯 Escolher Alvo Estratégico:", df_radar['Ativo'])
taxa_anual_liq = df_radar[df_radar['Ativo'] == ativo_sel]['Rent_Anual'].values[0]
taxa_mensal_liq = (1 + (taxa_anual_liq/100))**(1/12) - 1

st.sidebar.divider()
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000)

# 4. PAINEL PRINCIPAL COM INDICADORES COLORIDOS
st.title("🏆 Wealth Catalyst - Estratégia Soberana")

# Indicadores com Cores de Fundo Fortes para Leitura Clara
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box alvo-bg'>ALVO: {taxa_anual_liq:.2f}% a.a.</div>", unsafe_allow_html=True)

st.write("")
st.markdown("### 🔍 Radar de Oportunidades (Top 5 Mercado)")

def colorir_risco(val):
    color = '#10b981' if val == 'Baixo' else '#f59e0b' if val == 'Moderado' else '#ef4444'
    return f'color: {color}; font-weight: bold'

df_radar_view = df_radar.copy()
df_radar_view['Rent_Anual'] = df_radar_view['Rent_Anual'].apply(lambda x: f"{x:.2f}%")
st.table(df_radar_view.style.applymap(colorir_risco, subset=['Risco']))

# ABAS
tab1, tab2 = st.tabs(["📊 CRONOGRAMA LÍQUIDO", "🚀 PROJEÇÃO DE LIBERDADE"])

with tab1:
    st.subheader(f"Plano Tático: {ativo_sel}")
    saldo, logs = 0, []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal_liq
        saldo += aporte + lucro
        logs.append({
            "Mês": f"Mês {m:02d}", 
            "Aporte": f"R$ {aporte:,.2f}", 
            "Lucro Líquido": f"R$ {lucro:,.2f}", 
            "Patrimônio": f"R$ {saldo:,.2f}"
        })
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Aceleração de 10 Anos")
    renda_alvo = st.number_input("Sua Renda Alvo Mensal (R$):", value=5000)
    cap_alvo = renda_alvo / taxa_mensal_liq
    st.info(f"Capital Alvo: R$ {cap_alvo:,.2f}")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal_liq)
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio Acumulado": f"R$ {saldo_10:,.2f}",
            "Renda Passiva": f"R$ {saldo_10 * taxa_mensal_liq:,.2f}",
            "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"
        })
    st.table(pd.DataFrame(logs_10))

if st.sidebar.button("🔒 Sair"):
    st.session_state.auth = False
    st.rerun()
