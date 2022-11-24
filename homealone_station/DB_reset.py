import sqlite3

def reset_current_stage():

    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)

    c = conn.cursor()

    c.execute("UPDATE kid set current_stage='' where id = 1")
    conn.close()
    
def reset_current_state():    
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)

    c = conn.cursor()

    c.execute("UPDATE kid set current_state='' where id = 1")
    conn.close()
    
def reset_lazy_cnt():   
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)

    c = conn.cursor()

    c.execute("UPDATE kid set lazy_cnt=0 where id = 1")
    conn.close()
    
def reset_alert_cnt():    
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)

    c = conn.cursor()

    c.execute("UPDATE kid set alert_cnt=0 where id = 1")
    conn.close()
    
def reset_stage_rep():   
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)

    c = conn.cursor()

    c.execute("UPDATE kid set stage_rep=0 where id = 1")
    conn.close()
    
def reset_cnt():
    reset_lazy_cnt()
    reset_alert_cnt()
    reset_stage_rep()
    
def reset_all():
    reset_current_stage()
    reset_current_state()
    
    reset_lazy_cnt()
    reset_alert_cnt()
    reset_stage_rep()