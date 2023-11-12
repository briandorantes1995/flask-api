from functools import wraps
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app

import jwt
from models import db, Usuario, Empleado, Habitacion, TipoHabitacion, Reservacion

api = Blueprint('api', __name__)


@api.route('/')
def hello_world():
    return 'Inicio Proy Int 2'


@api.route('/registro', methods=('POST',))
def register():
    data = request.get_json()
    user = Usuario(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = Usuario.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({'token': token})


# Mostrar de Usuarios
@api.route('/mostrarUsuarios', methods=['GET'])
def mostrar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([s.to_dict() for s in usuarios])


# Habitaciones----------------------------------------------------------------------------------------------------------
# Creat Tipo(doble,sencilla...)
@api.route('/crearTipo', methods=['POST'])
def crear_tipo():
    try:
        data = request.get_json()
        tipo = TipoHabitacion(**data)
        db.session.add(tipo)
        db.session.commit()

        return jsonify({"message": "TipoHabitacion created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Mostrar Tipos
@api.route('/Tipos', methods=['GET'])
def mostrar_tipos():
    tipos = TipoHabitacion.query.all()
    return jsonify([s.to_dict() for s in tipos])


# Crear Habitacion
@api.route('/crearHabitacion', methods=['POST'])
async def crear_habitacion():
    data = request.get_json()
    habitacion = Habitacion(**data)
    db.session.add(habitacion)
    db.session.commit()


# Mostrar Habitaciones
@api.route('/Habitaciones', methods=['GET'])
def mostrar_habitaciones():
    habitaciones = Habitacion.query.all()
    return jsonify([s.to_dict() for s in habitaciones])
