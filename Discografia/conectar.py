import mysql.connector

class Conectar:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='MatteoCasal2009',
                database='discografia',
                ssl_disabled=True
            )
            if self.conexion.is_connected():
                print('Conexión exitosa a la base de datos')
        except Exception as ex:
            print('Error de conexión:', ex)
            self.conexion = None

    def cursor(self):
        return self.conexion.cursor()

    def commit(self):
        self.conexion.commit()

    def rollback(self):
        self.conexion.rollback()