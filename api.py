from functools import wraps
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app

import jwt
from models import db, Usuario, Empleado, Habitacion, TipoHabitacion, Reservacion

api = Blueprint('api', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = Usuario.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


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
        'id': user.id,
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

        return jsonify({"message": "TipoHabitacion creada Exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Mostrar Tipos
@api.route('/Tipos', methods=['GET'])
def mostrar_tipos():
    tipos = TipoHabitacion.query.all()
    return jsonify([tipo.to_dict() for tipo in tipos])


# Crear Habitacion
@api.route('/crearHabitacion', methods=['POST'])
def crear_habitacion():
    try:
        data = request.get_json()
        habitacion = Habitacion(**data)
        db.session.add(habitacion)
        db.session.commit()
        return jsonify({"message": "Habitacion  creada Exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Mostrar Habitaciones
@api.route('/Habitaciones', methods=['GET'])
def mostrar_habitaciones():
    habitaciones = Habitacion.query.all()
    return jsonify([habitacion.to_dict() for habitacion in habitaciones])


# Ruta para obtener una habitación por ID
@api.route('/Habitacion/<int:habitacion_id>', methods=['GET'])
def obtener_habitacion_por_id(habitacion_id):
    habitacion = Habitacion.query.get(habitacion_id)

    if habitacion:
        return jsonify(habitacion.to_dict())
    else:
        return jsonify({"mensaje": "Habitación no encontrada"}), 404


# Crear Reservacion
@api.route('/crearReservacion', methods=['POST'])
def crear_reservacion():
    data = request.get_json()
    reservacion = Reservacion(**data)
    db.session.add(reservacion)
    db.session.commit()


# Mostrar Reservaciones
@api.route('/Reservaciones', methods=['GET'])
def mostrar_reservaciones():
    reservaciones = Reservacion.query.all()
    return jsonify([reservacion.to_dict() for reservacion in reservaciones])


# Mostrar Reservaciones del usuario
@api.route('/Reservacion/<int:usuario_id>', methods=['GET'])
def mostrar_reservaciones_usuario(usuario_id):
    reservaciones = Reservacion.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([reservacion.to_dict() for reservacion in reservaciones])
