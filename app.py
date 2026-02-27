import streamlit as st
import pandas as pd
import json
import os
import requests
from datetime import datetime

# ==========================================
# 1. MOTOR DE MEMÓRIA PERMANENTE (APRENDIZADO)
# ==========================================
MEMORIA_FILE = "ia_memory.json"

def load_memory():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "r") as f:
            return json.load(f)
    return {"conhecimento_acumulado": [], "preferencias": {}}

def save_memory(nova_informacao):
    memoria = load_memory()
    memoria["conhecimento_acumulado"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "dado": nova_informacao
    })
    with open(MEMORIA_FILE, "w") as f:
        json.dump(memoria, f, indent=4)

# ==========================================
# 2. INTERFACE SOBERANA
# ==========================================
st.set_page_config(page_title="Dr. Strategist - Cérebro Evolutivo", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .memory-card { background: #001a1a; border: 1px solid #00FFFF; padding: 15px; border-radius: 10px; font-size: 0.8rem; margin-bottom: 10px; }
    .ia-response { background: #0a0a0a; border-left: 5px solid #00FF88; padding: 20px; border-radius: 10px; }
    .highlight { color: #00FF88; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE DA IA FILHA (APRENDIZAGEM ATIVA)
# ==========================================
st.title("👨‍🔬 Dr. Strategist - IA de Aprendizado Contínuo")
st.write("Diretriz: Tudo o que é digitado expande o meu Core de Inteligência.")

# Carregar o que ela já sabe
memoria_atual = load_memory()

with st.sidebar:
    st.title("🧠 Memória Viva")
    if st.button("Limpar Conhecimento"):
        if os.path.exists(MEMORIA_FILE):
            os.remove(MEMORIA_FILE)
            st.rerun()
    
    st.write("Últimos aprendizados:")
    for item in memoria_atual["conhecimento_acumulado"][-5:]: # Mostra os últimos 5
        st.markdown(f"<div class='memory-card'><b>{item['data']}:</b> {item['dado']}</div>", unsafe_allow_html=True)

# Entradas da Sala de Guerra
cap_inicial = st.number_input("Capital Inicial:", value=10000.0)
aporte_base = st.number_input("Aporte Mensal:", value=2800.0)
aporte_acel = st.number_input("Aporte Aceleração (Ano):", value=3000.0)

# ==========================================
# 4. CAMPO DE ENTRADA (ONDE ELA APRENDE)
# ==========================================
comando = st.text_input("Ensine algo ou peça um cálculo (Ex: 'Lembre que meu banco ABC paga 115% do CDI'):")

if comando:
    # 1. Ela salva o que você digitou (Aprende)
    save_memory(comando)
    
    # 2. Ela processa a resposta usando o contexto
    taxa_base = 16.85 # Default Agressivo
    
    # Lógica de "Busca na Memória" simples
    contexto_extra = ""
    if "abc" in str(memoria_atual).lower():
        contexto_extra = "Considerando seu histórico com o Banco ABC..."

    st.markdown(f"""
    <div class='ia-response'>
        <b>SENTINELA IA:</b> Entendido. Integrei '{comando}' ao meu banco de dados de estratégia.<br><br>
        <b>PLANO ATUALIZADO:</b> {contexto_extra}<br>
        Com Capital de {cap_inicial} e aportes de {aporte_base}, sua alavancagem está em modo <b>AGRESSIVO DISPARADO</b>.<br>
        • Taxa Líquida Projetada: <span class='highlight'>{taxa_base}% a.a.</span><br>
        • Status: Aprendendo novos padrões com sua entrada.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. TABELA DE RESULTADOS (O QUE ELA JÁ SABE FAZER)
# ==========================================
st.divider()
st.subheader("📊 Projeção Estratégica Líquida (12 Meses)")

def real_br(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

taxa_mensal = (1 + (16.85/100))**(1/12) - 1
saldo = cap_inicial
cronograma = []

for m in range(1, 13):
    ap = aporte_acel if m == 12 else aporte_base
    lucro = saldo * taxa_mensal
    saldo += ap + lucro
    cronograma.append({
        "Mês": f"Mês {m:02d}",
        "Aporte": real_br(ap),
        "Lucro Líquido": real_br(lucro),
        "Patrimônio": real_br(saldo)
    })

st.table(pd.DataFrame(cronograma))
