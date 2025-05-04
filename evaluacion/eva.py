from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests

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

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut_estudiante = db.Column(db.String(20), nullable=False)
    semestre = db.Column(db.String(20), nullable=False)
    asignatura = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Float, nullable=False)

@app.before_first_request
def crear_tablas():
    db.create_all()

@app.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.json
    # Verificar estudiante existe
    est_url = f"{os.getenv('EST_SERVICE_URL')}/estudiantes/{data['rut_estudiante']}"
    resp = requests.get(est_url)
    if resp.status_code != 200:
        return jsonify({'error':'Estudiante no existe'}), 400

    ev = Evaluacion(
        rut_estudiante=data['rut_estudiante'], semestre=data['semestre'],
        asignatura=data['asignatura'], nota=data['nota']
    )
    db.session.add(ev)
    db.session.commit()
    return jsonify(data), 201

@app.route('/evaluaciones', methods=['GET'])
def listar_evaluaciones():
    evs = Evaluacion.query.all()
    return jsonify([{
        'id': e.id,
        'rut_estudiante': e.rut_estudiante,
        'semestre': e.semestre,
        'asignatura': e.asignatura,
        'nota': e.nota
    } for e in evs])

@app.route('/evaluaciones/<rut>', methods=['GET'])
def por_estudiante(rut):
    evs = Evaluacion.query.filter_by(rut_estudiante=rut).all()
    return jsonify([{
        'id': e.id,
        'rut_estudiante': e.rut_estudiante,
        'semestre': e.semestre,
        'asignatura': e.asignatura,
        'nota': e.nota
    } for e in evs])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)