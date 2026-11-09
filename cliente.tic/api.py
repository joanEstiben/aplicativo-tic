import requests


def enviar_ticket_servidor(server_ip, payload):
  try:
    url = f"http://{server_ip}/api/tickets"
    response = requests.post(url, json=payload, timeout=5)
    return response.status_code in (200, 201)
  except Exception as e:
    return False