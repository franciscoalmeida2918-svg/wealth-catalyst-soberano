import streamlit as st
import pandas as pd
from model import (
    baixar_dados,
    criar_features,
    preparar_dados,
    treinar_modelo,
    gerar_sinais,
    simular_estrategia
)

st.set_page_config(page_title="IA Financeira", layout="wide")

st.title("📈 IA para Investimentos – Previsão e Estratégia")

ticker = st.sidebar.text_input("Ticker", "AAPL")
start = st.sidebar.date_input("Data inicial", pd.to_datetime("2015-01-01"))
n_lags = st.sidebar.slider("Número de Lags", 3, 20, 5)

if st.sidebar.button("Treinar IA"):
    with st.spinner("Baixando dados..."):
        df_raw = baixar_dados(ticker, str(start))

    with st.spinner("Criando features..."):
        df_feat = criar_features(df_raw, n_lags=n_lags)

    with st.spinner("Preparando dados..."):
        X, y, feature_cols = preparar_dados(df_feat)

    with st.spinner("Treinando modelo..."):
        modelo, mse_scores = treinar_modelo(X, y)

    st.success("Modelo treinado com sucesso!")
    st.write("MSE médio:", sum(mse_scores) / len(mse_scores))

    with st.spinner("Gerando sinais..."):
        df_signals = gerar_sinais(df_feat, modelo, feature_cols)

    with st.spinner("Simulando estratégia..."):
        df_resultado = simular_estrategia(df_signals)

    st.subheader("Equity Curve")
    st.line_chart(df_resultado[["Strategy_Equity", "Buy_Hold_Equity"]])

    st.subheader("Importância das Features")
    st.bar_chart(modelo.feature_importances_)
