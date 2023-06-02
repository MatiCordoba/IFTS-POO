import sqlite3

# En este bloque vamos a tener la conexión con la base de datos. También la función de crear tabla
def conexionBD():
    bd = sqlite3.connect("Clase 11/empleados.bd")
    print("Base de datos abierta")
    return bd

conexion = conexionBD()

def crearTabla(conexion):
    cur = conexion.cursor()

    cur.execute('''CREATE TABLE empleados
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nro_legajo INTEGER NOT NULL UNIQUE,
                    dni INTEGER NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    area TEXT NOT NULL)''')

    conexion.commit()


# En este bloque vamos a tener la lógica de cada una de las opciones de la app.
# Pero primero vamos a crear el menú que nos permita acceder a cada opción de la app.


def inicioApp(conexion):
    print("--- Menú de opciones ---")
    print("Opción 1: Insertar un registro de empleado")
    print("Opción 2: Seleccionar un registro de empleado a partir de su número DNI")
    print("Opción 3: Seleccionar todos los empleados o los registros de la tabla")
    print("Opción 4: Modificar el area de un empleado en función de su número de legajo")
    print("Opción 5: Eliminar un empleado a partir del número de legajo")
    print("Opción 6: Finalizar")
    opcion = int(input(f'Escriba el número de la opción que desea inicializar: '))

    if opcion < 1 or opcion > 6:
        raise ValueError(f'Es imposible acceder a la opción => {opcion}')
    elif opcion == 1:
        insertarRegistro(conexion)
    elif opcion == 2:
        seleccionarRegistro_DNI(conexion)
    elif opcion == 3:
        seleccionarTodo(conexion)
    elif opcion == 4:
        modificarArea(conexion)
    elif opcion == 5:
        eliminarEmpleado(conexion)
    elif opcion == 6:
        print("Se ha finalizado su sesión.")
        return False
    return True
    

def insertarRegistro(conexion):
    cur = conexion.cursor()

    nro_legajo = int(input("Inserte el número de legajo: "))
    dni = int(input("Inserte el DNI sin puntos: "))
    nombre = input("Inserte el nombre: ")
    apellido = input("Inserte el apellido: ")
    area = input("Inserte el área: ")

    cur.execute("INSERT INTO empleados (nro_legajo, dni, nombre, apellido, area) VALUES (?, ?, ?, ?, ?)", 
                (nro_legajo, dni, nombre, apellido, area))

    conexion.commit()
    print(f"Se ha agregado el nuevo registro de {apellido}, {nombre} satisfactoriamente")

def seleccionarRegistro_DNI(conexion):
    cur = conexion.cursor()

    dni = int(input("Ingrese el número de DNI sin puntos: "))
    s = (dni,)
    cur.execute("SELECT * FROM empleados WHERE dni = ?", s)
    print(cur.fetchone())

def seleccionarTodo(conexion):
    cur = conexion.cursor()
    cur.execute("SELECT * FROM empleados ORDER BY id ASC")
    print(cur.fetchall())

def modificarArea(conexion):
    cur = conexion.cursor()

    nro_legajo = int(input("Para modificar el area del emplaeado, ingrese el número de legajo: "))
    area = input("Ingrese el nuevo área: ")
    sentencia = "UPDATE empleados SET area = ? WHERE nro_legajo = ?;"

    cur.execute(sentencia, [area, nro_legajo])
    conexion.commit()
    print("Área del empleado actualizado")

def eliminarEmpleado(conexion):
    cur = conexion.cursor()

    intentoSeguridad = int(input("Inserte el número de legajo que desea eliminar: "))
    nro_legajo = int(input("Vuelva a insertar el número de legajo que desea eliminar: "))

    if intentoSeguridad == nro_legajo:
        sentencia = "DELETE FROM empleados WHERE nro_legajo = ?;"
        cur.execute(sentencia, [nro_legajo])
    else:
        print("Los números de legajo no coinciden, vuelva a intentarlo")
        return True

    conexion.commit()
    print("Legajo eliminado correctamente")


# En este bloque vamos a verificar si la tabla existe antes de crearla.
# Además de esto, vamos a hacer la conexión con la tabla y la base de datos
# Y, por último, cerramos la conexión con la base de datos

def tablaExiste(conexion):
    cur = conexion.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='empleados'")
    return cur.fetchone() is not None

def eliminarTabla(conexion):
    cur = conexion.cursor()

    cur.execute("DROP TABLE IF EXISTS empleados")
    conexion.commit()

if not tablaExiste(conexion):
    crearTabla(conexion)
    print("Tabla creada")


# En este bloque vamos a dar inicio a la app hasta que la función nos indique terminarla.
while True:
    if not inicioApp(conexion):
        break


conexion.close()