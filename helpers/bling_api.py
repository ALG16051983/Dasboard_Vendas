import requests

def buscar_pedidos(api_key):
    url = f"https://bling.com.br/Api/v2/pedidos/json/?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    pedidos = []
    for pedido in data.get("retorno", {}).get("pedidos", []):
        p = pedido["pedido"]
        pedidos.append({
            "data": p["data"],
            "numero": p["numero"],
            "cliente": p["cliente"]["nome"],
            "valor": p["valor"],
            "produtos": ", ".join([item["item"]["descricao"] for item in p.get("itens", [])])
        })
    return pedidos
