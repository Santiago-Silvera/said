from datetime import time
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from services import (
    guardar_respuesta,
    obtener_bloques_horarios,
    verificar_profesor,
    listar_materias,
    listar_turnos,
    get_professor_data,
    get_previous_preferences,
    listar_turnos_materias_profesor
)
from app import app  # Import the Flask app

class TestServices(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('services.db.session')
    @patch('services.Prioridad')
    @patch('services.BloqueHorario')
    @patch('services.Profesor')
    def test_guardar_respuesta(self, 
                               mock_profesor_class: MagicMock, 
                               mock_bloque_class: MagicMock, 
                               mock_prioridad_class: MagicMock, 
                               mock_db_session: MagicMock):
        # Mock Profesor.query.filter_by().first()
        mock_profesor = MagicMock(cedula=123)
        mock_profesor_class.query = MagicMock()
        mock_profesor_class.query.filter_by.return_value.first.return_value = mock_profesor

        # Mock Prioridad.query.filter_by().delete() and .first()
        mock_prioridad_query = MagicMock()
        mock_prioridad_query.filter_by.return_value.delete.return_value = None
        mock_prioridad_query.filter_by.return_value.first.return_value = None  # Simula que no existe aún
        mock_prioridad_class.query = mock_prioridad_query

        # Mock BloqueHorario.query.get()
        mock_bloque_query = MagicMock()
        mock_bloque_query.get.side_effect = lambda x: MagicMock(id=x)
        mock_bloque_class.query = mock_bloque_query

        # Mock sesión
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        preferences_data = {1: 2, 2: 3}
        guardar_respuesta(preferences_data, 123)

        # Comprobaciones
        self.assertEqual(mock_db_session.add.call_count, 2)
        mock_db_session.commit.assert_called_once()
        # Verifica que se haya actualizado ultima_modificacion
        self.assertIsNotNone(mock_profesor.ultima_modificacion)

    @patch('services.BloqueHorario')
    def test_obtener_bloques_horarios(self, mock_bloque_horario: MagicMock):
        mock_query = MagicMock()
        
        mock_query.all.return_value = [
            MagicMock(id=1, dia="Monday", hora_inicio=time(8, 0), hora_fin=time(9, 0)),
            MagicMock(id=2, dia="Monday", hora_inicio=time(9, 0), hora_fin=time(10, 0)),
        ]
        mock_bloque_horario.query = mock_query

        with app.app_context():
            result = obtener_bloques_horarios()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['dia'], "Monday")

    @patch('services.Profesor')
    def test_verificar_profesor_exists(self, mock_profesor_class: MagicMock):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.first.return_value = MagicMock(cedula=123)

        mock_query.filter_by.return_value = mock_filter
        mock_profesor_class.query = mock_query

        result = verificar_profesor(123)
        self.assertTrue(result)

    @patch('services.Profesor')
    def test_verificar_profesor_not_exists(self, mock_profesor_class: MagicMock):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.first.return_value = None

        mock_query.filter_by.return_value = mock_filter
        mock_profesor_class.query = mock_query

        result = verificar_profesor(123)
        self.assertFalse(result)

    @patch('services.Materia')
    def test_listar_materias(self, mock_materias: MagicMock):
        mock_query = MagicMock()
        mock_query.all.return_value = [
            MagicMock(codigo="MAT101", nombre="Mathematics", carga_horaria=4),
            MagicMock(codigo="PHY101", nombre="Physics", carga_horaria=3)
        ]
        mock_materias.query = mock_query
        result = listar_materias()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['codigo'], "MAT101")

    @patch('services.Turno')
    def test_listar_turnos(self, mock_turno: MagicMock):
        mock_query = MagicMock()
        mock_query.all.return_value = [
            MagicMock(nombre="Morning"),
            MagicMock(nombre="Evening")
        ]
        mock_turno.query = mock_query
        result = listar_turnos()
        self.assertEqual(len(result), 2)
        self.assertIn("Morning", result)

    @patch('services.Profesor')
    def test_get_professor_data(self, mock_profesor_class: MagicMock):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.first.return_value = MagicMock(nombre="Juan Perez")
        
        mock_query.filter_by.return_value = mock_filter
        mock_profesor_class.query = mock_query

        result = get_professor_data(123)
        self.assertEqual(result, {"nombre": "Juan Perez"})

    @patch('services.Profesor')
    def test_get_professor_data_not_found(self, mock_profesor_class: MagicMock):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        
        mock_query.filter_by.return_value = mock_filter
        mock_profesor_class.query = mock_query
        with self.assertRaises(ValueError):
            get_professor_data(123)

    @patch('services.Prioridad')
    def test_get_previous_preferences(self, mock_prioridad_class: MagicMock):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_query.filter_by.return_value.all.return_value = [
            MagicMock(bloque_horario=1, valor=2),
            MagicMock(bloque_horario=2, valor=3)
        ]
        mock_prioridad_class.query = mock_query
        result = get_previous_preferences(123)
        self.assertEqual(result, {1: 2, 2: 3})

    @patch('services.Turno')
    @patch('services.Materia')
    @patch('services.PuedeDictar')
    @patch('services.Profesor')
    def test_listar_turnos_materias_profesor(
        self,
        mock_profesor_class,
        mock_puede_dictar_class,
        mock_materia_class,
        mock_turno_class
    ):
        # Mock Profesor.query.filter_by().first()
        mock_profesor_query = MagicMock()
        mock_profesor_query.filter_by.return_value.first.return_value = MagicMock(cedula="123", nombre="Juan Perez")
        mock_profesor_class.query = mock_profesor_query

        # Mock PuedeDictar.query.filter_by().all()
        mock_pd1 = MagicMock(materia="MAT101", turno="Morning")
        mock_pd2 = MagicMock(materia="PHY101", turno="Evening")
        mock_puede_dictar_query = MagicMock()
        mock_puede_dictar_query.filter_by.return_value.all.return_value = [mock_pd1, mock_pd2]
        mock_puede_dictar_class.query = mock_puede_dictar_query

        # Mock Materia.query.filter_by().first()
        def mock_materia_filter_by(codigo):
            mock_materia = MagicMock()
            if codigo == "MAT101":
                mock_materia.codigo = "MAT101"
                mock_materia.nombre = "Mathematics"
                mock_materia.carga_horaria = 4
            else:
                mock_materia.codigo = "PHY101"
                mock_materia.nombre = "Physics"
                mock_materia.carga_horaria = 3
            return MagicMock(first=MagicMock(return_value=mock_materia))
        mock_materia_class.query.filter_by.side_effect = mock_materia_filter_by

        # Mock Turno.query.filter_by().first()
        def mock_turno_filter_by(nombre):
            mock_turno = MagicMock()
            mock_turno.nombre = nombre
            return MagicMock(first=MagicMock(return_value=mock_turno))
        mock_turno_class.query.filter_by.side_effect = mock_turno_filter_by

        # Ejecutar
        result = listar_turnos_materias_profesor("123")

        # Validaciones
        self.assertEqual(len(result["materias"]), 2)
        self.assertEqual(result["materias"][0]["codigo"], "MAT101")
        self.assertIn("Morning", result["turnos"])
        self.assertIn("Evening", result["turnos"])

if __name__ == '__main__':
    unittest.main()