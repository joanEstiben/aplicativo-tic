import tkinter as tk
from tkinter import messagebox
from config import cargar_configuracion, guardar_configuracion
from ui import AplicativoTICWidget


def pedir_ambiente_inicial():
    config = cargar_configuracion()
    if config and "server_ip" in config:
        return config["server_ip"]

    # Pantalla inicial de configuración (Solo la primera vez)
    setup_win = tk.Tk()
    setup_win.title("Configuración Inicial - Aplicativo TIC")
    setup_win.geometry("360x210")
    setup_win.resizable(False, False)
    setup_win.config(bg="#f4f6f9")

    tk.Label(
        setup_win,
        text="Configuración de Red TIC",
        font=("Arial", 12, "bold"),
        bg="#f4f6f9",
        fg="#0f172a",
    ).pack(pady=15)
    tk.Label(
        setup_win,
        text=(
            "Ingresa la IP y puerto del Servidor Central:\n(Ej:"
            " 10.1.173.187:5000)"
        ),
        font=("Arial", 9),
        bg="#f4f6f9",
        fg="#64748b",
        justify=tk.CENTER,
    ).pack(pady=5)

    txt_ip = tk.Entry(setup_win, font=("Arial", 11), width=25, justify=tk.CENTER)
    txt_ip.pack(pady=5)
    txt_ip.insert(0, "10.1.173.187:5000")

    server_ip_container = {"ip": None}

    def guardar_y_continuar():
        ip = txt_ip.get().strip()
        if not ip:
            messagebox.showwarning("Aviso", "Por favor ingresa una IP válida.")
            return
        guardar_configuracion(ip)
        server_ip_container["ip"] = ip
        setup_win.destroy()

    tk.Button(
        setup_win,
        text="Guardar e Iniciar Widget",
        font=("Arial", 10, "bold"),
        bg="#16a34a",
        fg="white",
        command=guardar_y_continuar,
    ).pack(pady=10)

    setup_win.mainloop()
    return server_ip_container["ip"]


if __name__ == "__main__":
    ip_servidor = pedir_ambiente_inicial()
    if ip_servidor:
        root = tk.Tk()
        app = AplicativoTICWidget(root, ip_servidor)
        root.mainloop()