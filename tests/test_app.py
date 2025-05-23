import unittest
from unittest.mock import patch

from said import app


class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('said.verificar_profesor')
    @patch('said.render_template')
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

    @patch('said.listar_turnos_materias_profesor')
    @patch('said.get_professor_data')
    @patch('said.obtener_bloques_horarios')
    @patch('said.get_previous_preferences')
    @patch('said.verificar_profesor')
    @patch('said.render_template')
    def test_index_authenticated(
        self, mock_render_template, mock_verificar_profesor,
        mock_get_previous_preferences, mock_obtener_bloques_horarios,
        mock_get_professor_data, mock_listar_turnos_materias_profesor
    ):
        mock_verificar_profesor.return_value = True
        mock_get_professor_data.return_value = {'nombre': 'Juan'}
        mock_listar_turnos_materias_profesor.return_value = {
            "materias": [
                {"codigo": "MAT101", "nombre": "Matemática", "carga_horaria": 4}
            ],
            "turnos": ["Mañana"]
        }
        # Simulate bloques_horarios for all and for turno
        all_bloques = [
            {'id': 1, 'dia': 'Monday', 'hora_inicio': '08:00', 'hora_fin': '10:00'},
            {'id': 2, 'dia': 'Tuesday', 'hora_inicio': '10:00', 'hora_fin': '12:00'}
        ]
        turno_bloques = [
            {'id': 1, 'dia': 'Monday', 'hora_inicio': '08:00', 'hora_fin': '10:00'}
        ]
        def obtener_bloques_horarios_side_effect(turno=None):
            if turno is None:
                return all_bloques
            if turno == "Mañana":
                return turno_bloques
            return []
        mock_obtener_bloques_horarios.side_effect = obtener_bloques_horarios_side_effect
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
        self.assertIn('bloques_turno', kwargs)
        self.assertEqual(kwargs['ci'], 123)
        self.assertEqual(kwargs['professor_name'], 'Juan')
        self.assertIn(1, kwargs['bloques_turno'])
        self.assertNotIn(2, kwargs['bloques_turno'])

    def test_entry_missing_hash(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Error de autenticaci", response.data)

    @patch('said.decode_hash')
    def test_entry_valid_hash(self, mock_decode_hash):
        mock_decode_hash.return_value = 123
        response = self.app.get('/?hash=abc')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/preferences'))

    @patch('said.guardar_respuesta')
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
