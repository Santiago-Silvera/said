import unittest
from unittest.mock import patch, MagicMock

import jwt
from app import app

class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # self.app.testing = True

    @patch('app.verificar_profesor')
    @patch('app.render_template')
    def test_index_unauthenticated(self, mock_render_template, mock_verificar_profesor):
        mock_verificar_profesor.return_value = False
        mock_render_template.return_value = "Error page"
        with self.app.session_transaction() as sess:
            sess['user_id'] = None
        response = self.app.get('/preferences')
        self.assertEqual(response.status_code, 401)
        mock_render_template.assert_called_once_with(
            'error.html', message="Usuario no autenticado. Por favor, inicie sesión."
        )

    @patch('app.verificar_profesor')
    @patch('app.get_professor_data')
    @patch('app.obtener_bloques_horarios')
    @patch('app.get_previous_preferences')
    @patch('app.render_template')
    def test_index_authenticated(
        self, mock_render_template, mock_get_previous_preferences,
        mock_obtener_bloques_horarios, mock_get_professor_data, mock_verificar_profesor
    ):
        mock_verificar_profesor.return_value = True
        mock_get_professor_data.return_value = {'nombre': 'Juan'}
        mock_obtener_bloques_horarios.return_value = [
            {'id': 1, 'dia': 'Monday', 'hora_inicio': '08:00', 'hora_fin': '10:00'}
        ]
        mock_get_previous_preferences.return_value = {1: 2}
        mock_render_template.return_value = "Rendered Template"
        with self.app.session_transaction() as sess:
            sess['user_id'] = 123
        response = self.app.get('/preferences')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_once()
        args, kwargs = mock_render_template.call_args
        self.assertEqual(args[0], 'index.html')
        self.assertIn('bloques_horarios', kwargs)
        self.assertEqual(kwargs['ci'], 123)
        self.assertEqual(kwargs['professor_name'], 'Juan')

    def test_handle_auth_missing_token(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Token faltante", response.data)

    @patch('app.jwt.decode')
    @patch('app.render_template')
    def test_handle_auth_valid_token(self, mock_render_template, mock_jwt_decode):
        mock_jwt_decode.return_value = {"user_id": 1}
        response = self.app.get('/?token=valid_token')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/preferences')

    @patch('app.jwt.decode', side_effect=Exception("Invalid token"))
    @patch('app.render_template')
    def test_handle_auth_invalid_token(self, mock_render_template, mock_jwt_decode):
        mock_render_template.return_value = "Error page"
        response = self.app.get('/?token=invalid_token')
        self.assertEqual(response.status_code, 500)
        mock_render_template.assert_called()

    @patch('app.jwt.decode', side_effect=jwt.ExpiredSignatureError())
    @patch('app.render_template')
    def test_handle_auth_expired_token(self, mock_render_template, mock_jwt_decode):
        mock_render_template.return_value = "Error page"
        response = self.app.get('/?token=expired_token')
        self.assertEqual(response.status_code, 401)
        mock_render_template.assert_called()

    @patch('app.guardar_respuesta')
    def test_submit_valid_preferences(self, mock_guardar_respuesta):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 123
        data = {
            "preferences": [{"bloque_horario_id": 1, "valor_prioridad": 5}]
        }
        response = self.app.post('/submit', json=data)
        self.assertEqual(response.status_code, 200)
        mock_guardar_respuesta.assert_called_once()

    def test_submit_missing_preferences(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 123
        response = self.app.post('/submit', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Debes proporcionar preferencias.", response.data)

if __name__ == '__main__':
    unittest.main()