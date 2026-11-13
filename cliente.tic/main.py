import os
import json
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from config import SERVER_IP
from ui import AplicativoTICWidget

# Configurar el tema oscuro para que coincida con tu diseño principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"

def cargar_configuracion_avanzada():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return None

def guardar_configuracion_avanzada(tipo, salon):
    config = {"tipo": tipo, "salon": salon}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def pedir_configuracion_inicial():
    config = cargar_configuracion_avanzada()
    if config:
        return config

    import base64
    from PIL import Image, ImageTk

    win = ctk.CTk()
    win.title("Configuración Inicial - Soporte TIC")
    win.geometry("400x460")
    win.resizable(False, False)
    win.configure(fg_color="#0f172a")

    # Orbes decorativos de fondo
    canvas = ctk.CTkCanvas(win, bg="#0f172a", highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.create_oval(-80, -80, 220, 220, fill="#1e1b4b", outline="")
    canvas.create_oval(250, 300, 480, 520, fill="#0c2340", outline="")

    card = ctk.CTkFrame(win, fg_color="#1e293b", corner_radius=20,
                        border_width=1, border_color="#334155")
    card.pack(fill="both", expand=True, padx=22, pady=22)

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    try:
        pil_img = Image.open(logo_path).convert("RGBA")
        pil_img.thumbnail((160, 60), Image.LANCZOS)
        logo_ctk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(pil_img.width, pil_img.height))
        ctk.CTkLabel(card, image=logo_ctk, text="").pack(pady=(22, 6))
    except:
        ctk.CTkLabel(card, text="🛠️", font=ctk.CTkFont("Arial", 40)).pack(pady=(22, 6))

    ctk.CTkLabel(card, text="Soporte Técnico TIC",
                 font=ctk.CTkFont("Arial", 17, "bold"),
                 text_color="#f8fafc").pack(pady=(0, 2))
    ctk.CTkLabel(card, text="Selecciona el rol de este equipo",
                 font=ctk.CTkFont("Arial", 10),
                 text_color="#64748b").pack(pady=(0, 18))

    # Separador
    ctk.CTkFrame(card, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=(0, 16))

    ctk.CTkLabel(card, text="Rol del Equipo:",
                 font=ctk.CTkFont("Arial", 11, "bold"),
                 text_color="#cbd5e1").pack(anchor="w", padx=24)

    rol_var = ctk.StringVar(value="Estudiante (Kiosco Salón)")

    frame_salon = ctk.CTkFrame(card, fg_color="transparent")

    lbl_salon = ctk.CTkLabel(frame_salon, text="Número de Salón / Ambiente:",
                              font=ctk.CTkFont("Arial", 11, "bold"),
                              text_color="#cbd5e1")
    lbl_salon.pack(anchor="w", padx=4)
    txt_salon = ctk.CTkEntry(frame_salon, placeholder_text="Ej: Salón 1401",
                              height=38, font=ctk.CTkFont("Arial", 12))
    txt_salon.pack(fill="x", pady=(4, 0))

    def actualizar_interfaz(choice):
        if "Administrador" in choice:
            frame_salon.pack_forget()
        else:
            frame_salon.pack(fill="x", padx=20, pady=(10, 0), after=combo_rol)

    combo_rol = ctk.CTkComboBox(
        card,
        values=["Estudiante (Kiosco Salón)", "Administrador (Técnico)"],
        variable=rol_var, command=actualizar_interfaz,
        height=38, font=ctk.CTkFont("Arial", 12),
        fg_color="#0f172a", border_color="#334155",
        button_color="#6366f1", button_hover_color="#4f46e5",
    )
    combo_rol.pack(fill="x", padx=20, pady=(4, 0))
    frame_salon.pack(fill="x", padx=20, pady=(10, 0))

    resultado_ref = {"config": None}

    def guardar():
        seleccion = rol_var.get()
        es_admin = "Administrador" in seleccion
        tipo = "admin" if es_admin else "estudiante"
        salon = txt_salon.get().strip() if not es_admin else "ADMIN"
        if not es_admin and not salon:
            messagebox.showwarning("Aviso", "Por favor ingresa el número de salón.")
            return
        guardar_configuracion_avanzada(tipo, salon)
        resultado_ref["config"] = {"tipo": tipo, "salon": salon}
        win.destroy()

    ctk.CTkButton(
        card, text="Guardar e Iniciar →", command=guardar,
        fg_color="#6366f1", hover_color="#4f46e5",
        font=ctk.CTkFont("Arial", 12, "bold"),
        corner_radius=12, height=44,
    ).pack(fill="x", padx=20, pady=(20, 20))

    win.mainloop()
    return resultado_ref["config"]


if __name__ == "__main__":
    config = pedir_configuracion_inicial()
    
    if config:
        if config["tipo"] == "admin":
            print("🚀 Abriendo Dashboard de Administrador...")
            import webview
            import os
            dash_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dashboard.html"))
            webview.create_window("Panel de Control - Soporte TIC", url=f"file:///{dash_path.replace(os.sep, '/')}", width=1200, height=700)
            webview.start()
        else:
            print(f"🚀 Iniciando Widget Kiosco para el Salón: {config['salon']}")
            AplicativoTICWidget(None, SERVER_IP, config["salon"])
