
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

def readValues():
    df = pd.read_csv("https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station-set/all/period/latest-hour/data.csv",sep=';',skiprows=3)
    df.columns = df.columns.str.strip()


    print(df.head())
    df_halmstad = df[df['StationsId'] == 62410 ]
    return df_halmstad.iloc[0,5]

def WriteValueToDb(temp):
    timestamp = datetime.now().isoformat(sep=' ',timespec='seconds')
    try:
        conn = sqlite3.connect('halmstad_temp.db')

        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO prev_temps (name, celsius,time)
            VALUES (?, ?,?)
            ''', ('Halmstad Flygplats', temp, timestamp))

        conn.commit()
        return 'Temperature successfully written to db'
    except sqlite3.Error as e:
        return f'Error writing to db: {e}'
    finally:
        conn.close()
        print('Db connection closed')


print(WriteValueToDb(readValues()))