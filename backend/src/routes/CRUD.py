from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required
from extensions import conexion, crear_token
from werkzeug.security import generate_password_hash, check_password_hash
import loggers







AUTH = Blueprint("auth", __name__, url_prefix="/auth")

debugLog = loggers.my_logger("debug_logger", "DEBUG", True, False)
fileLog = loggers.my_logger("log_file", "WARNING", False, "MyLog.log")


@AUTH.route("/register", methods=["POST"])
def register():

    if "usuario_id" in session:
        return jsonify({"error": "Ya autenticado",
        "session" : session["usuario_token"]}), 400


    cursor=None
    data = request.get_json()

    if not data:
        return jsonify({'error':'Datos inválidos'}), 400

    email = data.get("email", "").strip().lower()
    userName = data.get("name", "Anónimo").strip()
    password = data.get("password", "")
    passwordCheck = data.get("password_check", "").strip()

    if not email or not password or not passwordCheck:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400   

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

        token = crear_token(email)

        session.clear()
        session["usuario_id"] = usuario["id"]
        session["usuario_email"] = usuario["email"]
        session["usuario_token"] = token

        return jsonify({
            'message': 'Usuario registrado correctamente',
            'token': token
        }), 200

    except Exception as e:
        print(e)
        fileLog.error(f"Error en register: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        if cursor:
            cursor.close()


@AUTH.route("/login", methods=["POST"])
def login():

    if "usuario_id" in session:
        return jsonify({"error": "Ya autenticado",
        "session" : session["usuario_token"]}), 400

    cursor=None
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password")

    print("DATA EN LOGIN", data)

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

        token = crear_token(userEmail)

        session.clear()
        session.permanent = True
        session["usuario_token"] = token
        session["usuario_id"] = userId
        session["usuario_email"] = userEmail
        session["usuario_name"] = userName
        
        print(f"✓ SESIÓN CREADA: usuario_id={userId}")
        print(f"✓ SESIÓN DATA: {dict(session)}")

        return jsonify({
            "token": token,
            "user": userName
        }), 200

    except Exception as e:
        print(f"✗ ERROR EN LOGIN: {str(e)}")
        fileLog.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        if cursor:
            cursor.close()



@AUTH.route("/tareas", methods=["POST"])
@jwt_required()
def postTareas():
    cursor=None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        titulo = data.get("titulo", "").strip()
        descripcion = data.get("descripcion", "").strip()
        estado = data.get("estado", "pendiente").strip().lower()

        if estado not in ("pendiente","hecho","cancelado"):
            estado = "pendiente"

        if not titulo:
            return jsonify({"error": "Título requerido"}), 400
        print(session)
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
        print(e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()


@AUTH.route("/tareas", methods=["GET"])
def getTareas():
    cursor=None
    try:

        if "usuario_id" not in session:
            return jsonify({"error": "No autenticado"}), 401

        userId = session["usuario_id"]

        cursor = conexion.connection.cursor()

        query = """
            SELECT id, titulo, descripcion, estado
            FROM tareas
            WHERE id_usuario = %s
            ORDER BY id DESC
            LIMIT 50
        """

        cursor.execute(query, (userId,))
        tareas = cursor.fetchall()

        return jsonify({
            "ok": True,
            "tareas": tareas
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        if cursor:
            cursor.close()

@AUTH.route("/logout")
def logout():
    session.clear()
    token=None
    return jsonify({"exito": "Sesión finalizada"}), 200