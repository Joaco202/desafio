from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Configuración de la base de datos
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    rut = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    curso = db.Column(db.String(50), nullable=False)

@app.before_first_request
def crear_tablas():
    db.create_all()

@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.json
    est = Estudiante(
        rut=data['rut'], nombre=data['nombre'],
        edad=data['edad'], curso=data['curso']
    )
    db.session.add(est)
    db.session.commit()
    return jsonify(data), 201

@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([{
        'rut': e.rut, 'nombre': e.nombre,
        'edad': e.edad, 'curso': e.curso
    } for e in estudiantes])

@app.route('/estudiantes/<rut>', methods=['GET'])
def obtener_estudiante(rut):
    e = Estudiante.query.get(rut)
    if not e:
        return jsonify({'error':'No encontrado'}), 404
    return jsonify({
        'rut': e.rut, 'nombre': e.nombre,
        'edad': e.edad, 'curso': e.curso
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)