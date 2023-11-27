from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    hospedado = db.Column(db.Boolean, default=False)
    reservaciones = db.relationship('Reservacion', back_populates='usuario')
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, nombre=self.nombre, email=self.email)


class Empleado(db.Model):
    __tablename__ = "empleado"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(255), default="colaborador")
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        empleado = cls.query.filter_by(email=email).first()
        if not empleado or not check_password_hash(empleado.password, password):
            return None

        return empleado

    def to_dict(self):
        return dict(id=self.id, nombre=self.nombre, email=self.email)


class TipoHabitacion(db.Model):
    __tablename__ = "tipo_habitacion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(255), unique=True)
    descripcion = db.Column(db.String(255), nullable=True)
    habitaciones = db.relationship('Habitacion', back_populates='tipo_habitacion', lazy='dynamic')
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __init__(self, tipo, descripcion):
        self.tipo = tipo
        self.descripcion = descripcion

    def to_dict(self):
        return dict(id=self.id,
                    tipo=self.tipo,
                    descripcion=self.descripcion,)


class Habitacion(db.Model):
    __tablename__ = "habitaciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imagen = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.String(255), nullable=False)
    tipo_habitacion_id = db.Column(db.Integer, db.ForeignKey('tipo_habitacion.id'))
    tipo_habitacion = db.relationship('TipoHabitacion', back_populates='habitaciones', lazy='select')
    reservaciones = db.relationship('Reservacion', back_populates='habitacion')
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __init__(self, imagen, nombre, numero, costo, tipo):
        self.imagen = imagen
        self.nombre = nombre
        self.numero = numero
        self.costo = costo
        self.tipo_habitacion_id = tipo

    def to_dict(self):
        return dict(id=self.id, imagen=self.imagen, nombre=self.nombre,
                    numero=self.numero, costo=self.costo,
                    tipo=self.tipo_habitacion.to_dict())


class Reservacion(db.Model):
    __tablename__ = "reservacion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservado_desde = db.Column(db.DateTime, default=datetime.utcnow)
    dias = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitaciones.id'))
    usuario = db.relationship('Usuario', back_populates='reservaciones')
    habitacion = db.relationship('Habitacion', back_populates='reservaciones')
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __init__(self, dias, usuario, habitacion):
        self.dias = dias
        self.usuario_id = usuario
        self.habitacion_id = habitacion

    def to_dict(self):
        return dict(id=self.id,
                    fecha_inicial=self.reservado_desde.strftime('%d-%m-%Y'),
                    dias=self.dias,
                    usuario=self.usuario.nombre if self.usuario else None,
                    habitacion=self.habitacion.numero if self.habitacion else None)
