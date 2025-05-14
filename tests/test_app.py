import unittest
from unittest.mock import patch, MagicMock
from app import app, db

class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.session')
    def test_index_redirects_to_login_when_not_authenticated(self, mock_session):
        mock_session.get.return_value = None
        response = self.app.get('/preferences')
        self.assertEqual(response.status_code, 302)
        self.assertIn("https://www3.um.edu.uy/profesores/default.asp", response.location)

    @patch('app.session')
    @patch('app.render_template')
    def test_index_renders_template_when_authenticated(self, mock_render_template, mock_session):
        mock_session.get.return_value = 1  # Simulate authenticated user
        mock_render_template.return_value = "Rendered Template"
        response = self.app.get('/preferences')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_once_with(
            'index.html', time_slots=app.time_slots, days_of_week=app.days_of_week, ci=None
        )

    def test_handle_auth_missing_token(self):
        response = self.app.get('/auth')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Token missing"})

    @patch('app.jwt.decode')
    @patch('app.session')
    def test_handle_auth_valid_token(self, mock_session, mock_jwt_decode):
        mock_jwt_decode.return_value = {"user_id": 1}
        response = self.app.get('/auth?token=valid_token')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/preferences')
        mock_session.__setitem__.assert_called_once_with('user_id', 1)

    @patch('app.jwt.decode', side_effect=Exception("Invalid token"))
    def test_handle_auth_invalid_token(self, mock_jwt_decode):
        response = self.app.get('/auth?token=invalid_token')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"error": "Invalid token"})

    @patch('app.json.loads')
    @patch('app.guardar_respuesta')
    def test_submit_valid_preferences(self, mock_guardar_respuesta, mock_json_loads):
        mock_json_loads.return_value = [{"bloque_horario_id": 1, "valor_prioridad": 5}]
        response = self.app.post('/submit', data={"preferences": '[{"bloque_horario_id": 1, "valor_prioridad": 5}]'})
        self.assertEqual(response.status_code, 200)
        mock_guardar_respuesta.assert_called_once()

    def test_submit_missing_preferences(self):
        response = self.app.post('/submit', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Ha ocurrido un error", response.data.decode())

if __name__ == '__main__':
    unittest.main()