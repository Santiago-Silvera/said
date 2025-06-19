"""End-to-end tests for the Flask application routes."""

import unittest
from datetime import time

from said import app
from entities import db, Profesor, Materia, Horario, BloqueHorario, Turno, TurnoHorario, PuedeDictar, Prioridad


def encode_hash(value: str, offset: int = 7) -> str:
    """Generate the encoded hash used by the legacy client."""
    return "".join(f"{ord(c)+offset:02X}" for c in value)


class TestAppEndpoints(unittest.TestCase):
    """Run the HTTP endpoints against a temporary database."""

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        cls.ctx = app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.ctx.pop()

    def setUp(self):
        db.create_all()
        self.client = app.test_client()
        # Insert minimal data
        prof = Profesor(cedula="1", nombre="juan", nombre_completo="Juan Perez")
        turno = Turno(nombre="Mañana")
        horario = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        bloque = BloqueHorario(id=1, dia="lun", hora_inicio=time(8, 0), hora_fin=time(10, 0))
        turno_horario = TurnoHorario(hora_inicio=time(8, 0), hora_fin=time(10, 0), turno="Mañana")
        materia = Materia(nombre="MAT101", nombre_completo="Matemática")
        puede = PuedeDictar(profesor="juan", materia="MAT101", turno="Mañana")
        db.session.add_all([prof, turno, horario, bloque, turno_horario, materia, puede])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_unauthenticated(self):
        """Visiting preferences without login should return an error page."""
        res = self.client.get("/preferences")
        self.assertEqual(res.status_code, 401)
        self.assertIn(b"Usted no se encuentra registrado", res.data)

    def test_index_authenticated(self):
        """Logged users should see the preferences page."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "1"
        res = self.client.get("/preferences")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Juan Perez", res.data)

    def test_entry_missing_hash(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 401)

    def test_entry_valid_hash(self):
        hash_value = encode_hash("1")
        res = self.client.get(f"/?hash={hash_value}")
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.headers["Location"].endswith("/preferences"))

    def test_submit_valid_preferences(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = "1"
        res = self.client.post("/submit", json={"preferences": {"1": 2}})
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Preferencias guardadas", res.data)
        pref = Prioridad.query.filter_by(profesor="juan", bloque_horario=1).first()
        self.assertIsNotNone(pref)

    def test_submit_missing_preferences(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = "1"
        res = self.client.post("/submit", json={})
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"Debes proporcionar preferencias", res.data)


if __name__ == "__main__":
    unittest.main()
