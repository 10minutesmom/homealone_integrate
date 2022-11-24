import time
import json
import datetime
import sqlite3

def get_is_kid_home():
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT is_kid_home FROM kid where id = 1")
    
    is_kid_home = c.fetchone()[0]
    conn.close()

    return int(is_kid_home)

def get_where_is_kid():
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT where_is_kid FROM kid where id = 1")
    
    where_is_kid = c.fetchone()[0]
    conn.close()

    return where_is_kid

def get_is_kid_ready():
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT is_kid_ready FROM kid where id = 1")
    
    is_kid_ready = c.fetchone()[0]
    conn.close()

    return is_kid_ready

def get_current_stage() :
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT current_stage FROM kid where id=1")
    
    current_state = c.fetchone()[0]
    conn.close()

    return current_state

def get_current_state() :
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT current_state FROM kid where id=1")
    
    current_state = c.fetchone()[0]
    conn.close()

    return current_state

def get_lazy_cnt() :
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT lazy_cnt FROM kid where id=1")
    
    lazy_cnt = c.fetchone()[0]
    conn.close()

    return int(lazy_cnt)

def get_alert_cnt() :
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT alert_cnt FROM kid where id=1")
    
    lazy_cnt = c.fetchone()[0]
    conn.close()

    return int(lazy_cnt)

def get_stage_rep():
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT stage_rep FROM kid where id=1")
    
    lazy_cnt = c.fetchone()[0]
    conn.close()

    return int(lazy_cnt)