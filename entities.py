from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Profesor(db.Model):
    __tablename__ = 'profesor'
    cedula = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    min_max_dias = db.Column(db.String(50), nullable=True)
    ultima_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Preferencia
    preferencias = db.relationship('Preferencia', backref='profesor', lazy=True)

    def __repr__(self):
        return f'<Profesor {self.nombre_completo}>'


class Materia(db.Model):
    __tablename__ = 'materia'
    codigo = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    cantidad_dias = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Materia {self.nombre}>'


class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Turno {self.nombre}>'


class Horario(db.Model):
    __tablename__ = 'horario'
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Horario {self.hora_inicio} - {self.hora_fin}>'


class BloqueHorario(db.Model):
    __tablename__ = 'bloque_horario'
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(20), nullable=False)
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'), nullable=False)

    # Relación con Horario
    horario = db.relationship('Horario', backref='bloques_horarios', lazy=True)

    def __repr__(self):
        return f'<BloqueHorario {self.dia}>'


class Preferencia(db.Model):
    __tablename__ = 'preferencia'
    id = db.Column(db.Integer, primary_key=True)
    valor_prioridad = db.Column(db.Integer, nullable=False)
    profesor_cedula = db.Column(db.String(20), db.ForeignKey('profesor.cedula'), nullable=False)
    bloque_horario_id = db.Column(db.Integer, db.ForeignKey('bloque_horario.id'), nullable=False)

    # Relación con BloqueHorario
    bloque_horario = db.relationship('BloqueHorario', backref='preferencias', lazy=True)

    def __repr__(self):
        return f'<Preferencia {self.valor_prioridad}>'