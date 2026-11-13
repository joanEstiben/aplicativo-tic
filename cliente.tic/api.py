import requests


def url_servidor(server_ip, ruta):
    host = str(server_ip).strip().replace("http://", "").replace("https://", "").rstrip("/")
    if ":" not in host:
        host = f"{host}:5000"
    return f"http://{host}{ruta}"


def enviar_ticket_servidor(server_ip, payload):
    try:
        url = url_servidor(server_ip, "/api/tickets")
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 201:
            print(f"Error al enviar ticket: {response.status_code} {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error al enviar ticket: {e}")
        return False

def obtener_categorias_servidor(server_ip):
    try:
        url = url_servidor(server_ip, "/api/categorias")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error al obtener categorías del servidor: {e}")
    return []  # Retorna lista vacía si hay algún fallo para evitar que la app se caiga