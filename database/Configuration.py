import mysql.connector
from mysql.connector import errorcode, MySQLConnection
import api.website_collecting as wc

db_url = "45.88.109.46"
db_port = 3306
db_schema_name = "feinstaub"
db_name = "feinstaub"
db_passwd = "feinstaub"


def connect() -> [None, MySQLConnection]:
    try:
        print(f"Attempting to connect to database located at {db_url}:{db_port}/{db_schema_name} with credentials name: {db_name}, passwd: {db_passwd}...")
        connection = mysql.connector.connect(host=db_url, port=db_port, user=db_name, password=db_passwd, database=db_schema_name)
        print("Connection established!")

        return connection
    except mysql.connector.Error as e:
        print("Error while connecting to database")
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password declined!")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Specified database / schema does not exist!")
        else:
            print(f"err {e.errno}")
            print(e)


db_connection = connect()

con = wc.DataCollector()
con.collect(db_url, db_port, db_schema_name, db_name, db_passwd)

def execute(sql) -> dict:
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(sql)

    return cursor.fetchall()
