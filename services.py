from typing import Any, List
from entities import TurnoHorario, db, Prioridad, BloqueHorario, Profesor, Materia, Turno, PuedeDictar


def decode_hash(encoded: int) -> int:
    offset = 7  # Debe ser el mismo que en ASP
    original = ""

    for i in range(0, len(encoded), 2):
        hex_pair = encoded[i:i+2]
        val = int(hex_pair, 16) - offset
        original += chr(val)

    return original


def guardar_respuesta(preferences, ci):
    """
    Guarda las preferencias horarias de un profesor en la base de datos.

    :param preferences: Diccionario con índices de bloques horarios como claves y prioridades como valores.
    :param ci: Cédula del profesor.
    """
    profesor: Profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    if not profesor:
        raise ValueError(f"No se encontró un profesor con la cédula {ci}")

    profesor.ultima_modificacion = db.func.now()

    # Eliminar preferencias previas
    Prioridad.query.filter_by(profesor=str(ci)).delete()

    print("services.py: Preferences to save:", preferences)
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

def obtener_bloques_horarios(turno=None):
    """
    Obtiene información de los horarios y días disponibles según el turno ingresado.

    :param turno: Nombre del turno (opcional).
    :return: Una lista de diccionarios con bloques horarios y días de la semana.
    """
    if turno is None:
        # Obtener todos los bloques horarios
        bloques_horarios = BloqueHorario.query.all()
    else:
        # Unir TurnoHorario con BloqueHorario usando el id de bloque
        bloques_horarios = (
            db.session.query(BloqueHorario)
            .join(TurnoHorario, BloqueHorario.id == TurnoHorario.id)
            .filter(TurnoHorario.turno == turno)
            .all()
        )

    return [
        {
            "id": bloque.id,
            "dia": bloque.dia,
            "hora_inicio": bloque.hora_inicio.strftime("%H:%M"),
            "hora_fin": bloque.hora_fin.strftime("%H:%M")
        }
        for bloque in bloques_horarios
    ]


def verificar_profesor(ci: int) -> bool:
    """
    Verifica si un profesor existe en la base de datos.

    :param ci: Cédula del profesor.
    :return: True si el profesor existe, False en caso contrario.
    """
    profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    return profesor is not None

def listar_materias():
    """
    Lista todas las materias disponibles.

    :return: Una lista de materias.
    """
    materias: List[Any] = Materia.query.all()
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
    profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    if not profesor:
        return {}
    preferencias = Prioridad.query.filter_by(profesor=profesor.nombre).all()
    return {p.bloque_horario: p.valor for p in preferencias}


def listar_turnos_materias_profesor(ci):
    """
    Lista todas las materias asociadas a un profesor dado su cédula y los turnos asociados a esas materias.

    :param ci: Cédula del profesor.
    :return: Un diccionario con dos listas: 'materias' y 'turnos'.
    """
    profesor: Profesor = Profesor.query.filter_by(cedula=str(ci)).first()
    if not profesor:
        raise ValueError(f"No se encontró un profesor con la cédula {ci}")

    # Buscar todas las filas de PuedeDictar para este profesor
    puede_dictar = PuedeDictar.query.filter_by(profesor=profesor.nombre).all()
    lista_materias = []
    lista_turnos = set()
    codigos_materias = set()

    for pd in puede_dictar:
        materia = Materia.query.filter_by(codigo=pd.materia).first()
        turno = Turno.query.filter_by(nombre=pd.turno).first()
        if materia and materia.codigo not in codigos_materias:
            lista_materias.append({
                "codigo": materia.codigo,
                "nombre": materia.nombre,
                "carga_horaria": materia.carga_horaria
            })
            codigos_materias.add(materia.codigo)
        if turno:
            lista_turnos.add(turno.nombre)

    return {
        "materias": lista_materias,
        "turnos": list(lista_turnos)
    }
