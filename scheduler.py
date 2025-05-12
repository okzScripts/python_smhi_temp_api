import schedule
import time
import sqlite3
from datetime import datetime

from app import getLatestDBentry,WriteValueToDb,readValues

def scheduled_job():
    WriteValueToDb(readValues())

schedule.every(30).minutes.do(scheduled_job)
counter = 0
while True:
    
    schedule.run_pending()
    time.sleep(5)
    print(f"Awaiting new measured values from API... Count: {counter}")
    counter += 1
