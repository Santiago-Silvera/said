import unittest
from unittest.mock import patch, MagicMock
from src.services import guardar_respuesta, get_time_info, verificar_profesor
from src.entities import Profesor, BloqueHorario, Preferencia
from app import app  # Import the Flask app

class TestServices(unittest.TestCase):
    @patch('services.Profesor.query.filter_by')
    @patch('services.BloqueHorario.query.get')
    @patch('services.db.session')
    def test_guardar_respuesta(self, mock_db_session, mock_bloque_horario_query, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = MagicMock(cedula=123)
        mock_bloque_horario_query.return_value = MagicMock(id=1)

        preferences_data = [{"bloque_horario_id": 1, "valor_prioridad": 5}]
        guardar_respuesta(preferences_data, 123)

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('services.db.session.query')
    def test_get_time_info(self, mock_query):
        mock_query.return_value.distinct.return_value.all.side_effect = [
            [("Monday",), ("Tuesday",)],
            [(1,), (2,)]
        ]
        with app.app_context():  # Wrap the call in app context
            time_slots, days_of_week = get_time_info()
        self.assertEqual(time_slots, ["Monday", "Tuesday"])
        self.assertEqual(days_of_week, [1, 2])

    @patch('services.Profesor.query.filter_by')
    def test_verificar_profesor_exists(self, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = MagicMock(cedula=123)
        result = verificar_profesor(123)
        self.assertTrue(result)

    @patch('services.Profesor.query.filter_by')
    def test_verificar_profesor_not_exists(self, mock_profesor_query):
        mock_profesor_query.return_value.first.return_value = None
        result = verificar_profesor(123)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()