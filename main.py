import streamlit as st
import json
import pandas as pd
from helpers.bling_api import buscar_pedidos

st.title("Painel de Pedidos - Bling Integrado")

with open("contas.json", "r") as f:
    contas = json.load(f)["contas"]

if st.button("Buscar Pedidos"):
    todos_pedidos = []
    for conta in contas:
        pedidos = buscar_pedidos(conta["apikey"])
        for pedido in pedidos:
            pedido["origem"] = conta["nome"]
        todos_pedidos.extend(pedidos)
    
    df = pd.DataFrame(todos_pedidos)
    st.dataframe(df)

    st.download_button("Baixar em Excel", df.to_excel(index=False), file_name="pedidos.xlsx")
    st.download_button("Baixar em CSV", df.to_csv(index=False), file_name="pedidos.csv")
