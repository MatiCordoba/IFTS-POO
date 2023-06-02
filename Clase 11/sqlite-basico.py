import sqlite3

bd = sqlite3.connect("example.db")
print("Base de datos abierta")

################################################################
cur = bd.cursor()

# Crear una tabla con execute
cur.execute('''CREATE TABLE stocks
                (date text, trans text, symbol text, qty real, price real)''')


################################################################
# Insertar un registro
cur.execute('''INSERT INTO stocks VALUES ('2020-01-05', 'BUY', 'RHAT', 100, 35.14)''')

# Guardar los cambios
cur.commit()

# Nota:
# Se recomienda cerrar la conexión a la BD si hemos terminado. Solo debemos asegurarnos de que se hayan aplicado los cambios o se perderán
bd.close()

################################################################
# Nunca se debería hacer esto, es inseguro
# symbol = 'RHAT'
# cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Hacer esto
t = ('RHAT',)
cur.execute('SELECT * FROM sotcks WHERE symbol=?', t)
print(cur.fetchone())

################################################################
# Este ejemplo usa la forma con un iterador
purchases = [('2006-03-28', 'BUY', 'SONY', 1000, 45.00),
             ('2006-03-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-03-06', 'SELL', 'IBM', 500, 53.00),
            ]

cur.executemany('INSERT INTO stocks VALUES (?, ?, ?, ?, ?)', purchases)

################################################################
# Sentencia para eliminar
symbol = 'SONY'
sentencia = "DELETE FROM sotcks WHERE symbol = ?;"

# Eliminar el registro
cur.execute(sentencia, [symbol])
bd.commit()
print("Eliminado con éxito")

# Sentencia para actualizar
qty = 1500
price = 85.00
symbol = 'MSFT'
sentencia = "UPDATE stocks SET qty = ?, price = ? WHERE symbol = ?;"

# Actualizar datos
cur.execute(sentencia, [qty, price, symbol])
bd.commit
print("Datos guardados")

################################################################
# Para conectar MySQL y Python 3, tenemos que instalar el módulo PyMySQL con el siguiente comando:
# pip install PyMySQL