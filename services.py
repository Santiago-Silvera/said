from entities import db, Preferencia, BloqueHorario, Profesor
import json

def guardar_respuesta(preferences_data, ci):
    """
    Guarda las preferencias horarias de un profesor en la base de datos.

    :param preferences_data: Lista de preferencias horarias.
    :param ci: Cédula del profesor.
    """
    profesor = Profesor.query.filter_by(cedula=ci).first()
    if not profesor:
        raise ValueError(f"No se encontró un profesor con la cédula {ci}")

    for preference in preferences_data:
        bloque_horario_id = preference.get('bloque_horario_id')
        valor_prioridad = preference.get('valor_prioridad')

        # Verificar si el bloque horario existe
        bloque_horario = BloqueHorario.query.get(bloque_horario_id)
        if not bloque_horario:
            raise ValueError(f"No se encontró un bloque horario con ID {bloque_horario_id}")

        # Crear una nueva preferencia
        nueva_preferencia = Preferencia(
            valor_prioridad=valor_prioridad,
            profesor_cedula=ci,
            bloque_horario_id=bloque_horario_id
        )
        db.session.add(nueva_preferencia)

    # Guardar los cambios en la base de datos
    db.session.commit()


def get_time_info():
    """
    Obtiene información de los horarios y días disponibles.

    :return: Una tupla con dos listas: horarios y días de la semana.
    """
    horarios = db.session.query(BloqueHorario.dia).distinct().all()
    horarios = [h[0] for h in horarios]  # Extraer los valores de los resultados

    dias = db.session.query(BloqueHorario.horario_id).distinct().all()
    dias = [d[0] for d in dias]  # Extraer los valores de los resultados

    return horarios, dias


def verificar_profesor(ci):
    """
    Verifica si un profesor existe en la base de datos.

    :param ci: Cédula del profesor.
    :return: True si el profesor existe, False en caso contrario.
    """
    profesor = Profesor.query.filter_by(cedula=ci).first()
    return profesor is not None