from datetime import datetime
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Configuración conectada a tu base de datos PROYECTO.TIC
DB_CONFIG = {
    "dbname": "PROYECTO.TIC",
    "user": "postgres",
    "password": "101606",  # <--- CAMBIA ESTO por tu contraseña de postgres
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
  categoria = data.get("categoria")
  descripcion = data.get("descripcion")

  if not usuario or not descripcion:
    return (
        jsonify({"error": "Faltan datos obligatorios (usuario o descripción)"}),
        400,
    )

  codigo_ticket = f"TIC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

  try:
    conexion = conectar_db()
    cursor = conexion.cursor()

    query = """
            INSERT INTO tickets (codigo_ticket, nombre_usuario, equipo_hostname, direccion_ip, categoria, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pendiente')
        """
    cursor.execute(
        query,
        (codigo_ticket, usuario, hostname, ip, categoria, descripcion),
    )
    conexion.commit()

    cursor.close()
    conexion.close()

    print(
        f"[NUEVO CASO] Ticket {codigo_ticket} recibido de {usuario} ({hostname})"
    )
    return (
        jsonify({
            "mensaje": "Ticket registrado con éxito",
            "ticket": codigo_ticket,
        }),
        201,
    )

  except Exception as e:
    print(f"[ERROR DB]: {e}")
    return jsonify({"error": "Error interno al guardar en la base de datos"}), 500


if __name__ == "__main__":
  print("🚀 Servidor central de Aplicativo TIC iniciado en el puerto 5000...")
  app.run(host="0.0.0.0", port=5000, debug=False)