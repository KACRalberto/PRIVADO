from flask import Flask, jsonify, g, request, session
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from extensions import conexion, jwt
from routes.CRUD import AUTH
import os
import loggers
from datetime import timedelta


load_dotenv()

app = Flask(__name__)

# ========== CONFIGURACIÓN CRUCIAL PARA SESIONES ==========
# Secret key debe ser DIFERENTE a JWT_SECRET_KEY
app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")

# ========== CONFIGURACIÓN DE SESIONES PARA CORS ==========
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Permite envío en requests desde frontend
# Use secure cookies when running in production over HTTPS
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'  # set to True on real server
app.config['SESSION_COOKIE_NAME'] = 'betodo_session'

# ========== CONFIGURACIÓN DE CORS ==========
CORS(
    app, 
    origins=["http://localhost:5173", "http://localhost:5174"],
    supports_credentials=True,  # IMPORTANTE: permite enviar cookies
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

##CONFIGURACION DE LA APP
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_ACCESS_EXPIRES"] = timedelta(hours=24)
jwt.init_app(app)
conexion.init_app(app)
############

### loggers de prueba 
debug_log = loggers.my_logger("debug_logger", "DEBUG", True, False)
file_log = loggers.my_logger("log_file", "WARNING", False, "MyLog.log")
debug_log.debug("hola")
file_log.warning("MENSAJE SALUDO DUPLICADO :):") ########## PREGUNTAR LUIS
file_log.warning("el unico")
###########

app.register_blueprint(AUTH)


# handle missing routes with JSON response (helps APIs and debugging)
@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.before_request
def before_request():
    """Marcar sesiones como permanentes"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

@app.after_request
# add modern security headers to every response
# this helps mitigate XSS, clickjacking, and content sniffing
# CSP is kept simple; adjust for production
# note: if the frontend is served from different origins modificar la política
# antes de desplegar en producción.
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    # Strict-Transport-Security se habilita sólo con HTTPS en producción
    # response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    return response

if __name__ == "__main__":
    app.run(debug = True)

