import streamlit as st
import pandas as pd
import requests

# 1. SEGURANÇA E ESTRUTURA
st.set_page_config(page_title="Wealth Catalyst IA", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    if not st.session_state.auth:
        st.title("🛡️ Wealth Catalyst IA")
        st.subheader("Scanner de Oportunidades em Tempo Real")
        senha = st.text_input("Chave de Segurança:", type="password")
        if st.button("Acessar Terminal"):
            if senha == "#1F2r34":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Acesso Negado.")
        return False
    return True

if login():
    # 2. MOTOR DE BUSCA E ANÁLISE TÉCNICA (Soberano)
    @st.cache_data(ttl=3600)
    def scanner_de_mercado():
        try:
            # Captura de indicadores macro
            selic = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
            ipca = float(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json", timeout=5).json()[0]['valor'])
            
            # Análise Comparativa de Ativos (Foco em Ganho Líquido)
            oportunidades = [
                {"Ativo": "LCI/LCA (Melhor Taxa)", "Rent_Anual": ipca + 6.5, "Categoria": "Renda Fixa Isenta", "Risco": "Baixo"},
                {"Ativo": "CDB (120% CDI)", "Rent_Anual": (selic * 1.20) * 0.825, "Categoria": "Renda Fixa Tributada", "Risco": "Baixo"},
                {"Ativo": "FIIs (Dividend Yield)", "Rent_Anual": 11.5, "Categoria": "Fundo Imobiliário", "Risco": "Moderado"},
                {"Ativo": "Ações (Crescimento/Div)", "Rent_Anual": 15.8, "Categoria": "Renda Variável", "Risco": "Alto"},
                {"Ativo": "CRI/CRA (Premium)", "Rent_Anual": ipca + 7.5, "Categoria": "Crédito Privado", "Risco": "Moderado"}
            ]
            return selic, ipca, oportunidades
        except:
            return 13.25, 4.50, []

    selic_at, ipca_at, radar = scanner_de_mercado()

    # 3. INTERFACE DE COMANDO
    st.sidebar.title("🕹️ Scanner de Ativos")
    st.sidebar.write(f"📊 **Macro:** SELIC {selic_at}% | IPCA {ipca_at}%")
    
    # Seleção baseada no Radar de Oportunidades
    df_radar = pd.DataFrame(radar)
    ativo_selecionado = st.sidebar.selectbox("Selecione o Ativo para o Plano:", df_radar['Ativo'].tolist())
    
    # Extração da taxa do ativo selecionado
    taxa_escolhida = df_radar[df_radar['Ativo'] == ativo_selecionado]['Rent_Anual'].values[0]
    taxa_mensal = (1 + (taxa_escolhida/100))**(1/12) - 1

    st.sidebar.divider()
    aporte_base = st.sidebar.number_input("Aporte Mensal (R$):", value=2500)
    aporte_acel = st.sidebar.number_input("Aporte Aceleração (R$):", value=3000)

    # 4. PAINEL DE CONTROLE DE CAPITAL
    st.title("🏆 Terminal Wealth Catalyst - Estratégia Soberana")
    
    # Radar de Oportunidades Visual
    st.markdown("### 🔍 Radar de Oportunidades (Top 5 Mercado)")
    st.table(df_radar.style.highlight_max(subset=['Rent_Anual'], color='#10b981'))

    tab1, tab2 = st.tabs(["📊 PLANO TÁTICO (1 ANO)", "🚀 ACELERAÇÃO 10 ANOS"])

    with tab1:
        st.subheader(f"Projeção Líquida: {ativo_selecionado}")
        saldo, logs = 0, []
        for m in range(1, 13):
            aporte = aporte_acel if m in [6, 12] else aporte_base
            lucro = saldo * taxa_mensal
            saldo += aporte + lucro
            logs.append({"Mês": m, "Aporte": aporte, "Lucro Líquido": lucro, "Patrimônio": saldo})
        
        st.table(pd.DataFrame(logs).style.format({
            "Aporte": "R$ {:.2f}", "Lucro Líquido": "R$ {:.2f}", "Patrimônio": "R$ {:.2f}"
        }))

    with tab2:
        st.subheader("🏁 Plano de Independência Financeira")
        renda_alvo = st.number_input("Renda Mensal Desejada (R$):", value=5000)
        capital_necessario = renda_alvo / taxa_mensal
        
        st.success(f"Seu Patrimônio Alvo: **R$ {capital_necessario:,.2f}**")
        
        saldo_10, lista_10 = 0, []
        for ano in range(1, 11):
            for m in range(1, 13):
                aporte = aporte_acel if (m == 6 or m == 12) else aporte_base
                saldo_10 += aporte + (saldo_10 * taxa_mensal)
            
            progresso = (saldo_10 / capital_necessario) * 100
            lista_10.append({
                "Ano": ano, 
                "Patrimônio": saldo_10, 
                "Renda Passiva": saldo_10 * taxa_mensal,
                "Status da Meta": f"{progresso:.1f}%"
            })
        
        st.table(pd.DataFrame(lista_10).style.format({"Patrimônio": "R$ {:.2f}", "Renda Passiva": "R$ {:.2f}"}))

    if st.sidebar.button("🔒 Encerrar"):
        st.session_state.auth = False
        st.rerun()
