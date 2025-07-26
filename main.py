import re
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import text
from correo import enviar_bienvenida
import os
# import requests

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creando tablas: {e}")


# Definimos un modelo de prueba
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()

    if not nombre or not correo:
        return "Nombre y correo son obligatorios", 400

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, correo):
        return "Correo con formato inválido", 400

    # Verificar si ya existe en la base
    existe = Usuario.query.filter_by(correo=correo).first()
    if existe:
        return "Este correo ya está registrado", 400

    nuevo_usuario = Usuario(nombre=nombre, correo=correo)
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Verificamos si es de Gmail
    if correo.endswith("@gmail.com"):
        enviar_bienvenida(correo, nombre)


    usuarios = Usuario.query.all()
    return render_template('_tabla_usuarios.html', usuarios=usuarios, correo=correo)


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios_json():
    usuarios = Usuario.query.all()  # Obtiene todos los registros reales de PostgreSQL
    resultado = [
        {'id': u.id, 'nombre': u.nombre} for u in usuarios
    ]
    return jsonify(resultado)

if __name__ == '__main__':
    with app.app_context():
         try:
            db.engine.execute(text("""
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) NOT NULL
            );
            """))
        except Exception as e:
            import sys
            print(f"Error creando tabla manualmente: {e}", file=sys.stderr)
    app.run(debug=True)

# Forzando redeploy para crear tablas
