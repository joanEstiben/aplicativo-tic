from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Habilita la comunicación sin bloqueos con el dashboard

# Configuración conectada a tu base de datos PROYECTO.TIC
DB_CONFIG = {
    "dbname": "PROYECTO.TIC",
    "user": "postgres",
    "password": "101606",  # <--- Cambia esto si tu contraseña es distinta
    "host": "localhost",
    "port": "5432",
}

def conectar_db():
    return psycopg2.connect(**DB_CONFIG)


@app.route("/api/tickets", methods=["POST"])
def recibir_ticket():
    data = request.get_json()
    usuario = data.get("usuario")
    hostname = data.get("hostname")
    ip = data.get("ip")
    salon = data.get("salon", "Sin especificar")
    categoria = data.get("categoria")
    descripcion = data.get("descripcion")

    if not usuario or not categoria:
        return jsonify({"error": "Faltan datos obligatorios (usuario o categoría)"}), 400

    codigo_ticket = f"TIC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = """
            INSERT INTO tickets (codigo_ticket, nombre_usuario, equipo_hostname, direccion_ip, salon, categoria, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pendiente')
        """
        cursor.execute(query, (codigo_ticket, usuario, hostname, ip, salon, str(categoria), descripcion))
        conexion.commit()
        cursor.close()
        conexion.close()

        print(f"[NUEVO CASO] Ticket {codigo_ticket} recibido de {usuario} ({hostname})")
        return jsonify({"mensaje": "Ticket registrado con éxito", "ticket": codigo_ticket}), 201
    except Exception as e:
        print(f"[ERROR DB TICKETS]: {e}")
        return jsonify({"error": "Error interno al guardar en la base de datos"}), 500


@app.route("/api/categorias", methods=["GET"])
def obtener_categorias():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, icono_base64, color_principal, color_fondo FROM categorias_tic ORDER BY id ASC;")
        filas = cursor.fetchall()
        
        categorias = []
        for fila in filas:
            categorias.append({
                "id": fila[0],
                "nombre": fila[1],
                "icono_base64": fila[2],
                "color": fila[3],
                "bg": "#f0fdf4",
                "circle_bg": fila[4]
            })
        cursor.close()
        conexion.close()
        return jsonify(categorias), 200
    except Exception as e:
        print(f"[ERROR DB CATEGORIAS]: {e}")
        return jsonify({"error": "No se pudieron obtener las categorías"}), 500


@app.route("/api/dashboard/stats", methods=["GET"])
def obtener_estadisticas():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets;")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado = 'Pendiente';")
        pendientes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado = 'En Proceso';")
        en_proceso = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado = 'Resuelto';")
        resueltos = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        
        return jsonify({"total": total, "pendientes": pendientes, "en_proceso": en_proceso, "resueltos": resueltos}), 200
    except Exception as e:
        print(f"[ERROR STATS]: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/dashboard/tickets", methods=["GET"])
def obtener_tickets_dashboard():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, codigo_ticket, salon, categoria, descripcion, estado, 
                   COALESCE(tecnico_asignado, 'Sin asignar'), 
                   TO_CHAR(fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') 
            FROM tickets ORDER BY id DESC;
        """)
        filas = cursor.fetchall()
        
        tickets = []
        for f in filas:
            tickets.append({
                "id": f[0],
                "codigo": f[1],
                "salon": f[2],
                "categoria": f[3],
                "descripcion": f[4] if f[4] else "Sin descripción adicional",
                "estado": f[5],
                "tecnico": f[6],
                "fecha": f[7] if f[7] else "Reciente"
            })
        cursor.close()
        conexion.close()
        return jsonify(tickets), 200
    except Exception as e:
        print(f"[ERROR DASHBOARD TICKETS]: {e}")
        return jsonify({"error": "No se pudieron obtener los tickets"}), 500


@app.route("/api/dashboard/actualizar/<int:ticket_id>", methods=["PUT"])
def actualizar_ticket(ticket_id):
    data = request.get_json()
    nuevo_estado = data.get("estado")
    nuevo_tecnico = data.get("tecnico")

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        query = "UPDATE tickets SET estado = %s, tecnico_asignado = %s WHERE id = %s"
        cursor.execute(query, (nuevo_estado, nuevo_tecnico, ticket_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "Ticket actualizado con éxito"}), 200
    except Exception as e:
        print(f"[ERROR ACTUALIZAR TICKET]: {e}")
        return jsonify({"error": "No se pudo actualizar el ticket"}), 500


@app.route("/api/auth/login", methods=["POST"])
def login_usuario():
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("password")

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, rol, password_hash FROM usuarios_tic WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        if usuario and usuario[3] == password:
            return jsonify({
                "exito": True,
                "id": usuario[0],
                "nombre": usuario[1],
                "rol": usuario[2]
            }), 200
        else:
            return jsonify({"exito": False, "error": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"[ERROR LOGIN]: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/admin/tecnicos", methods=["GET", "POST"])
def gestionar_tecnicos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    if request.method == "POST":
        data = request.get_json()
        nombre = data.get("nombre")
        correo = data.get("correo")
        password = data.get("password")

        try:
            cursor.execute(
                "INSERT INTO usuarios_tic (nombre, correo, password_hash, rol) VALUES (%s, %s, %s, 'tecnico')",
                (nombre, correo, password)
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Técnico agregado con éxito"}), 201
        except Exception as e:
            conexion.rollback()
            cursor.close()
            conexion.close()
            return jsonify({"error": "El correo ya está registrado o faltan datos"}), 400

    elif request.method == "GET":
        cursor.execute("SELECT id, nombre, correo, rol, estado FROM usuarios_tic ORDER BY id ASC;")
        filas = cursor.fetchall()
        tecnicos = [{"id": f[0], "nombre": f[1], "correo": f[2], "rol": f[3], "estado": f[4]} for f in filas]
        cursor.close()
        conexion.close()
        return jsonify(tecnicos), 200


@app.route("/api/admin/agenda", methods=["GET", "POST"])
def gestionar_agenda():
    conexion = conectar_db()
    cursor = conexion.cursor()

    if request.method == "POST":
        data = request.get_json()
        try:
            cursor.execute(
                """INSERT INTO agenda_tecnicos (tecnico_id, dia_semana, hora_inicio, hora_fin, sede, descripcion, creado_por)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (data.get("tecnico_id"), data.get("dia"), data.get("hora_inicio"), 
                 data.get("hora_fin"), data.get("sede", "Sede Principal"), 
                 data.get("descripcion"), data.get("creado_por", "Super Admin"))
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Turno diario registrado correctamente"}), 201
        except Exception as e:
            print(f"[ERROR AGENDA POST]: {e}")
            conexion.rollback()
            cursor.close()
            conexion.close()
            return jsonify({"error": str(e)}), 400

    elif request.method == "GET":
        cursor.execute("""
            SELECT a.id, u.nombre, a.dia_semana, a.hora_inicio, a.hora_fin, 
                   COALESCE(a.sede, 'Sede Principal'), a.descripcion
            FROM agenda_tecnicos a
            JOIN usuarios_tic u ON a.tecnico_id = u.id
            ORDER BY a.id DESC;
        """)
        filas = cursor.fetchall()
        agenda = [{
            "id": f[0], "tecnico": f[1], "dia": f[2], "inicio": f[3], 
            "fin": f[4], "sede": f[5], "descripcion": f[6]
        } for f in filas]
        cursor.close()
        conexion.close()
        return jsonify(agenda), 200


if __name__ == "__main__":
    print("🚀 Servidor central de Aplicativo TIC iniciado en el puerto 5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)