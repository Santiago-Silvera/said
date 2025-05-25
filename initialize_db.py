from datetime import time

def initialize_database():
    from said import app
    from entities import db, Profesor, Materia, Horario, BloqueHorario, Turno, TurnoHorario, PuedeDictar, Persona

    with app.app_context():
        db.drop_all()
        db.create_all()

        pers1 = Persona(cedula="1001", nombre="Juan", mail="test@test.com")
        pers2 = Persona(cedula="1002", nombre="Ana")
        db.session.add_all([pers1, pers2])

        # Profesores
        prof1 = Profesor(cedula="1001", nombre="jp", nombre_completo="Juan Pérez")
        prof2 = Profesor(cedula="1002", nombre="am", nombre_completo="Ana Gómez")
        db.session.add_all([prof1, prof2])

        # Materias
        mat1 = Materia(nombre="MAT101", nombre_completo="Matemática Básica")
        mat2 = Materia(nombre="FIS101", nombre_completo="Física General")
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
            for h in [hor1, hor2]:
                bloque = BloqueHorario(id=idx, dia=dia, hora_inicio=h.hora_inicio, hora_fin=h.hora_fin)
                idx += 1
                db.session.add(bloque)

        for t, h in zip([turno1, turno2], [hor1, hor2]):
            turno_horario = TurnoHorario(hora_inicio=h.hora_inicio, hora_fin=h.hora_fin, turno=t.nombre)
            db.session.add(turno_horario)
        # PuedeDictar
        pd1 = PuedeDictar(profesor="jp", materia="MAT101", turno="Mañana", grupos_max=2)
        pd2 = PuedeDictar(profesor="jp", materia="FIS101", turno="Tarde", grupos_max=1)
        db.session.add_all([pd1, pd2])

        db.session.commit()
    print("Test data loaded successfully.")

    print("Base de datos inicializada y tablas creadas.")

def cargar_personas_desde_excel(path_xlsx):
    from said import app
    from entities import db, Persona, Profesor
    import pandas as pd
    df = pd.read_excel(path_xlsx)
    # Espera columnas: 'Cedula', 'Nombre', 'Mail'
    with app.app_context():
        for _, row in df.iterrows():
            ci: str = str(row['Cedula']).strip()
            nombre: str = row['Nombre']
            mail = row['Mail']
            if pd.isna(mail):
                mail = ""
            print(f"CI: {ci}, Nombre: {nombre}, Mail: {mail}")
            persona = Persona(
                cedula=ci,
                nombre=nombre,  # Primer nombre
                mail=mail,
            )
            nombre = ''.join(word[0].lower() for word in nombre.split())
            profesor = Profesor(
                cedula=ci,
                nombre=nombre,
                nombre_completo=nombre,
            )
            db.session.merge(persona)  # merge para upsert
            db.session.merge(profesor)  # merge para upsert
        db.session.commit()
        print("Profesores cargados correctamente.")

if __name__ == "__main__":
    initialize_database()
    cargar_personas_desde_excel("profesores.xlsx")