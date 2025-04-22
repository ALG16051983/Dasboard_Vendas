import requests

def buscar_pedidos(api_key):
    url = f"https://www.bling.com.br/Api/v2/pedidos/json/?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pedidos = []
        if "retorno" in data and "pedidos" in data["retorno"]:
            for item in data["retorno"]["pedidos"]:
                pedido = item.get("pedido", {})
                pedidos.append({
                    "numero": pedido.get("numero"),
                    "data": pedido.get("data"),
                    "cliente": pedido.get("cliente", {}).get("nome"),
                    "valor": pedido.get("valor")
                })
        return pedidos
    else:
        return []
