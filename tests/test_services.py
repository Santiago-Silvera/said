import unittest
from unittest.mock import patch, MagicMock
from services import save_response, get_time_info, verify_professor, listar_materias, listar_turnos
# from entities import Profesor, BloqueHorario, Preferencia, Materia, Turno
from app import app  # Import the Flask app

class TestServices(unittest.TestCase):
    @patch('services.Profesor.query.filter_by')
    @patch('services.BloqueHorario.query.get')
    @patch('services.db.session')
    def test_guardar_respuesta(self, mock_db_session, mock_bloque_horario_query, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = MagicMock(cedula=123)
        mock_bloque_horario_query.return_value = MagicMock(id=1)

        preferences_data = [{"bloque_horario_id": 1, "valor_prioridad": 2}]
        save_response(preferences_data, 123)

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('services.BloqueHorario.query.all')
    def test_get_time_info(self, mock_query):
        mock_query.return_value = [
            MagicMock(id=1, dia="Monday", hora_inicio="08:00", hora_fin="10:00"),
            MagicMock(id=2, dia="Tuesday", hora_inicio="10:00", hora_fin="12:00")
        ]
        with app.app_context():
            result = get_time_info()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['dia'], "Monday")

    @patch('services.Profesor.query.filter_by')
    def test_verificar_profesor_exists(self, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = MagicMock(cedula=123)
        result = verify_professor(123)
        self.assertTrue(result)

    @patch('services.Profesor.query.filter_by')
    def test_verificar_profesor_not_exists(self, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = None
        result = verify_professor(123)
        self.assertFalse(result)

    @patch('services.Materia.query.all')
    def test_listar_materias(self, mock_query):
        mock_query.return_value = [
            MagicMock(codigo="MAT101", nombre="Mathematics", carga_horaria=4),
            MagicMock(codigo="PHY101", nombre="Physics", carga_horaria=3)
        ]
        result = listar_materias()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['codigo'], "MAT101")

    @patch('services.Turno.query.all')
    def test_listar_turnos(self, mock_query):
        mock_query.return_value = [
            MagicMock(nombre="Morning"),
            MagicMock(nombre="Evening")
        ]
        result = listar_turnos()
        self.assertEqual(len(result), 2)
        self.assertIn("Morning", result)

if __name__ == '__main__':
    unittest.main()