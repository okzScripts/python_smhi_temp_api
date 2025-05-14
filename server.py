from flask import Flask, jsonify
import sqlite3
import pandas as pd
from datetime import datetime

class TempRecord:
    def __init__(self,id:int, celsius: float, time:str):
        self.id      = id
        self.celsius = celsius
        self.time    = datetime.fromisoformat(time) if isinstance (time,str) else time

    def To_Dict(self):
        return {
            'id': self.id,
            'celsius': self.celsius,
            'time': self.time.isoformat()
        }



app = Flask(__name__)

@app.route('/temperatures',methods=['GET'])
def GetTemps():
    conn = sqlite3.connect('halmstad_temp.db')
    df = pd.read_sql_query('SELECT id,time,celsius FROM prev_temps ORDER BY id DESC LIMIT 25',conn)
    df['time'] = pd.to_datetime(df['time'],format='mixed')
    df['celsius'] = df['celsius'].astype(float)
    result = df.iterrows()
    conn.close()
    records = [
        TempRecord(row['id'], row['celsius'], row['time']).To_Dict()
        for _, row in df.iterrows()
    ]
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
