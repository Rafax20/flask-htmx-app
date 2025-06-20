from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rafael:rafa123@localhost/Flaskbd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definimos un modelo de prueba
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    if nombre:
        nuevo = Usuario(nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()
    usuarios = Usuario.query.all()
    return render_template('_tabla_usuarios.html', usuarios=usuarios)

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios_json():
    usuarios = Usuario.query.all()  # Obtiene todos los registros reales de PostgreSQL
    resultado = [
        {'id': u.id, 'nombre': u.nombre} for u in usuarios
    ]
    return jsonify(resultado)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
