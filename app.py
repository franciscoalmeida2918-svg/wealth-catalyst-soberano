import streamlit as st
import pandas as pd
import requests

# 1. SEGURANÇA E TELA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Wealth Catalyst IA")
    st.subheader("Estratégia Soberana - Terminal Privado")
    senha = st.text_input("Chave de Segurança:", type="password")
    if st.button("Acessar Terminal"):
        if senha == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Chave Inválida.")
    st.stop()

# 2. MOTOR DE DADOS
@st.cache_data(ttl=3600)
def obter_dados():
    try:
        s = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        i = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
        return s, i
    except:
        return 13.25, 4.50

selic, ipca = obter_dados()

# 3. SIDEBAR - INTELIGÊNCIA
st.sidebar.title("🕹️ Central de Comando")
cor = "#10b981" if ipca <= 4.5 else "#FF4B4B"
sugestao = "CDB (110% CDI)" if ipca <= 4.5 else "LCI/LCA (IPCA + 6%)"

st.sidebar.markdown(f"""
    <div style="border: 2px solid {cor}; padding: 15px; border-radius: 10px;">
        <strong style="color: {cor};">💡 INSIGHT DA IA:</strong><br>
        IPCA: {ipca}% | SELIC: {selic}%<br>
        <b>Estratégia Recomendada: {sugestao}</b>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()
aporte_base = st.sidebar.number_input("Aporte Mensal Base (R$):", value=2500)
aporte_extra = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000)

titulos = {
    "LCI/LCA (IPCA + 6%)": ipca + 6.0,
    "CDB (110% CDI)": (selic * 1.1) * 0.825,
    "Ações/FIIs (Estratégico)": 14.5
}
ativo_sel = st.sidebar.selectbox("Título Estratégico:", list(titulos.keys()))
taxa_mensal = (1 + (titulos[ativo_sel]/100))**(1/12) - 1

# 4. DASHBOARD
st.title("🏆 Wealth Catalyst IA")
tab1, tab2 = st.tabs(["📊 PLANO TÁTICO (1 ANO)", "🚀 RUMO À INDEPENDÊNCIA"])

with tab1:
    st.subheader(f"Evolução Líquida: {ativo_sel}")
    saldo, dados_ano = 0, []
    for m in range(1, 13):
        aporte = aporte_extra if m in [6, 12] else aporte_base
        lucro = saldo * taxa_mensal
        saldo += aporte + lucro
        dados_ano.append({"Mês": f"Mês {m}", "Aporte": aporte, "Lucro Líquido": lucro, "Total": saldo})
    st.table(pd.DataFrame(dados_ano).style.format({"Aporte": "R$ {:.2f}", "Lucro Líquido": "R$ {:.2f}", "Total": "R$ {:.2f}"}))

with tab2:
    st.subheader("🏁 Meta de Liberdade")
    alvo_mensal = st.number_input("Renda Mensal Desejada (R$):", value=5000)
    cap_alvo = alvo_mensal / taxa_mensal
    st.success(f"Patrimônio Alvo para Viver de Renda: **R$ {cap_alvo:,.2f}**")
    
    saldo_10, lista_10 = 0, []
    for ano in range(1, 11):
        for m in range(1, 13):
            aporte = aporte_extra if (m == 6 or m == 12) else aporte_base
            saldo_10 += aporte + (saldo_10 * taxa_mensal)
        lista_10.append({
            "Ano": f"Ano {ano}", 
            "Patrimônio": saldo_10, 
            "Renda Mensal": saldo_10 * taxa_mensal,
            "Progresso": f"{(saldo_10/cap_alvo)*100:.1f}%"
        })
    st.table(pd.DataFrame(lista_10).style.format({"Patrimônio": "R$ {:.2f}", "Renda Mensal": "R$ {:.2f}"}))

if st.sidebar.button("🔒 Sair"):
    st.session_state.auth = False
    st.rerun()
