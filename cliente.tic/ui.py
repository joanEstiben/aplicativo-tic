import socket
import tkinter as tk
from tkinter import messagebox
from api import enviar_ticket_servidor


class AplicativoTICWidget:

    def __init__(self, root, server_ip):
        self.root = root
        self.server_ip = server_ip
        self.root.title("Aplicativo TIC - Soporte Técnico")
        self.root.geometry("380x480")
        self.root.resizable(False, False)
        self.root.config(bg="#f4f6f9")
        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado institucional
        tk.Label(
            self.root,
            text="🛠️ Aplicativo TIC - Soporte",
            font=("Arial", 14, "bold"),
            bg="#0f172a",
            fg="white",
            pady=12,
        ).pack(fill=tk.X)

        frame = tk.Frame(self.root, bg="#f4f6f9", padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        # Detección automática del equipo
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "Desconocida"

        tk.Label(
            frame,
            text=f"💻 PC: {hostname} | IP: {local_ip}",
            font=("Arial", 9),
            bg="#f4f6f9",
            fg="#64748b",
        ).pack(anchor="w", pady=(0, 10))

        # Campo Usuario
        tk.Label(
            frame,
            text="Tu Nombre / Departamento:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f9",
            fg="#334155",
        ).pack(anchor="w")
        self.txt_usuario = tk.Entry(frame, font=("Arial", 11), width=32)
        self.txt_usuario.pack(anchor="w", pady=(2, 10))

        # Campo Categoría
        tk.Label(
            frame,
            text="Categoría del Incidente:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f9",
            fg="#334155",
        ).pack(anchor="w")
        self.combo_categoria = tk.StringVar(value="Hardware (PC/Periféricos)")
        categorias = [
            "Hardware (PC/Periféricos)",
            "Red / Internet / Wi-Fi",
            "Software / Sistema Operativo",
            "Impresora / Escáner",
            "Otro",
        ]
        tk.OptionMenu(frame, self.combo_categoria, *categorias).pack(
            anchor="w", pady=(2, 10)
        )

        # Campo Descripción
        tk.Label(
            frame,
            text="Descripción del problema:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f9",
            fg="#334155",
        ).pack(anchor="w")
        self.txt_descripcion = tk.Text(
            frame, font=("Arial", 10), width=32, height=5, relief=tk.SOLID, bd=1
        )
        self.txt_descripcion.pack(anchor="w", pady=(2, 15))

        # Botón de envío
        tk.Button(
            frame,
            text="Enviar Solicitud a TIC",
            font=("Arial", 11, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            width=28,
            command=lambda: self.procesar_envio(hostname, local_ip),
        ).pack(anchor="center")

    def procesar_envio(self, hostname, local_ip):
        usuario = self.txt_usuario.get().strip()
        categoria = self.combo_categoria.get()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()

        if not usuario or not descripcion:
            messagebox.showwarning(
                "Campos Vacíos",
                "Por favor ingresa tu nombre y detalla el problema.",
            )
            return

        payload = {
            "usuario": usuario,
            "hostname": hostname,
            "ip": local_ip,
            "categoria": categoria,
            "descripcion": descripcion,
        }

        exito = enviar_ticket_servidor(self.server_ip, payload)
        if exito:
            messagebox.showinfo(
                "Éxito", "¡Tu reporte ha sido enviado al almacén de soporte!"
            )
            self.txt_descripcion.delete("1.0", tk.END)
        else:
            messagebox.showerror(
                "Error de Red",
                "No se pudo conectar con el servidor central de almacenamiento.",
            )
            #holaaaaaaaaaaaaa