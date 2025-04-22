import streamlit as st
import json
import pandas as pd
from helpers.bling_api import buscar_pedidos
import io
from datetime import datetime

st.title("Painel de Pedidos - Bling Integrado")

# Carregar as contas do arquivo JSON
with open("contas.json", "r") as f:
    contas = json.load(f)["contas"]

# Filtros
st.sidebar.header("Filtros")
filtro_conta = st.sidebar.multiselect("Selecionar contas", [conta["nome"] for conta in contas], default=[conta["nome"] for conta in contas])
filtro_data_inicio = st.sidebar.date_input("Data inicial", value=None)
filtro_data_fim = st.sidebar.date_input("Data final", value=None)

# Botão para buscar os pedidos
if st.button("Buscar Pedidos"):
    todos_pedidos = []
    for conta in contas:
        if conta["nome"] not in filtro_conta:
            continue
        pedidos = buscar_pedidos(conta["apikey"])
        for pedido in pedidos:
            pedido["origem"] = conta["nome"]
        todos_pedidos.extend(pedidos)
    
    df = pd.DataFrame(todos_pedidos)

    # Convertendo a coluna de data para datetime e filtrando
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    if filtro_data_inicio:
        df = df[df["data"] >= pd.to_datetime(filtro_data_inicio)]
    if filtro_data_fim:
        df = df[df["data"] <= pd.to_datetime(filtro_data_fim)]

    st.subheader("Pedidos Encontrados")
    st.dataframe(df)

    # Gerar arquivos para download
    csv = df.to_csv(index=False)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)

    st.download_button("Baixar em CSV", data=csv, file_name="pedidos.csv", mime="text/csv")
    st.download_button("Baixar em Excel", data=excel_buffer, file_name="pedidos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
