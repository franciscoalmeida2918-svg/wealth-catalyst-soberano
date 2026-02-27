import streamlit as st
import pandas as pd
import requests

# 1. ESTÉTICA E SEGURANÇA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

# Estilização CSS para cores e tabelas
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTable { border: 1px solid #30363d; border-radius: 10px; }
    .metric-card {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
    }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    st.subheader("Terminal de Alta Performance")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "#123*4":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Acesso Negado.")
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
    except:
        return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = scanner_soberano()

# 3. SIDEBAR E SELEÇÃO
st.sidebar.title("🕹️ Central de Comando")
df_radar = pd.DataFrame(radar_dados)

# Seletor com destaque visual no nome
ativo_sel = st.sidebar.selectbox("🎯 Escolher Alvo Estratégico:", df_radar['Ativo'])
taxa_anual_liq = df_radar[df_radar['Ativo'] == ativo_sel]['Rent_Anual'].values[0]
taxa_mensal_liq = (1 + (taxa_anual_liq/100))**(1/12) - 1

st.sidebar.divider()
aporte_base = st.sidebar.number_input("Aporte Padrão (R$):", value=2500)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000)

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst - Estratégia Soberana")

# Cards de Indicadores
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='metric-card'>SELIC: <b>{selic_at}%</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'>IPCA: <b>{ipca_at}%</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'>TAXA ALVO: <b>{taxa_anual_liq:.2f}% a.a.</b></div>", unsafe_allow_html=True)

st.write("")
st.markdown("### 🔍 Radar de Oportunidades em Tempo Real")

# Formatação da Tabela Colorida
def colorir_risco(val):
    color = '#10b981' if val == 'Baixo' else '#f59e0b' if val == 'Moderado' else '#ef4444'
    return f'color: {color}; font-weight: bold'

df_radar_view = df_radar.copy()
df_radar_view['Rent_Anual'] = df_radar_view['Rent_Anual'].apply(lambda x: f"{x:.2f}%")

st.table(df_radar_view.style.applymap(colorir_risco, subset=['Risco']))

# ABAS DE RESULTADOS
tab1, tab2 = st.tabs(["📊 CRONOGRAMA LÍQUIDO (1 ANO)", "🚀 PROJEÇÃO DE LIBERDADE (10 ANOS)"])

with tab1:
    st.subheader(f"Fluxo de Caixa: {ativo_sel}")
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
    st.subheader("Aceleração de Ganho de Capital")
    renda_alvo = st.number_input("Sua Renda Alvo Mensal (R$):", value=5000)
    capital_necessario = renda_alvo / taxa_mensal_liq
    
    st.info(f"Capital necessário para viver de renda: **R$ {capital_necessario:,.2f}**")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal_liq)
        
        renda_gerada = saldo_10 * taxa_mensal_liq
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio Acumulado": f"R$ {saldo_10:,.2f}",
            "Renda Mensal Passiva": f"R$ {renda_gerada:,.2f}",
            "Meta (%)": f"{(saldo_10/capital_necessario)*100:.1f}%"
        })
    
    st.table(pd.DataFrame(logs_10))

if st.sidebar.button("🔒 Sair"):
    st.session_state.auth = False
    st.rerun()
