from flask import Flask, send_from_directory
from flask_cors import CORS
from task_manager.routes.crud_routes import crud_bp
from task_manager.routes.ia_routes import ia_bp
from task_manager.routes.user_story_routes import user_story_bp
import os
from flask_sqlalchemy import SQLAlchemy
from task_manager.connection import connection
import pymysql
from task_manager.models.db import db

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
# app.register_blueprint(task_bp)
app.register_blueprint(crud_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(user_story_bp)

# Ruta para servir la interfaz web
@app.route('/')
def serve_ui():
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui')), 'index.html')

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui')), path)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{connection.DB_USER}:{connection.DB_PASSWORD}@{connection.DB_HOST}:{connection.DB_PORT}/{connection.DB_NAME}?ssl_verify_cert=false"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_database_if_not_exists():
    import pymysql
    # Forzar conexión SSL sin verificación de certificado (compatible con Azure)
    conn = pymysql.connect(
        host=connection.DB_HOST,
        user=connection.DB_USER,
        password=connection.DB_PASSWORD,
        port=int(connection.DB_PORT),
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ssl': {}}
    )
    db_name = connection.DB_NAME
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
    finally:
        conn.close()

create_database_if_not_exists()

with app.app_context():
    from task_manager.models import UserStory, Task
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)