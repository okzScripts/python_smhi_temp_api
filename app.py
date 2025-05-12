
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime,timedelta


def getLatestDBentry():
    try:
        conn = sqlite3.connect('halmstad_temp.db')
        cursor = conn.cursor()
        cursor.execute("SELECT time FROM prev_temps ORDER BY time DESC LIMIT 1")

        last_entry = cursor.fetchone()

        if last_entry:
            return datetime.fromisoformat(last_entry[0])
        else:
            return None
    except sqlite3.Error as e:
        print(f'Error: {e}')
    finally:
        cursor.close()

def readValues():
    df = pd.read_csv("https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station-set/all/period/latest-hour/data.csv",sep=';',skiprows=3)
    df.columns = df.columns.str.strip()


    print(df.head())
    df_halmstad = df[df['StationsId'] == 62410 ]
    return df_halmstad.iloc[0,5]

def WriteValueToDb(temp):
    timestamp = datetime.now().isoformat(sep=' ',timespec='seconds')
    
    if datetime.now() - getLatestDBentry() > timedelta(minutes=15):
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
    else:
        print(f'The latest entry was {datetime.now() - getLatestDBentry()} ago, too early to write new entry')
        return 'Script good, but no db entry'


print(WriteValueToDb(readValues()))
