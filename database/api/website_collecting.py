from urllib.error import HTTPError

import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy import text



class DataCollector:
    # Constructor - setzt den Start auf den 14.03.2022 und das Ende auf den gestrigen Tag
    def __init__(self):
        self.end_date = date.today() - relativedelta(days=1)
        self.start_date = date(2022, 3, 14)

        self.delta = self.end_date - self.start_date   # returns timedelta (Differenz)

    # Generiere eine Liste von URLs, die direkt auf die gewollten CSV Dateien zeigen
    # Pro Tag jeweils genau eine URL
    def get_url_list(self, sensorname, delta):
        hrefs = []
        #delta.days die Anzahl der Tage zwischen definiertem Start und Ende
        for i in range(delta.days + 1):
            #Datum des gesuchten Tages
            day = self.start_date + timedelta(days=i)
            if day.year != date.today().year:
                #Vergangene Jahre (werden nur mit dem Jahr angezeigt)
                hrefs.append('https://archive.sensor.community/{}/{}/{}_{}'
                             .format(str(day.year), str(day), str(day), sensorname))
            else:
                #Aktuelle Jahr (Da es mit dem Aktuellen Datum angezeigt wird)
                hrefs.append('https://archive.sensor.community/{}/{}_{}'
                             .format(str(day), str(day), sensorname))
        return hrefs



    # Generiere die URLS
    # Hole die CSV Dateien ab
    # Und importiere sie in die mysql Datenbank

    #Zugriffsdaten unserer MySQL Datenbank
    def collect(self, db_url, db_port, db_schema_name, db_name, db_passwd):

        #Speichert eine Liste von URLs in einem Array
        dht22_hrefs = self.get_url_list('dht22_sensor_3660.csv', self.delta)
        sds011_hrefs = self.get_url_list('sds011_sensor_3659.csv', self.delta)

        #SQL Alchemy connection
        sql_engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?autocommit=true'
                                   .format(db_name, db_passwd, db_url, db_port, db_schema_name), pool_recycle=3600)
        db_connection = sql_engine.connect()

        #Leeren beider Tabellen in der Datenbank
        db_connection.execute(text("DELETE FROM sensor_3659"))
        db_connection.execute(text("DELETE FROM sensor_3660"))

        for elem in dht22_hrefs:
            try:
                #csv wird ausgelesen aus der URL/ URL sind getrennt durch ein Semikolon
                data = pd.read_csv(elem, sep=';')
                #Umwandeln in ein Data Frame / Spalten werden definiert
                df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity'])
                #timestamp = Datentyp Datum
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                #Dataframe wird in die MySQL Datenbank übertragen
                #if_exists = 'append' wird in eine vorhandene Tabelle eingefügt
                df.to_sql('sensor_3660', db_connection, if_exists='append', index=False)

            except HTTPError:
                print("WARNING - Got HttpError for {}".format(elem))

        for elem in sds011_hrefs:
            try:
                data = pd.read_csv(elem, sep=';')
                df = pd.DataFrame(data, columns=['timestamp', 'P1', 'P2'])
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df.to_sql('sensor_3659', db_connection, if_exists='append', index=False)

            except HTTPError:
                print("WARNING - Got HttpError for {}".format(elem))
