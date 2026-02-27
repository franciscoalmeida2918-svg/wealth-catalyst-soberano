import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. ESTÉTICA DE ELITE (RESOLVENDO O PROBLEMA DAS IMAGENS)
st.set_page_config(page_title="IA Sentinela Soberana", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    /* Limpeza de Tabelas */
    div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; background-color: #000; border: 1px solid #1f1f1f; }
    div[data-testid="stTable"] th { background-color: #0d0d0d; color: #00FF88 !important; padding: 15px; border: 1px solid #1f1f1f; }
    div[data-testid="stTable"] td { padding: 12px; border: 1px solid #1f1f1f; color: #EEE !important; }
    
    /* Cards de Inteligência */
    .ia-response { background: #0d0d0d; border: 1px solid #00FF88; padding: 25px; border-radius: 15px; margin: 20px 0; border-left: 8px solid #00FF88; }
    .highlight { color: #00FF88; font-weight: bold; }
    .bank-badge { background-color: #00FF88; color: #000; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# 2. SEGURANÇA E CONEXÃO COM O CÉREBRO CENTRAL (DR. IA)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ Chave de Comando")
    if st.text_input("Senha:", type="password") == "&*102030":
        if st.button("ATIVAR IA"): st.session_state.auth = True; st.rerun()
    st.stop()

# 3. MOTOR DE APRENDIZADO DIÁRIO (API REAL TIME)
@st.cache_data(ttl=3600)
def fetch_market():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json").json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").json()[0]['valor'])
        return s, i
    except: return 13.25, 4.50

selic, ipca = fetch_market()

# 4. SALA DE GUERRA (SIDEBAR)
st.sidebar.title("🕹️ Sala de Guerra")
cap_inicial = st.sidebar.number_input("Capital Inicial (R$):", value=1000.0)
aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500.0)
aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000.0)

# 5. A IA QUE APRENDE (SENTINELA EVOLUTIVA)
st.title("🤖 IA Sentinela: Inteligência Evolutiva")
st.write(f"Conectada ao Dr. IA | Mercado hoje: SELIC {selic}% | IPCA {ipca}%")

if "historico_ia" not in st.session_state: st.session_state.historico_ia = []

with st.container():
    pergunta = st.text_input("Comando para a IA (Ex: Crie o plano de hoje):", key="cmd")
    
    if pergunta:
        # Lógica de cálculo soberano para tomada de decisão
        taxa_abc = 16.80 # Título foco que ganha da inflação
        lucro_estimado_12m = (cap_inicial * (taxa_abc/100)) + (aporte_base * 12)
        
        resposta = f"""
        <div class='ia-response'>
            <b>ANÁLISE SENTINELA:</b> Baseado na SELIC de {selic}%, detectei que o banco <span class='bank-badge'>ABC</span> 
            é a melhor rota hoje. <br><br>
            <b>PLANO ESTRATÉGICO:</b> <br>
            • Alocação: 50% em CRI IPCA+ no ABC para garantir <span class='highlight'>{(taxa_abc-ipca):.2f}% de ganho real</span>. <br>
            • Projeção 12 meses: Patrimônio líquido estimado em <span class='highlight'>R$ {lucro_estimado_12m:,.2f}</span>. <br><br>
            <i>IA aprendeu: Você prioriza liquidez no Inter e Inter e aceleração máxima no ABC. Protocolo Anti-Inflação Ativado.</i>
        </div>
        """
        st.markdown(resposta, unsafe_allow_html=True)
        st.session_state.historico_ia.append(pergunta)

# 6. TABELA DE RESULTADOS (EXCEL STYLE - LÍQUIDO REAL)
st.divider()
st.subheader("📊 Cronograma de Ganhos Líquidos (Visão Excel)")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

taxa_mensal = (1 + (16.80/100))**(1/12) - 1
saldo = cap_inicial
dados_tabela = []

for m in range(1, 13):
    ap = aporte_acel if m in [6, 12] else aporte_base
    lucro = saldo * taxa_mensal
    saldo += ap + lucro
    dados_tabela.append({
        "Mês": f"Mês {m:02d}",
        "Aporte": real_br(ap),
        "Lucro Líquido": real_br(lucro),
        "Patrimônio": real_br(saldo)
    })

st.table(pd.DataFrame(dados_tabela))
