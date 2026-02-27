import streamlit as st
import pandas as pd
import requests

# 1. ESTÉTICA E CONFIGURAÇÃO
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stTable"] { background-color: #1A1A1A; border: 1px solid #333333; border-radius: 8px; }
    th { color: #FFFFFF !important; background-color: #262626 !important; }
    td { color: #FFFFFF !important; }
    .indicator-box { padding: 25px; border-radius: 15px; text-align: center; color: white; font-weight: 800; font-size: 1.4rem; margin-bottom: 15px; }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .alvo-bg { background-color: #005f36; }  
    .acelerador-card { background-color: #1E1E1E; padding: 20px; border: 2px solid #FFD700; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == ".1234.": st.session_state.auth = True; st.rerun()
    st.stop()

# 2. MOTOR DE BUSCA (REAL-TIME) + INTELIGÊNCIA DE ACELERAÇÃO
@st.cache_data(ttl=3600)
def buscar_dados_mercado():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        
        radar = [
            {"Ativo": "LCI/LCA (Isento)", "Rent_Anual": i + 6.8, "Risco": "Baixo", "Tipo": "Proteção"},
            {"Ativo": "CDB (125% CDI)", "Rent_Anual": (s * 1.25) * 0.825, "Risco": "Baixo", "Tipo": "Renda Fixa"},
            {"Ativo": "FIIs (Destaque Dividendos)", "Rent_Anual": 12.5, "Risco": "Moderado", "Tipo": "Renda Variável"},
            {"Ativo": "Ações (Máxima Aceleração)", "Rent_Anual": 16.2, "Risco": "Alto", "Tipo": "Crescimento"},
            {"Ativo": "CRI/CRA Premium", "Rent_Anual": i + 7.8, "Risco": "Moderado", "Tipo": "Crédito Privado"}
        ]
        return s, i, radar
    except: return 13.25, 4.50, []

selic_at, ipca_at, radar_dados = buscar_dados_mercado()
df_radar = pd.DataFrame(radar_dados)

# Identifica o título com maior poder de aceleração
melhor_ativo_nome = df_radar.loc[df_radar['Rent_Anual'].idxmax()]['Ativo']
melhor_taxa_valor = df_radar['Rent_Anual'].max()

# 3. SIDEBAR (INTERAÇÃO DO USUÁRIO)
st.sidebar.title("🕹️ Painel de Controle")
st.sidebar.markdown("### Ajuste seus Parâmetros")
aporte_base = st.sidebar.number_input("Aporte Base (R$):", value=2500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)
mes_acel = st.sidebar.checkbox("Este mês terá Aporte de Aceleração?")
valor_aporte_atual = aporte_extra if mes_acel else aporte_base

st.sidebar.divider()
st.sidebar.markdown("### Seleção de Título")
ativo_escolhido = st.sidebar.selectbox("Qual título você deseja operar hoje?", df_radar['Ativo'].tolist())
taxa_anual_escolhida = df_radar[df_radar['Ativo'] == ativo_escolhido]['Rent_Anual'].values[0]
taxa_mensal = (1 + (taxa_anual_escolhida/100))**(1/12) - 1

# 4. PAINEL PRINCIPAL
st.title("🏆 Wealth Catalyst IA - Terminal Soberano")

# Indicadores Macro
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic_at}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca_at}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box alvo-bg'>OPERAÇÃO: {taxa_anual_escolhida:.2f}% a.a.</div>", unsafe_allow_html=True)

# CARD DE ACELERAÇÃO (SUGESTÃO IA)
st.markdown(f"""
    <div class='acelerador-card'>
        <span style='color: #FFD700; font-size: 1.2rem;'>⚡ <strong>MOTOR DE ACELERAÇÃO ATIVADO</strong></span><br>
        O título com maior poder de ganho real hoje é: <strong>{melhor_ativo_nome}</strong> ({melhor_taxa_valor:.2f}% a.a.).<br>
        Sugestão de Alocação: <strong>{real_br(valor_aporte_atual * 0.7)}</strong> em {ativo_escolhido} e <strong>{real_br(valor_aporte_atual * 0.3)}</strong> em {melhor_ativo_nome} para acelerar a meta.
    </div>
""", unsafe_allow_html=True)

# Radar Completo para o usuário analisar
st.markdown("### 🔍 Radar de Oportunidades Líquidas")
def colorir_risco(val):
    color = '#00ff88' if val == 'Baixo' else '#ffcc00' if val == 'Moderado' else '#ff4444'
    return f'color: {color}; font-weight: bold'

df_radar_view = df_radar.copy()
df_radar_view['Rent_Anual'] = df_radar_view['Rent_Anual'].apply(lambda x: f"{x:.2f}%")
st.table(df_radar_view.style.applymap(colorir_risco, subset=['Risco']))

# ABAS DE PROJEÇÃO
tab1, tab2 = st.tabs(["📊 CRONOGRAMA 12 MESES", "🚀 PROJEÇÃO 10 ANOS"])

with tab1:
    st.subheader(f"Plano Tático Baseado em: {ativo_escolhido}")
    saldo, logs = 0, []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    st.subheader("Simulação de Independência Financeira")
    renda_alvo = st.number_input("Renda Desejada (R$):", value=5000.0)
    cap_alvo = renda_alvo / taxa_mensal
    st.success(f"Capital Alvo: {real_br(cap_alvo)}")
    
    saldo_10, logs_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if m in [6, 12] else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal)
        logs_10.append({"Ano": f"Ano {ano:02d}", "Patrimônio": real_br(saldo_10), "Renda Passiva": real_br(saldo_10 * taxa_mensal), "Meta (%)": f"{(saldo_10/cap_alvo)*100:.1f}%"})
    st.table(pd.DataFrame(logs_10))
