import streamlit as st
import pandas as pd
import requests
import locale

# 1. ESTÉTICA SOBERANA - PRETO FOSCO (MATTE BLACK)
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    /* Fundo Preto Fosco em toda a aplicação */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    /* Estilização das tabelas para combinar com o fundo */
    .stTable, div[data-testid="stTable"] {
        background-color: #1a1a1a;
        border-radius: 10px;
    }
    /* Indicadores com cores sólidas e contraste alto */
    .indicator-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.3rem;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .selic-bg { background-color: #1e3a8a; } /* Azul Noite */
    .ipca-bg { background-color: #a63e14; }  /* Terracota Escuro */
    .alvo-bg { background-color: #065f46; }  /* Verde Floresta */
    
    /* Ajuste de cor do texto em inputs */
    input, select {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Função para formatar moeda no padrão R$ 1.100,00
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "3-1#234*":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Acesso Negado.")
    st.stop()

# 2. MOTOR DE BUSCA (REAL-TIME)
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

# 3. SIDEBAR
st.sidebar.title("🕹️ Central de Comando")
df_radar = pd.DataFrame(radar_dados)
ativo_sel = st.sidebar.selectbox("🎯 Ativo Estratégico:", df_radar['Ativo'])
taxa_anual_liq = df_radar[df_radar['Ativo'] == ativo_sel]['Rent_Anual'].values[0]
taxa_mensal_liq = (1 + (taxa_anual_liq/100))**(1/12) - 1

st.sidebar.divider()
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst IA")

# Indicadores com Cores Sólidas e Fundo Preto Fosco ao redor
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box alvo-bg'>ALVO: {taxa_anual_liq:.2f}% a.a.</div>", unsafe_allow_html=True)

st.write("")
st.markdown("### 🔍 Radar de Oportunidades Líquidas")

def colorir_risco(val):
    color = '#10b981' if val == 'Baixo' else '#f59e0b' if val == 'Moderado' else '#ef4444'
    return f'color: {color}; font-weight: bold'

df_radar_view = df_radar.copy()
df_radar_view['Rent_Anual'] = df_radar_view['Rent_Anual'].apply(lambda x: f"{x:.2f}%")
st.table(df_radar_view.style.applymap(colorir_risco, subset=['Risco']))

# ABAS COM FORMATAÇÃO R$ 1.100,00
tab1, tab2 = st.tabs(["📊 CRONOGRAMA LÍQUIDO", "🚀 PROJEÇÃO DE LIBERDADE"])

with tab1:
    st.subheader(f"Plano 12 Meses: {ativo_sel}")
    saldo, logs = 0, []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal_liq
        saldo += aporte + lucro
        logs.append({
            "Mês": f"Mês {m:02d}", 
            "Aporte": formatar_brl(aporte), 
            "Lucro Líquido": formatar_brl(lucro), 
            "Patrimônio": formatar_brl(saldo)
        })
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Simulação 10 Anos (Aceleração)")
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo = renda_alvo / taxa_mensal_liq
    st.info(f"Capital Alvo: {formatar_brl(cap_alvo)}")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal_liq)
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio": formatar_brl(saldo_10),
            "Renda Passiva": formatar_brl(saldo_10 * taxa_mensal_liq),
            "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"
        })
    st.table(pd.DataFrame(logs_10))

if st.sidebar.button("🔒 Sair"):
    st.session_state.auth = False
    st.rerun()
