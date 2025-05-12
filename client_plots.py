from datetime import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('halmstad_temp.db')

cursor = conn.cursor()

df = pd.read_sql_query(f'SELECT * FROM prev_temps ORDER BY time DESC LIMIT 25',conn)

print(df)

df['time'] = pd.to_datetime(df['time'],format='mixed')
df['time'] = df['time'].dt.floor('s')

df = df.sort_values('time')
df['celsius'] = df['celsius'].astype(float)

print(df[['time','celsius']])

plt.figure(figsize=(10, 5))
plt.plot(df['time'], df['celsius'], marker='o', linestyle='-', color='skyblue')
plt.title('Temperature - Halmstad Flygplats')
plt.xlabel('Date')
plt.ylabel('Temp')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()