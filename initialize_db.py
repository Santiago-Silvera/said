from typing import List
from datetime import time

def initialize_database():
    from said import app
    from entities import db, Profesor, Materia, Horario, BloqueHorario, Prioridad, Turno, TurnoHorario, PuedeDictar

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Profesores
        prof1 = Profesor(cedula="1001", nombre="Juan", nombre_completo="Juan Pérez", mail="juan@mail.com")
        prof2 = Profesor(cedula="1002", nombre="Ana", nombre_completo="Ana Gómez", mail="ana@mail.com")
        db.session.add_all([prof1, prof2])

        # Materias
        mat1 = Materia(codigo="MAT101", nombre="Matemática", nombre_completo="Matemática Básica", cantidad_dias=2, carga_horaria=4)
        mat2 = Materia(codigo="FIS101", nombre="Física", nombre_completo="Física General", cantidad_dias=3, carga_horaria=5)
        db.session.add_all([mat1, mat2])

        # Horarios
        hor1 = Horario(hora_inicio=time(8, 0), hora_fin=time(10, 0))
        hor2 = Horario(hora_inicio=time(10, 0), hora_fin=time(12, 0))
        db.session.add_all([hor1, hor2])

        # Turnos
        turno1 = Turno(nombre="Mañana")
        turno2 = Turno(nombre="Tarde")
        db.session.add_all([turno1, turno2])

        # Bloques Horarios
        idx: int = 0
        for dia in ['lun', 'mar', 'mie', 'jue', 'vie']:
            for t, h in zip([turno1, turno2], [hor1, hor2]):
                bloque = BloqueHorario(id=idx, dia=dia, hora_inicio=h.hora_inicio, hora_fin=h.hora_fin)
                turno_horario = TurnoHorario(id=idx, hora_inicio=h.hora_inicio, hora_fin=h.hora_fin, turno=t.nombre)
                idx += 1
                db.session.add(turno_horario)
                db.session.add(bloque)

        # PuedeDictar
        pd1 = PuedeDictar(profesor="1001", materia="MAT101", turno="Mañana", grupos_max=2)
        pd2 = PuedeDictar(profesor="1002", materia="FIS101", turno="Tarde", grupos_max=1)
        db.session.add_all([pd1, pd2])

        db.session.commit()
    print("Test data loaded successfully.")

    print("Base de datos inicializada y tablas creadas.")

if __name__ == "__main__":
    initialize_database()