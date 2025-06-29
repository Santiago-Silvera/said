from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = 'PERSONAS'
    __table_args__ = {'schema': 'said'}
    id_persona = db.Column(db.BigInteger, primary_key=True)
    nombres = db.Column(db.String, nullable=False)
    apellidos = db.Column(db.String, nullable=False)
    fecha_nacimiento = db.Column(db.SmallInteger, nullable=False)
    email_um = db.Column(db.String)
    email_personal = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Persona {self.id_persona} - {self.nombres} {self.apellidos}>'


class Profesor(db.Model):
    __tablename__ = 'PROFESORES'
    __table_args__ = {'schema': 'said'}
    id_persona = db.Column(db.BigInteger, db.ForeignKey('said.PERSONAS.id_persona'), primary_key=True)
    fecha_desde = db.Column(db.Date, primary_key=True)
    fecha_hasta = db.Column(db.Date)
    ddu_estatus = db.Column(db.String(2), nullable=False, default='NS')
    ddu_fecha_finalizado = db.Column(db.Date)

    persona = db.relationship('Persona', backref='profesores', lazy=True)

    def __repr__(self):
        return f'<Profesor {self.id_persona}>'


class Materia(db.Model):
    __tablename__ = 'MATERIAS'
    __table_args__ = {'schema': 'said'}
    cod_materia = db.Column(db.String(7), primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    creditos = db.Column(db.SmallInteger, nullable=False)
    horas_clase = db.Column(db.SmallInteger, nullable=False)
    horas_laboratorio = db.Column(db.SmallInteger, nullable=False, default=0)
    horas_semanales = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return f'<Materia {self.cod_materia}>'


class Curso(db.Model):
    __tablename__ = 'CURSOS'
    __table_args__ = {'schema': 'said'}
    id_curso = db.Column(db.BigInteger, primary_key=True)
    cod_materia = db.Column(db.String(7), db.ForeignKey('said.MATERIAS.cod_materia'), nullable=False)
    semestre = db.Column(db.SmallInteger, nullable=False)
    anio = db.Column(db.SmallInteger, nullable=False)

    materia = db.relationship('Materia', backref='cursos', lazy=True)

    def __repr__(self):
        return f'<Curso {self.id_curso}>'


class ProfesorMateria(db.Model):
    __tablename__ = 'PROFESORES_MATERIAS'
    __table_args__ = {'schema': 'said'}
    id_persona = db.Column(db.BigInteger, db.ForeignKey('said.PROFESORES.id_persona'), primary_key=True)
    cod_materia = db.Column(db.String(7), db.ForeignKey('said.MATERIAS.cod_materia'), primary_key=True)
    fecha_desde = db.Column(db.Date, primary_key=True)
    fecha_hasta = db.Column(db.Date)

    def __repr__(self):
        return f'<ProfesorMateria {self.id_persona} - {self.cod_materia}>'


class ProfesorCurso(db.Model):
    __tablename__ = 'PROFESORES_CURSOS'
    __table_args__ = {'schema': 'said'}
    id_persona = db.Column(db.BigInteger, db.ForeignKey('said.PROFESORES.id_persona'), primary_key=True)
    id_curso = db.Column(db.BigInteger, db.ForeignKey('said.CURSOS.id_curso'), primary_key=True)

    def __repr__(self):
        return f'<ProfesorCurso {self.id_persona} - {self.id_curso}>'


class Horario(db.Model):
    __tablename__ = 'HORARIOS'
    __table_args__ = {'schema': 'said'}
    hora_inicio = db.Column(db.Time, primary_key=True)
    hora_fin = db.Column(db.Time, primary_key=True)

    def __repr__(self):
        return f'<Horario {self.hora_inicio} - {self.hora_fin}>'


class BloqueHorario(db.Model):
    __tablename__ = 'BLOQUES_HORARIOS'
    __table_args__ = {'schema': 'said'}
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String, db.CheckConstraint("dia IN ('lun', 'mar', 'mie', 'jue', 'vie')"), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(['hora_inicio', 'hora_fin'], ['said.HORARIOS.hora_inicio', 'said.HORARIOS.hora_fin']),
        {'schema': 'said'}
    )
    horario = db.relationship('Horario', primaryjoin="and_(BloqueHorario.hora_inicio == Horario.hora_inicio, BloqueHorario.hora_fin == Horario.hora_fin)", lazy=True)

    def __repr__(self):
        return f'<BloqueHorario {self.id}>'


class Turno(db.Model):
    __tablename__ = 'TURNOS'
    __table_args__ = {'schema': 'said'}
    nombre = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f'<Turno {self.nombre}>'


class TurnoHorario(db.Model):
    __tablename__ = 'TURNOS_HORARIOS'
    __table_args__ = (
        db.PrimaryKeyConstraint('hora_inicio', 'hora_fin', 'turno'),
        db.ForeignKeyConstraint(['hora_inicio', 'hora_fin'], ['said.HORARIOS.hora_inicio', 'said.HORARIOS.hora_fin']),
        {'schema': 'said'}
    )
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    turno = db.Column(db.String(30), db.ForeignKey('said.TURNOS.nombre'))
    horario = db.relationship('Horario', primaryjoin="and_(TurnoHorario.hora_inicio == Horario.hora_inicio, TurnoHorario.hora_fin == Horario.hora_fin)", lazy=True)
    turno_rel = db.relationship('Turno', backref='turnos_horarios', lazy=True)

    def __repr__(self):
        return f'<TurnoHorario {self.hora_inicio} - {self.hora_fin} ({self.turno})>'


class PuedeDictar(db.Model):
    __tablename__ = 'PUEDE_DICTAR'
    __table_args__ = {'schema': 'said'}
    profesor = db.Column(db.BigInteger, db.ForeignKey('said.PROFESORES.id_persona'), primary_key=True)
    materia = db.Column(db.String(7), db.ForeignKey('said.MATERIAS.cod_materia'), primary_key=True)
    turno = db.Column(db.String(30), db.ForeignKey('said.TURNOS.nombre'), primary_key=True)
    grupos_max = db.Column(db.Integer, db.CheckConstraint("grupos_max > 0"), default=1)

    def __repr__(self):
        return f'<PuedeDictar {self.profesor} - {self.materia} ({self.turno})>'


class Prioridad(db.Model):
    __tablename__ = 'PRIORIDADES'
    __table_args__ = {'schema': 'said'}
    profesor = db.Column(db.String, primary_key=True)
    bloque_horario = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Prioridad {self.profesor} - {self.bloque_horario}: {self.valor}>'