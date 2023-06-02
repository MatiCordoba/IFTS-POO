import pymysql

try:
    db = pymysql.connect(host='localhost',
        port = 3306,
        user = 'root',
        password = '',
        db = 'example'                     
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall)
    db.close()
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Ocurrió un problema al conectar", e)