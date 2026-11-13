import json
import os

# IP del equipo donde corre servidor_tic.py.
# En el mismo computador usa 127.0.0.1. En otro equipo de la red, la IP actual del servidor.
SERVER_IP = "127.0.0.1"

CONFIG_FILE = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    "AplicativoTIC",
    "config_tic.json",
)


def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None


def guardar_configuracion(salon):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"salon": salon}, f)
