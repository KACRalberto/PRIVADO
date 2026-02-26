from flask import Blueprint, jsonify, request, session
from extensions import conexion, crear_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import loggers
from uuid import uuid4
from datetime import datetime, timedelta

# utilities for sanitization/validation
import re
import bleach

# compile once for performance
_email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def sanitize_text(text: str) -> str:
    """Clean input from any HTML/script tags. Strips dangerous content."""
    if text is None:
        return ""
    # bleach.clean removes tags, attributes by default and escapes
    return bleach.clean(text, strip=True)


def is_valid_email(email: str) -> bool:
    return bool(_email_regex.match(email))







AUTH = Blueprint("auth", __name__, url_prefix="/auth")

debugLog = loggers.my_logger("debug_logger", "DEBUG", True, False)
fileLog = loggers.my_logger("log_file", "WARNING", False, "MyLog.log")


@AUTH.route("/register", methods=["POST"])
def register():

    # if "usuario_id" in session:
    #     return jsonify({"error": "Ya autenticado",
    #     "session" : session["usuario_token"]}), 400


    cursor=None
    data = request.get_json()
    print("DATA", data) 
    if not data:
        return jsonify({'error':'Datos inválidos'}), 400

    # sanitize all string inputs to strip html/js and trim whitespace
    email = sanitize_text(data.get("email", "")).strip().lower()
    userName = sanitize_text(data.get("name", "Anónimo")).strip()
    password = data.get("password", "")
    passwordCheck = sanitize_text(data.get("password_check", "")).strip()

    # basic format checks
    if not is_valid_email(email):
        return jsonify({'error': 'Email no válido'}), 400

    if not email or not password or not passwordCheck:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400   

    # simple length limits to guard contra datos masivos
    if len(email) > 254 or len(userName) > 50:
        return jsonify({'error': 'Campo demasiado largo'}), 400

    if len(password) < 5:
        return jsonify({"error":"Password demasiado corta"}), 400


    if passwordCheck != password:
        return jsonify({"error": "Las contraseñas deben coincidir"}), 400

    try:
        cursor = conexion.connection.cursor()

        queryCheck = "SELECT id FROM usuarios WHERE email = %s"
        cursor.execute(queryCheck, (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({'error': 'El email ya está registrado'}), 409

        passwordHash = generate_password_hash(password)

        queryInsert = """
            INSERT INTO usuarios (email, password, username)
            VALUES (%s, %s, %s)
        """
        cursor.execute(queryInsert, (email, passwordHash, userName))
        conexion.connection.commit()

        queryUser = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(queryUser, (email,))
        usuario = cursor.fetchone()

        token = crear_token(str(usuario["id"]))

        session.clear()
        session.permanent = True
        session["usuario_id"] = usuario["id"]
        session["usuario_email"] = usuario["email"]
        session["usuario_token"] = token

        return jsonify({
            'message': 'Usuario registrado correctamente',
            'token': token,
            'user': usuario["username"]
        }), 200

    except Exception as e:
        fileLog.error(f"Error en register: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        if cursor:
            cursor.close()


@AUTH.route("/login", methods=["POST"])
def login():

    # if "usuario_id" in session:
    #     return jsonify({"error": "Ya autenticado",
    #     "session" : session["usuario_token"]}), 400

    cursor=None
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = sanitize_text(data.get("email", "")).strip().lower()
    password = data.get("password")

    if not is_valid_email(email):
        return jsonify({'error': 'Email no válido'}), 400

    if not email or not password:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    try:
        cursor = conexion.connection.cursor()

        queryCheck = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(queryCheck, (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        passwordOk = check_password_hash(user["password"], password)

        if not passwordOk:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        userId = user["id"]
        userEmail = user["email"]
        userName = user["username"]

        token = crear_token(str(user["id"]))

        session.clear()
        session.permanent = True
        session["usuario_token"] = token
        session["usuario_id"] = userId
        session["usuario_email"] = userEmail
        session["usuario_name"] = userName
        

        return jsonify({
            "token": token,
            "user": userName
        }), 200

    except Exception as e:
        fileLog.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        if cursor:
            cursor.close()



@AUTH.route("/tareas", methods=["POST"])
@jwt_required()
def postTareas():
    # Verificar que el usuario esté autenticado en sesión o con JWT
    if "usuario_id" not in session:
        # allow fallback to JWT identity
        session["usuario_id"] = get_jwt_identity()
    if "usuario_id" not in session:
        return jsonify({"error": "No autenticado"}), 401
    

    cursor=None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        titulo = sanitize_text(data.get("titulo", "")).strip()
        descripcion = sanitize_text(data.get("descripcion", "")).strip()
        estado = sanitize_text(data.get("estado", "pendiente")).strip().lower()

        if estado not in ("pendiente","en_marcha","completada"):
            estado = "pendiente"

        if not titulo:
            return jsonify({"error": "Título requerido"}), 400
        if len(titulo) > 100 or len(descripcion) > 1000:
            return jsonify({"error": "Texto demasiado largo"}), 400

        userId = session["usuario_id"]

        cursor = conexion.connection.cursor()

        query = """
            INSERT INTO tareas (id_usuario, titulo, descripcion, estado)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (userId, titulo, descripcion, estado))
        conexion.connection.commit()

        return jsonify({
            "status": "ok"
        }), 201

    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()


@AUTH.route("/tareas", methods=["GET"])
@jwt_required()
def getTareas():
    cursor=None
    try:

        if "usuario_id" not in session:
            session["usuario_id"] = get_jwt_identity()
        if "usuario_id" not in session:
            return jsonify({"error": "No autenticado"}), 401

        userId = session["usuario_id"]

        cursor = conexion.connection.cursor()

        query = """
            SELECT id_tarea, titulo, descripcion, estado
            FROM tareas
            WHERE id_usuario = %s
            ORDER BY id_tarea DESC
            LIMIT 50
        """

        cursor.execute(query, (userId,))
        tareas = cursor.fetchall()
        return jsonify({
            "ok": True,
            "tareas": tareas
        }), 200

    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()

@AUTH.route("/tareas/<int:tarea_id>", methods=["PUT"])
@jwt_required()
def updateTarea(tarea_id):
    cursor=None
    try:
        if "usuario_id" not in session:
            session["usuario_id"] = get_jwt_identity()
        if "usuario_id" not in session:
            return jsonify({"error": "No autenticado"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        userId = session["usuario_id"]
        nuevoEstado = sanitize_text(data.get("estado", "")).strip().lower()

        if nuevoEstado not in ("pendiente", "en_marcha", "completada"):
            return jsonify({"error": "Estado inválido"}), 400

        cursor = conexion.connection.cursor()

        # Verificar que la tarea pertenece al usuario
        queryCheck = "SELECT id_usuario FROM tareas WHERE id_tarea = %s"
        cursor.execute(queryCheck, (tarea_id,))
        tarea = cursor.fetchone()

        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404

        if tarea["id_usuario"] != userId:
            return jsonify({"error": "No autorizado"}), 403

        # Actualizar la tarea
        query = "UPDATE tareas SET estado = %s WHERE id_tarea = %s"
        cursor.execute(query, (nuevoEstado, tarea_id))
        conexion.connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Tarea actualizada"
        }), 200

    except Exception as e:
        fileLog.error(f"Error en updateTarea: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()

@AUTH.route("/tareas/<int:tarea_id>", methods=["DELETE"])
@jwt_required()
def deleteTarea(tarea_id):
    cursor=None
    try:
        if "usuario_id" not in session:
            session["usuario_id"] = get_jwt_identity()
        if "usuario_id" not in session:
            return jsonify({"error": "No autenticado"}), 401

        userId = session["usuario_id"]

        cursor = conexion.connection.cursor()

        # Verificar que la tarea pertenece al usuario
        queryCheck = "SELECT id_usuario FROM tareas WHERE id_tarea = %s"
        cursor.execute(queryCheck, (tarea_id,))
        tarea = cursor.fetchone()

        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404

        if tarea["id_usuario"] != userId:
            return jsonify({"error": "No autorizado"}), 403

        # Eliminar la tarea
        query = "DELETE FROM tareas WHERE id_tarea = %s"
        cursor.execute(query, (tarea_id,))
        conexion.connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Tarea eliminada"
        }), 200

    except Exception as e:
        fileLog.error(f"Error en deleteTarea: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()

@AUTH.route("/tareas", methods=["DELETE"])
@jwt_required()
def deleteAllTareas():
    cursor=None
    try:
        if "usuario_id" not in session:
            session["usuario_id"] = get_jwt_identity()
        if "usuario_id" not in session:
            return jsonify({"error": "No autenticado"}), 401

        userId = session["usuario_id"]

        cursor = conexion.connection.cursor()

        # Eliminar todas las tareas del usuario
        query = "DELETE FROM tareas WHERE id_usuario = %s"
        cursor.execute(query, (userId,))
        conexion.connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Todas las tareas eliminadas"
        }), 200

    except Exception as e:
        fileLog.error(f"Error en deleteAllTareas: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()

@AUTH.route("/logout")
def logout():
    session.clear()
    token=None
    return jsonify({"exito": "Sesión finalizada"}), 200


# Endpoint para solicitar recuperación de contraseña
@AUTH.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    cursor = None
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"error": "Email requerido"}), 400

    email = sanitize_text(data.get("email")).strip().lower()
    if not is_valid_email(email):
        return jsonify({"error": "Email no válido"}), 400

    try:
        cursor = conexion.connection.cursor()
        queryUser = "SELECT id, email, username FROM usuarios WHERE email = %s"
        cursor.execute(queryUser, (email,))
        user = cursor.fetchone()

        if not user:
            # Para no revelar existencia de cuenta, devolver 200
            return jsonify({"message": "Si existe la cuenta, se ha enviado un correo"}), 200

        # Crear tabla password_resets si no existe
        queryCreate = '''
            CREATE TABLE IF NOT EXISTS password_resets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                token VARCHAR(128) NOT NULL,
                expires DATETIME NOT NULL,
                used TINYINT(1) DEFAULT 0
            ) ENGINE=InnoDB;
        '''
        cursor.execute(queryCreate)

        reset_token = uuid4().hex
        expires = datetime.utcnow() + timedelta(hours=1)

        queryInsert = "INSERT INTO password_resets (user_id, token, expires) VALUES (%s, %s, %s)"
        cursor.execute(queryInsert, (user['id'], reset_token, expires))
        conexion.connection.commit()

        # Devolver token al frontend para que este lo inserte en el email (EmailJS)
        return jsonify({"message": "Token creado", "token": reset_token}), 200

    except Exception as e:
        fileLog.error(f"Error en request_password_reset: {str(e)}")
        return jsonify({"error": "Error interno"}), 500
    finally:
        if cursor:
            cursor.close()


# Endpoint para aplicar nuevo password usando token
@AUTH.route("/reset-password", methods=["POST"])
def reset_password():
    cursor = None
    data = request.get_json()
    if not data or not data.get("token") or not data.get("password"):
        return jsonify({"error": "Token y password requeridos"}), 400

    token = sanitize_text(data.get("token"))
    new_password = data.get("password")  # password itself not sanitized so hash remains deterministic

    if len(new_password) < 5:
        return jsonify({"error": "Password demasiado corta"}), 400

    try:
        cursor = conexion.connection.cursor()
        query = "SELECT id, user_id, expires, used FROM password_resets WHERE token = %s"
        cursor.execute(query, (token,))
        record = cursor.fetchone()

        if not record:
            return jsonify({"error": "Token inválido"}), 400

        if record['used']:
            return jsonify({"error": "Token ya usado"}), 400

        expires = record['expires']
        # expires viene como datetime desde MySQL; comparar con UTC now
        if expires < datetime.utcnow():
            return jsonify({"error": "Token expirado"}), 400

        # Actualizar password del usuario
        passwordHash = generate_password_hash(new_password)
        queryUpdate = "UPDATE usuarios SET password = %s WHERE id = %s"
        cursor.execute(queryUpdate, (passwordHash, record['user_id']))

        # Marcar token como usado
        queryMark = "UPDATE password_resets SET used = 1 WHERE id = %s"
        cursor.execute(queryMark, (record['id'],))

        conexion.connection.commit()

        return jsonify({"message": "Contraseña actualizada"}), 200

    except Exception as e:
        fileLog.error(f"Error en reset_password: {str(e)}")
        return jsonify({"error": "Error interno"}), 500
    finally:
        if cursor:
            cursor.close()