"""Integration tests for service layer functions."""

from datetime import time
import unittest

from said import app
from entities import (
    db,
    Persona,
    Profesor,
    Materia,
    Horario,
    BloqueHorario,
    Prioridad,
    Turno,
    TurnoHorario,
    PuedeDictar,
)
from services import (
    guardar_respuesta,
    obtener_bloques_horarios,
    verificar_profesor,
    listar_materias,
    listar_turnos,
    get_professor_data,
    get_previous_preferences,
    listar_turnos_materias_profesor,
)


class TestServices(unittest.TestCase):
    """Exercise service helpers using a temporary SQLite database."""

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_basic_data(self):
        """Insert a professor, a schedule block and related records."""
        persona = Persona(cedula="1", nombre="juan")
        profesor = Profesor(cedula="1", nombre="juan", nombre_completo="Juan Perez")
        turno = Turno(nombre="Mañana")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        bloque = BloqueHorario(id=1, dia="lun", hora_inicio=time(8, 0), hora_fin=time(10, 0))
        turno_horario = TurnoHorario(hora_inicio=time(8, 0), hora_fin=time(10, 0), turno="Mañana")
        materia = Materia(nombre="MAT101", nombre_completo="Matemática")
        puede = PuedeDictar(profesor="juan", materia="MAT101", turno="Mañana")
        db.session.add_all([
            persona,
            profesor,
            turno,
            horario,
            bloque,
            turno_horario,
            materia,
            puede,
        ])
        db.session.commit()

    def test_guardar_respuesta(self):
        """Preferences should be stored as `Prioridad` rows."""
        self._create_basic_data()
        guardar_respuesta({1: 2}, "1")
        pref = Prioridad.query.filter_by(profesor="juan", bloque_horario=1).first()
        self.assertIsNotNone(pref)
        self.assertEqual(pref.valor, 2)

    def test_obtener_bloques_horarios(self):
        """Retrieve blocks with and without filtering by turn."""
        self._create_basic_data()
        all_blocks = obtener_bloques_horarios()
        morning = obtener_bloques_horarios("Mañana")
        self.assertEqual(len(all_blocks), 1)
        self.assertEqual(len(morning), 1)
        self.assertEqual(all_blocks[0]["id"], 1)

    def test_verificar_profesor(self):
        """Check existence of a professor by id."""
        self._create_basic_data()
        self.assertTrue(verificar_profesor("1"))
        self.assertFalse(verificar_profesor("2"))

    def test_listar_materias_y_turnos(self):
        """List available subjects and shifts."""
        self._create_basic_data()
        materias = listar_materias()
        turnos = listar_turnos()
        self.assertEqual(len(materias), 1)
        self.assertEqual(materias[0]["nombre"], "MAT101")
        self.assertIn("Mañana", turnos)

    def test_get_professor_data(self):
        """Fetch a professor record as a dictionary."""
        self._create_basic_data()
        data = get_professor_data("1")
        self.assertEqual(data["nombre"], "juan")
        self.assertEqual(data["nombre_completo"], "Juan Perez")

    def test_get_previous_preferences(self):
        """Retrieve previously saved preferences."""
        self._create_basic_data()
        Prioridad(profesor="juan", bloque_horario=1, valor=3)
        db.session.add(Prioridad(profesor="juan", bloque_horario=1, valor=3))
        db.session.commit()
        prefs = get_previous_preferences("1")
        self.assertEqual(prefs, {1: 3})

    def test_listar_turnos_materias_profesor(self):
        """Return the subjects and shifts linked to a professor."""
        self._create_basic_data()
        res = listar_turnos_materias_profesor("1")
        self.assertEqual(len(res["materias"]), 1)
        self.assertEqual(res["materias"][0]["nombre"], "MAT101")
        self.assertEqual(res["turnos"], ["Mañana"])


if __name__ == "__main__":
    unittest.main()
