import streamlit as st
import pandas as pd
import requests

# 1. ESTÉTICA SOBERANA - VISIBILIDADE MÁXIMA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    /* Fundo Preto Fosco Total */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Tornar tabelas visíveis: Fundo cinza muito escuro e texto branco */
    div[data-testid="stTable"] {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    th { color: #FFFFFF !important; background-color: #262626 !important; }
    td { color: #FFFFFF !important; }

    /* Indicadores com cores sólidas e brilho para leitura */
    .indicator-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 800;
        font-size: 1.4rem;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .selic-bg { background-color: #00429d; } /* Azul Intenso */
    .ipca-bg { background-color: #a33200; }  /* Laranja Queimado */
    .alvo-bg { background-color: #005f36; }  /* Verde Esmeralda */
    
    /* Ajuste de abas */
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# Função de formatação monetária Brasileira R$ 1.100,00
def real_br(valor):
    a = "{:,.2f}".format(valor)
    b = a.replace(',', 'v').replace('.', ',').replace('v', '.')
    return f"R$ {b}"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "12$34":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Acesso Negado.")
    st.stop()

# 2. MOTOR DE BUSCA
@st.cache_data(ttl=3600)
def scanner_soberano():
    try:
        # Pega taxas reais
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        
        radar = [
            {"Ativo": "LCI/LCA (Melhor Taxa)", "Rent_Anual": i + 6.5, "Categoria": "Renda Fixa Isenta", "Risco": "Baixo"},
            {"Ativo": "CDB (120% CDI)", "Rent_Anual": (s * 1.20) * 0.825, "Categoria": "Renda Fixa Tributada", "Risco": "Baixo"},
            {"Ativo": "FIIs (Dividend Yield)", "Rent_Anual": 11.5, "Categoria": "Fundo Imobiliário", "Risco": "Moderado"},
            {"Ativo": "Ações (Crescimento/Div)", "Rent_Anual": 15.8, "Categoria": "Renda Variável", "Risco": "Alto"},
            {"Ativo": "CRI/CRA (Premium)", "Rent_Anual": i + 7.5, "Categoria": "Crédito Privado", "Risco": "Moderado"}
        ]
        return s, i, radar
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

# Indicadores Coloridos e Visíveis
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box alvo-bg'>ALVO: {taxa_anual_liq:.2f}% a.a.</div>", unsafe_allow_html=True)

st.write("")
st.markdown("### 🔍 Radar de Oportunidades Líquidas")

def colorir_risco(val):
    color = '#00ff88' if val == 'Baixo' else '#ffcc00' if val == 'Moderado' else '#ff4444'
    return f'color: {color}; font-weight: bold'

df_radar_view = df_radar.copy()
df_radar_view['Rent_Anual'] = df_radar_view['Rent_Anual'].apply(lambda x: f"{x:.2f}%")
st.table(df_radar_view.style.applymap(colorir_risco, subset=['Risco']))

# ABAS ORGANIZADAS
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
            "Aporte": real_br(aporte), 
            "Lucro Líquido": real_br(lucro), 
            "Patrimônio": real_br(saldo)
        })
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Simulação 10 Anos")
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo = renda_alvo / taxa_mensal_liq
    st.markdown(f"**Capital Alvo para Independência: {real_br(cap_alvo)}**")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal_liq)
        logs_10.append({
            "Ano": f"Ano {ano:02d}",
            "Patrimônio": real_br(saldo_10),
            "Renda Passiva": real_br(saldo_10 * taxa_mensal_liq),
            "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"
        })
    st.table(pd.DataFrame(logs_10))

if st.sidebar.button("🔒 Sair"):
    st.session_state.auth = False
    st.rerun()
