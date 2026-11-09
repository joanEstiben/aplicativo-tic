import json
import os

CONFIG_FILE = "config_tic.json"


def cargar_configuracion():
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    except:
      return None
  return None


def guardar_configuracion(server_ip):
  with open(CONFIG_FILE, "w") as f:
    json.dump({"server_ip": server_ip}, f)