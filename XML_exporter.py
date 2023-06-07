import xml.etree.ElementTree
from database.Configuration import *

cur = db_connection.cursor()
test = cur.execute("SELECT * from sensor_3660")
print(con)