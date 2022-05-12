import sqlite3
import datetime

"""
datetime.datetime.now().replace(microsecond=0).isoformat()

devuelve fecha hora actual en formato ISO8601 simple

yyyymmddThh:mm:ss

"""


class Persona:
    def __init__(self, dni, apellido, nombre='', movil=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil
        


def ingresa_visita(persona):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        print(q)
        conn.execute(q)
        conn.commit()

        

    destino = input("Ingrese destino: ")

    horaActual = datetime.datetime.now().replace(microsecond=0).isoformat()

    q = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, destino)
            VALUES ('{persona.dni}',
                    '{horaActual}',
                    '{destino}');"""
    conn.execute(q)
    conn.commit()
    
    conn.close()
    

def egresa_visita (dni):
    """Coloca fecha y hora de egreso al visitante con dni dado"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{dni}'"""

    resu = conn.execute(q)

    horaActual = datetime.datetime.now().replace(microsecond=0).isoformat()

    if resu.fetchone():
        q = f"""UPDATE ingresos_egresos set fechahora_out =
                '{horaActual}' WHERE dni = '{dni}';"""
        conn.execute(q)
        conn.commit()
    
    conn.close()


def lista_visitantes_en_institucion ():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT * FROM personas;"""

    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def busca_visitantes(fecha_desde, fecha_hasta, destino, dni ):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')

    cond = ""
    base =  "SELECT * FROM ingresos_egresos "

    if dni != '':
        cond += f'dni = {dni} AND'
    elif fecha_desde != '':
        cond += f'fechahora_in = {fecha_desde} AND'
    elif fecha_hasta != '':
        cond += f'fechahora_out = {fecha_hasta} AND'
    elif destino != '':
        cond += f'destino = {destino} AND'

    base += ' WHERE ' + cond
    base = base[:-3]
    f = conn.execute(base)
    
    for fila in f:
        print(fila)

    conn.close()


def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL

           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT

           );'''

    conn.execute(qry)


if __name__ == '__main__':
    iniciar()

    
        
    """
    doc = input("Igrese dni> ")
    apellido = input("Igrese apellido> ")
    nombre = input("nombre> ")
    movil = input("móvil > ")

    p = Persona(doc, apellido, nombre, movil)
    
    ingresa_visita(p)
    """
    
    # lista_visitantes_en_institucion()
    
