from urllib.error import HTTPError

import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
import pymysql

class DataCollector:
    # Constructor - setzte als default das Jahr starten von gestern
    def __init__(self):
        self.end_date = date.today() - relativedelta(days=1)
        self.start_date = self.end_date - relativedelta(years=1)

        self.delta = self.end_date - self.start_date   # returns timedelta

    # Generiere eine Liste von URLs, die direkt auf die gewollten CSV Dateien zeigen
    # Pro Tag jeweils genau eine URL
    def get_url_list(self, sensorname, delta):
        hrefs = []
        for i in range(delta.days + 1):
            day = self.start_date + timedelta(days=i)
            if day.year != date.today().year:
                hrefs.append('https://archive.sensor.community/{}/{}/{}_{}'
                             .format(str(day.year), str(day), str(day), sensorname))
            else:
                hrefs.append('https://archive.sensor.community/{}/{}_{}'
                             .format(str(day), str(day), sensorname))
        return hrefs

    # Generiere die URLS
    # Hole die CSV Dateien ab
    # Und importiere sie in die mysql Datenbank
    def collect(self, db_url, db_port, db_schema_name, db_name, db_passwd):
        dht22_hrefs = self.get_url_list('dht22_sensor_3660.csv', self.delta)
        sds011_hrefs = self.get_url_list('sds011_sensor_3659.csv', self.delta)

        sql_engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?autocommit=true'
                                   .format(db_name, db_passwd, db_url, db_port, db_schema_name), pool_recycle=3600)
        db_connection = sql_engine.connect()

        for elem in dht22_hrefs:
            try:
                data = pd.read_csv(elem, sep=';')
                df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity'])
                df.to_sql('sensor_3659', db_connection, if_exists='replace', index=False)

            except HTTPError:
                print("WARNING - Got HttpError for {}".format(elem))

        for elem in sds011_hrefs:
            try:
                data = pd.read_csv(elem, sep=';')
                df = pd.DataFrame(data, columns=['timestamp', 'P1', 'P2'])
                df.to_sql('sensor_3660', db_connection, if_exists='replace', index=False)
            except HTTPError:
                print("WARNING - Got HttpError for {}".format(elem))
