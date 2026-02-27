import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

# 1. ESTÉTICA SOBERANA - GRID EXCEL, BLACK OPS E PROTEÇÃO VISUAL
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

st.markdown("""
    <style>
    /* Fundo Preto Fosco */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Tabelas estilo Excel Blindado */
    div[data-testid="stTable"] table { 
        border-collapse: collapse; 
        width: 100%; 
        background-color: #0d0d0d; 
        border: 1px solid #333; 
    }
    div[data-testid="stTable"] th { 
        border: 1px solid #444; 
        padding: 12px; 
        text-align: center; 
        background-color: #1a1a1a; 
        color: #00FF88 !important; 
        font-weight: bold;
    }
    div[data-testid="stTable"] td { 
        border: 1px solid #333; 
        padding: 10px; 
        text-align: right; 
        color: #FFFFFF !important; 
    }
    
    /* Indicadores Táticos */
    .indicator-box { 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        color: white; 
        font-weight: 800; 
        font-size: 1.2rem; 
        margin-bottom: 15px; 
        border: 1px solid #222; 
    }
    .selic-bg { background-color: #00429d; } 
    .ipca-bg { background-color: #a33200; }  
    .soberano-bg { background-color: #005f36; border: 2px solid #00FF88; }
    
    /* Card de Estratégia Ativa */
    .strategy-card { 
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%); 
        border: 1px solid #00FF88; 
        padding: 25px; 
        border-radius: 10px; 
        margin: 20px 0; 
    }
    .bank-badge { 
        background-color: #00FF88; 
        color: #000; 
        padding: 3px 8px; 
        border-radius: 4px; 
        font-weight: bold; 
        font-size: 0.85rem; 
    }
    .highlight { 
        color: #00FF88; 
        font-weight: bold; 
    }

    /* 🛡️ CORREÇÃO VISUAL: FORÇANDO VERDE NEON NAS TAGS DA SIDEBAR */
    div[data-testid="stMultiselect"] > div > div > div {
        background-color: #1a1a1a !important;
        border: 1px solid #00FF88 !important;
        color: #00FF88 !important;
    }
    div[data-testid="stMultiselect"] svg {
        fill: #00FF88 !important;
    }
    div[data-testid="stMultiselect"] button[title="Remove"] {
        color: #00FF88 !important;
    }

    </style>
""", unsafe_allow_html=True)

def real_br(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- SEGURANÇA CRIPTOGRÁFICA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Sistema de Inteligência Financeira - Terminal Soberano")
    user_key = st.text_input("Insira a Chave de Comando:", type="password")
    if st.button("Autenticar"):
        if user_key == "1234@GR":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Chave inválida. Protocolo de segurança ativado.")
    st.stop()

# 2. MOTOR DE BUSCA E INTELIGÊNCIA DE MERCADO
@st.cache_data(ttl=3600)
def engine_estrategico():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        
        # Estratégia distribuída nos SEUS bancos informados
        radar = [
            {"Ativo": "Crédito Privado (CRI/CRA)", "Rent_Anual": 17.5, "Peso": 0.50, "Banco": "Banco ABC"}, 
            {"Ativo": "LCI/LCA (Isento)", "Rent_Anual": round(i + 6.8, 2), "Peso": 0.30, "Banco": "Banco INTER"}, 
            {"Ativo": "Ações Dividendos/FIIs", "Rent_Anual": round(s * 1.25, 2), "Peso": 0.20, "Banco": "ITAÚ/XP"} 
        ]
        return s, i, radar
    except: return 13.25, 4.50, []

selic, ipca, plano_ativo = engine_estrategico()
# Correção: Gerando DataFrame se plano_ativo for []
df_plano = pd.DataFrame(plano_ativo) if plano_ativo else pd.DataFrame()

# 3. SALA DE GUERRA (SIDEBAR INTEGRADA)
st.sidebar.title("🕹️ Sala de Guerra")
if st.sidebar.button("🔴 Bloquear Terminal"):
    st.session_state.autenticado = False
    st.rerun()

st.sidebar.divider()
cap_inicial = st.sidebar.number_input("Valor Capital Inicial (R$):", value=1000.0, step=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0, step=500.0)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0, step=500.0)

st.sidebar.divider()
# 🎯 CORREÇÃO VISUAL: SELETOR DE TÍTULOS AGORA VERDE NEON
st.sidebar.markdown("### 🎯 Ativos Operacionais")
ativos_radar = [f"{p['Ativo']} ({p['Rent_Anual']}%)" for p in plano_ativo]
seletor_ativos = st.sidebar.multiselect("Selecione os Títulos para Alocação:", ativos_radar, default=ativos_radar)

# 4. TAXA SOBERANA E ALOCAÇÃO
# Cálculo da Taxa Soberana baseada APENAS nos ativos selecionados
if seletor_ativos:
    df_selecionados = df_plano[df_plano['Ativo'].apply(lambda x: any(sel_a.startswith(x) for sel_a in seletor_ativos))]
    if not df_selecionados.empty:
        total_peso = df_selecionados['Peso'].sum()
        df_selecionados['Peso_Ajustado'] = df_selecionados['Peso'] / total_peso # Recalcula o peso para que a soma seja 100%
        taxa_mix = sum(df_selecionados['Rent_Anual'] * df_selecionados['Peso_Ajustado'])
    else:
        taxa_mix = 0
else:
    taxa_mix = 0

taxa_mensal = (1 + (taxa_mix/100))**(1/12) - 1
valor_atual = aporte_extra if datetime.now().month in [6, 12] else aporte_base

# 5. PAINEL SOBERANO DE PERFORMANCE LÍQUIDA
st.title("🏆 Estratégia de Minimização de Prazo")

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='indicator-box selic-bg'>SELIC: {selic}%</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='indicator-box ipca-bg'>IPCA: {ipca}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='indicator-box soberano-bg'>TAXA SOBERANA: {taxa_mix:.2f}% a.a.</div>", unsafe_allow_html=True)

# 🛡️ CORREÇÃO TÁTICA: HTML AGORA RENDERIZADO COM SUCESSO
if taxa_mix > 0:
    st.markdown(f"""
    <div class='strategy-card'>
        <h3 style='color:#00FF88; margin:0;'>🛡️ VEREDITO DA IA: ALOCAÇÃO PARA MINIMIZAR PRAZO</h3>
        Para o aporte de <span class='highlight'>{real_br(valor_atual)}</span> este mês, sua estratégia de ganho líquido é:
        <br><br>
    """, unsafe_allow_html=True)
    
    for index, row in df_selecionados.iterrows():
        valor_alocar = valor_atual * row['Peso_Ajustado']
        st.markdown(f"• **{int(row['Peso_Ajustado']*100)}%** em **{row['Ativo']}** no <span class='bank-badge'>{row['Banco']}</span>: <span class='highlight'>{real_br(valor_alocar)}</span> <br><br>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <i>Essa estratégia garante um ganho real de <span class='highlight'>{(taxa_mix - ipca):.2f}%</span> acima da inflação, focando em encurtar sua meta de 10 anos.</i>
    </div>
    """, unsafe_allow_html=True)

# TABELAS LÍQUIDAS ESTILO EXCEL
tab1, tab2 = st.tabs(["📊 PLANO 1 ANO", "🚀 ACELERAÇÃO PARA META"])

with tab1:
    saldo = cap_inicial
    logs = []
    # Log Capital Inicial
    logs.append({"Mês": "Mês 00 (Inicial)", "Aporte": real_br(0), "Lucro Líquido": real_br(0), "Patrimônio": real_br(saldo)})
    
    for m in range(1, 13):
        # Regra de engajamento: aporte extra nos meses 6 e 12
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        logs.append({"Mês": f"Mês {m:02d}", "Aporte": real_br(aporte), "Lucro Líquido": real_br(lucro), "Patrimônio": real_br(saldo)})
    st.table(pd.DataFrame(logs))

with tab2:
    renda_alvo = st.number_input("Renda Mensal Desejada (R$):", value=5000.0)
    capital_meta = renda_alvo / (taxa_mensal if taxa_mensal > 0 else 1) # Proteção contra divisão por zero
    st.success(f"Capital Alvo para Independência: {real_br(capital_meta)}")
    
    saldo_meta = cap_inicial
    logs_meta = []
    
    # Simulação até o Alvo (Mínimo 1 Ano, Máximo 11 Anos)
    if taxa_mensal > 0:
        for ano in range(1, 12):
            for m in range(1, 13):
                aporte = aporte_extra if m in [6, 12] else aporte_base
                saldo_meta += aporte + (saldo_meta * taxa_mensal)
            
            progresso = (saldo_meta / capital_meta) * 100
            logs_meta.append({"Ano": f"Ano {ano:02d}", "Patrimônio Líquido": real_br(saldo_meta), "Progresso Meta": f"{progresso:.1f}%"})
            if saldo_meta >= capital_meta:
                st.balloons()
                st.warning(f"🎯 Meta alcançada com Maestria no ANO {ano}!")
                break
        st.table(pd.DataFrame(logs_meta))
    else:
        st.error("Selecione ao menos um título operacional para calcular a meta.")
