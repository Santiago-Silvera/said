"""Unit tests for the SQLAlchemy models defined in :mod:`entities`.

These tests use an in-memory SQLite database to verify that the models
behave as expected when performing common operations such as creation and
relationship checks.
"""

from datetime import time
import unittest
from entities import (
    db,
    Profesor,
    Materia,
    Horario,
    BloqueHorario,
    Prioridad,
    Turno,
    TurnoHorario,
    PuedeDictar,
)
from flask import Flask
from sqlalchemy import inspect

class TestEntities(unittest.TestCase):
    """Validate that ORM models map correctly to the database schema."""
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
        """A :class:`Profesor` should be persisted with all basic fields."""
        profesor = Profesor(cedula="123", nombre="juan", nombre_completo="Juan Perez", mail="juan@mail.com")
        db.session.add(profesor)
        db.session.commit()
        found = Profesor.query.filter_by(cedula="123").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.nombre, "juan")

    def test_materia_creation(self):
        """Ensure :class:`Materia` instances can be persisted."""
        materia = Materia(nombre="MAT101", nombre_completo="Matemática Básica")
        db.session.add(materia)
        db.session.commit()
        found = Materia.query.filter_by(nombre="MAT101").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.nombre_completo, "Matemática Básica")

    def test_horario_creation(self):
        """`Horario` stores a pair of start and end times."""
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(horario)
        db.session.commit()
        found = Horario.query.filter_by(hora_inicio=time(8, 0)).first()
        self.assertIsNotNone(found)
        self.assertEqual(found.hora_fin, time(10, 0))

    def test_bloque_horario_creation(self):
        """Blocks combine a day with a :class:`Horario`."""
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
        """`Prioridad` should store a professor's preference for a block."""
        profesor = Profesor(cedula="123", nombre="juan", nombre_completo="Juan Perez")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add_all([profesor, horario])
        db.session.commit()
        bloque = BloqueHorario(dia='lun', hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(bloque)
        db.session.commit()
        prioridad = Prioridad(profesor="juan", bloque_horario=bloque.id, valor=2)
        db.session.add(prioridad)
        db.session.commit()
        found = Prioridad.query.filter_by(profesor="juan").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.valor, 2)

    def test_turno_and_turnohorario_creation(self):
        """`TurnoHorario` should correctly link a schedule with a shift."""
        turno = Turno(nombre="Mañana")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add_all([turno, horario])
        db.session.commit()
        bloque = BloqueHorario(dia='lun', hora_inicio=time(8, 0), hora_fin=time(10, 0))
        db.session.add(bloque)
        db.session.commit()
        turnohorario = TurnoHorario(hora_inicio=time(8, 0), hora_fin=time(10, 0), turno="Mañana")
        db.session.add(turnohorario)
        db.session.commit()
        found = TurnoHorario.query.filter_by(turno="Mañana").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.turno, "Mañana")

    def test_puede_dictar_creation(self):
        """`PuedeDictar` establishes which subject a professor can teach."""
        profesor = Profesor(cedula="123", nombre="juan", nombre_completo="Juan Perez")
        materia = Materia(nombre="MAT101", nombre_completo="Matemática Básica")
        turno = Turno(nombre="Mañana")
        db.session.add_all([profesor, materia, turno])
        db.session.commit()
        puede = PuedeDictar(profesor="juan", materia="MAT101", turno="Mañana", grupos_max=2)
        db.session.add(puede)
        db.session.commit()
        found = PuedeDictar.query.filter_by(profesor="juan", materia="MAT101", turno="Mañana").first()
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
