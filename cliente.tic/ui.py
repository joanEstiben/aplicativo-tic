import socket
import os
import webview
from api import enviar_ticket_servidor


class Api:
    def __init__(self, server_ip, salon, hostname, local_ip):
        self.server_ip = server_ip
        self.salon = salon
        self.hostname = hostname
        self.local_ip = local_ip

    def enviar_ticket(self, categoria):
        payload = {
            "usuario": f"Salón {self.salon}",
            "hostname": self.hostname,
            "ip": self.local_ip,
            "salon": self.salon,
            "categoria": categoria,
            "descripcion": f"Reporte: {categoria}",
        }
        return enviar_ticket_servidor(self.server_ip, payload)


class AplicativoTICWidget:
    def __init__(self, root, server_ip, salon):
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "Desconocida"

        api = Api(server_ip, salon, hostname, local_ip)
        html_path = os.path.join(os.path.dirname(__file__), "app.html")

        window = webview.create_window(
            "Soporte TIC",
            url=f"file:///{html_path.replace(os.sep, '/')}",
            js_api=api,
            width=420,
            height=660,
            resizable=False,
            on_top=False,
        )

        def on_loaded():
            import base64
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            try:
                with open(logo_path, "rb") as f:
                    logo_b64 = base64.b64encode(f.read()).decode()
                logo_data = f"data:image/png;base64,{logo_b64}"
            except:
                logo_data = ""
            window.evaluate_js(
                f"setInfo('{salon}', '{hostname}', '{local_ip}', '{logo_data}')"
            )

        window.events.loaded += on_loaded
        webview.start()
