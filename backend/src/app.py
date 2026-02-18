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


# ========== CONFIGURACIÓN DE CORS ==========
CORS(
    app, 
    origins=["http://localhost:5173"],
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

@app.before_request
def before_request():
    """Marcar sesiones como permanentes"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

if __name__ == "__main__":
    app.run(debug = True)

