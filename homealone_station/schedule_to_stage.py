import time
import json
import pandas as pd
import datetime
import sqlite3


def fetch_schedule () :
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT schedule_uri FROM kid")
    
    dir = c.fetchone()[0]
    conn.close()
    
    f = open(dir)
    schedule_JSON = json.load(f)
    f.close()

    return schedule_JSON

def convert_schedule_to_stage(data):
    pass

if __name__ == "__main__" :   
    print(datetime.datetime.now())
    
    dir = './scheduleData.json'
    f = open(dir)
    
    schedule_JSON = fetch_schedule()
    timetable = schedule_JSON['timetable']
    timetable_df = pd.DataFrame.from_dict(timetable)
    print(timetable_df['mon'])
    


