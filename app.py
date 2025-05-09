import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import time


df = pd.read_csv("https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station-set/all/period/latest-hour/data.csv",sep=';',skiprows=3)
df.columns = df.columns.str.strip()


print(df.head())

df_halmstad = df[df['StationsId'] == 62410 ]
temp_halmstad = df_halmstad.iloc[0,5]
print(df_halmstad)

halmstad_string = f'Temperaturen för {df_halmstad['Stationsnamn'].values[0]} är {temp_halmstad}'

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

print(halmstad_string)

print(temp_halmstad)

conn = sqlite3.connect('halmstad_temp.db')

cursor = conn.cursor()

cursor.execute('''
    INSERT INTO prev_temps (name, celsius,time)
    VALUES (?, ?,?)
''', (df_halmstad['Stationsnamn'].values[0], temp_halmstad,current_time))

conn.commit()