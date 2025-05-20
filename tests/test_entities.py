from datetime import time
import unittest
from entities import db, Profesor, Materia, Horario, BloqueHorario, Prioridad, Turno, TurnoHorario, PuedeDictar
from flask import Flask
from sqlalchemy import inspect

class TestEntities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.session.begin_nested()

    def tearDown(self):
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        self.ctx.pop()

    def test_profesor_creation(self):
        profesor = Profesor(cedula="123", nombre="Juan", nombre_completo="Juan Perez", mail="juan@mail.com")
        db.session.add(profesor)
        db.session.commit()
        found = Profesor.query.filter_by(cedula="123").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.nombre, "Juan")

    def test_materia_creation(self):
        materia = Materia(codigo="MAT101", nombre="Matemática", nombre_completo="Matemática Básica", cantidad_dias=2, carga_horaria=4)
        db.session.add(materia)
        db.session.commit()
        found = Materia.query.filter_by(codigo="MAT101").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.nombre, "Matemática")

    def test_horario_creation(self):
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(horario)
        db.session.commit()
        found = Horario.query.filter_by(hora_inicio=time(8, 0)).first()
        self.assertIsNotNone(found)
        self.assertEqual(found.hora_fin, time(10, 0))

    def test_bloque_horario_creation(self):
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(horario)
        db.session.commit()
        bloque = BloqueHorario(dia='lun', hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(bloque)
        db.session.commit()
        found = BloqueHorario.query.filter_by(dia='lun').first()
        self.assertIsNotNone(found)
        self.assertEqual(found.hora_inicio, time(8, 0))

    def test_prioridad_creation(self):
        profesor = Profesor(cedula="123", nombre="Juan", nombre_completo="Juan Perez")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add_all([profesor, horario])
        db.session.commit()
        bloque = BloqueHorario(dia='lun', hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(bloque)
        db.session.commit()
        prioridad = Prioridad(profesor="123", bloque_horario=bloque.id, valor=2)
        db.session.add(prioridad)
        db.session.commit()
        found = Prioridad.query.filter_by(profesor="123").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.valor, 2)

    def test_turno_and_turnohorario_creation(self):
        turno = Turno(nombre="Mañana")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add_all([turno, horario])
        db.session.commit()
        bloque = BloqueHorario(dia='lun', hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(bloque)
        db.session.commit()
        turnohorario = TurnoHorario(id=bloque.id, hora_inicio=time(8, 0), hora_fin=time(10, 0), turno="Mañana")
        db.session.add(turnohorario)
        db.session.commit()
        found = TurnoHorario.query.filter_by(turno="Mañana").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.id, bloque.id)

    def test_puede_dictar_creation(self):
        profesor = Profesor(cedula="123", nombre="Juan", nombre_completo="Juan Perez")
        materia = Materia(codigo="MAT101", nombre="Matemática", nombre_completo="Matemática Básica", cantidad_dias=2, carga_horaria=4)
        turno = Turno(nombre="Mañana")
        db.session.add_all([profesor, materia, turno])
        db.session.commit()
        puede = PuedeDictar(profesor="123", materia="MAT101", turno="Mañana", grupos_max=2)
        db.session.add(puede)
        db.session.commit()
        found = PuedeDictar.query.filter_by(profesor="123", materia="MAT101", turno="Mañana").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.grupos_max, 2)

    def test_model_table_consistency(self):
        inspector = inspect(db.engine)
        # Get all table names from the database
        db_tables = set(inspector.get_table_names())
        # Get all table names from the models
        model_tables = set([table.name for table in db.metadata.sorted_tables])

        # Check that all model tables exist in the database
        self.assertEqual(model_tables, db_tables)

        # For each model table, check columns
        for table in db.metadata.sorted_tables:
            db_columns = {col['name']: col for col in inspector.get_columns(table.name)}
            model_columns = {col.name: col for col in table.columns}
            self.assertEqual(set(model_columns.keys()), set(db_columns.keys()), f"Column mismatch in table {table.name}")

            # Optionally, check column types (basic check)
            for col_name, model_col in model_columns.items():
                db_col_type = type(db_columns[col_name]['type']).__name__
                model_col_type = type(model_col.type).__name__
                self.assertTrue(
                    type_equivalent(model_col_type, db_col_type),
                    f"Type mismatch for column {col_name} in table {table.name}: model={model_col_type}, db={db_col_type}"
                )

def type_equivalent(model_type, db_type):
    # Map SQLAlchemy types to DB types for comparison
    equivalents = {
        'string': ['varchar', 'string', 'text'],
        'varchar': ['varchar', 'string', 'text'],
        'text': ['varchar', 'string', 'text'],
        'integer': ['integer', 'int', 'bigint', 'smallint'],
        'int': ['integer', 'int', 'bigint', 'smallint'],
        'float': ['float', 'real', 'numeric', 'decimal'],
        'numeric': ['float', 'real', 'numeric', 'decimal'],
        'boolean': ['boolean', 'bool'],
        'datetime': ['datetime', 'timestamp'],
        'date': ['date'],
        'time': ['time'],
    }
    model_type = model_type.lower()
    db_type = db_type.lower()
    for key, vals in equivalents.items():
        if model_type in vals and db_type in vals:
            return True
    return model_type == db_type

if __name__ == '__main__':
    unittest.main()