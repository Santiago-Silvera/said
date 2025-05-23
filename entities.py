from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = 'personas'
    cedula = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=True)
    rol = db.Column(db.String, db.CheckConstraint("rol IN ('profesor', 'administrador')"), nullable=False)

    def __repr__(self):
        return f'<Persona {self.cedula} - {self.nombre}>'


class Profesor(db.Model):
    __tablename__ = 'profesores'
    cedula = db.Column(db.String, db.ForeignKey('personas.cedula'), nullable=False)
    nombre = db.Column(db.String, primary_key=True)
    nombre_completo = db.Column(db.String, unique=True)
    ultima_modificacion = db.Column(db.DateTime, nullable=True)
    min_max_dias = db.Column(db.String, db.CheckConstraint("min_max_dias IN ('min', 'max')"))
    mail = db.Column(db.String)

    # Rename the backref to avoid conflict
    preferencias = db.relationship('Prioridad', backref='profesor_pref', lazy=True)
    puede_dictar = db.relationship('PuedeDictar', backref='profesor_puede_dic', lazy=True)

    def __repr__(self):
        return f'<Profesor {self.nombre_completo}>'


class Materia(db.Model):
    __tablename__ = 'materias'
    codigo = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    nombre_completo = db.Column(db.String, unique=True)
    cantidad_dias = db.Column(db.Integer, db.CheckConstraint("cantidad_dias IN (0, 1, 2, 3, 4, 5)"), nullable=False)
    carga_horaria = db.Column(db.Integer, db.CheckConstraint("carga_horaria >= 0"), nullable=False)

    puede_dictar = db.relationship('PuedeDictar', backref='materia_puede_dic', lazy=True)

    def __repr__(self):
        return f'<Materia {self.nombre}>'


class Horario(db.Model):
    __tablename__ = 'horarios'
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('hora_inicio', 'hora_fin'),
    )

    def __repr__(self):
        return f'<Horario {self.hora_inicio} - {self.hora_fin}>'


class BloqueHorario(db.Model):
    __tablename__ = 'bloques_horarios'
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String, db.CheckConstraint("dia IN ('lun', 'mar', 'mie', 'jue', 'vie')"), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    # Define foreign keys for the composite primary key in Horario
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['hora_inicio', 'hora_fin'],
            ['horarios.hora_inicio', 'horarios.hora_fin']
        ),
    )

    # Define the relationship with Horario
    horario = db.relationship(
        'Horario',
        primaryjoin="and_(BloqueHorario.hora_inicio == Horario.hora_inicio, BloqueHorario.hora_fin == Horario.hora_fin)",
        lazy=True
    )

    def __repr__(self):
        return f'<BloqueHorario {self.dia}>'


class Prioridad(db.Model):
    __tablename__ = 'prioridades'
    profesor = db.Column(db.String, db.ForeignKey('profesores.cedula'), primary_key=True)
    bloque_horario = db.Column(db.Integer, db.ForeignKey('bloques_horarios.id'), primary_key=True)
    valor = db.Column(db.Integer, db.CheckConstraint("valor IN (0, 1, 2, 3)"), nullable=False)

    def __repr__(self):
        return f'<Prioridad {self.valor}>'


class Turno(db.Model):
    __tablename__ = 'turnos'
    nombre = db.Column(db.String, primary_key=True)

    turnos_horarios = db.relationship('TurnoHorario', backref='turno_backref', lazy=True)

    def __repr__(self):
        return f'<Turno {self.nombre}>'


class TurnoHorario(db.Model):
    __tablename__ = 'turnos_horarios'
    id = db.Column(db.Integer, db.ForeignKey('bloques_horarios.id'), primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    turno = db.Column(db.String, db.ForeignKey('turnos.nombre'), primary_key=True)

    # Define foreign keys for the composite primary key in Horario
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['hora_inicio', 'hora_fin'],
            ['horarios.hora_inicio', 'horarios.hora_fin']
        ),
    )

    horario = db.relationship(
        'Horario',
        primaryjoin="and_(TurnoHorario.hora_inicio == Horario.hora_inicio, TurnoHorario.hora_fin == Horario.hora_fin)",
        lazy=True
    )

    def __repr__(self):
        return f'<TurnoHorario {self.hora_inicio} - {self.hora_fin} ({self.turno})>'


class PuedeDictar(db.Model):
    __tablename__ = 'puede_dictar'
    profesor = db.Column(db.String, db.ForeignKey('profesores.cedula'), primary_key=True)
    materia = db.Column(db.String, db.ForeignKey('materias.codigo'), primary_key=True)
    turno = db.Column(db.String, db.ForeignKey('turnos.nombre'), primary_key=True)
    grupos_max = db.Column(db.Integer, db.CheckConstraint("grupos_max > 0"), default=1)

    def __repr__(self):
        return f'<PuedeDictar {self.profesor} - {self.materia} ({self.turno})>'