import mysql.connector
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Razan2211",
        database="inventory_db"
    )
    return connection