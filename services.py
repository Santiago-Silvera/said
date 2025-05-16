from entities import db, Prioridad, BloqueHorario, Profesor, Materia, Turno, PuedeDictar

def save_response(preferences, ci):
    """
    Guarda las preferencias horarias de un profesor en la base de datos.

    :param preferences: Diccionario con índices de bloques horarios como claves y prioridades como valores.
    :param ci: Cédula del profesor.
    """
    profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    if not profesor:
        raise ValueError(f"No se encontró un profesor con la cédula {ci}")

    # Eliminar preferencias previas
    Prioridad.query.filter_by(profesor=str(ci)).delete()

    print("Preferences to save:", preferences)
    for bloque_horario_id, valor_prioridad in preferences.items():
        # Verificar si el bloque horario existe
        bloque_horario = BloqueHorario.query.get(bloque_horario_id)
        if not bloque_horario:
            raise ValueError(f"No se encontró un bloque horario con ID {bloque_horario_id}")
        valor_prioridad = valor_prioridad if valor_prioridad else 0

        # Crear o actualizar una prioridad
        prioridad = Prioridad.query.filter_by(profesor=str(ci), bloque_horario=bloque_horario_id).first()
        if prioridad:
            prioridad.valor = valor_prioridad
        else:
            nueva_prioridad = Prioridad(
                profesor=ci,
                bloque_horario=bloque_horario_id,
                valor=valor_prioridad
            )
            db.session.add(nueva_prioridad)

    # Guardar los cambios en la base de datos
    db.session.commit()

def get_time_blocks():
    """
    Obtiene información de los horarios y días disponibles.

    :return: Un diccionario con bloques horarios y días de la semana.
    """
    bloques_horarios = BloqueHorario.query.all()
    return [
        {
            "id": bloque.id,
            "dia": bloque.dia,
            "hora_inicio": bloque.hora_inicio.strftime("%H:%M"),
            "hora_fin": bloque.hora_fin.strftime("%H:%M")
        }
        for bloque in bloques_horarios
    ]

def verify_professor(ci):
    """
    Verifica si un profesor existe en la base de datos.

    :param ci: Cédula del profesor.
    :return: True si el profesor existe, False en caso contrario.
    """
    return Profesor.query.filter_by(cedula=str(ci)).first() is not None

def listar_materias():
    """
    Lista todas las materias disponibles.

    :return: Una lista de materias.
    """
    materias = Materia.query.all()
    return [
        {
            "codigo": materia.codigo,
            "nombre": materia.nombre,
            "carga_horaria": materia.carga_horaria
        }
        for materia in materias
    ]

def listar_turnos():
    """
    Lista todos los turnos disponibles.

    :return: Una lista de turnos.
    """
    turnos = Turno.query.all()
    return [turno.nombre for turno in turnos]


def get_professor_data(ci: int):
    """
    Obtiene los datos de un profesor a partir de su cédula.

    :param ci: Cédula del profesor.
    :return: Un diccionario con los datos del profesor.
    """
    profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    if not profesor:
        raise ValueError(f"No se encontró un profesor con la cédula {ci}")
    
    return {
        "nombre": profesor.nombre,
    }

def get_previous_preferences(ci):
    """
    Devuelve un diccionario {bloque_horario_id: valor} con las preferencias previas del profesor.
    """
    preferencias = Prioridad.query.filter_by(profesor=str(ci)).all()
    return {p.bloque_horario: p.valor for p in preferencias}