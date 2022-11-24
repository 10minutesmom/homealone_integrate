from apscheduler.schedulers.background import BackgroundScheduler
import state_manager
import time
import json
import datetime
import sqlite3
import DB_reset
import DB_fetch
import DB_mod
import remote_control

sched = BackgroundScheduler()

stage_dic = {'Not_in_home':'Not_in_home',
'No_schedule':'No_schedule',
'Safety_margin':'Safety_margin',
'Need_to_ready':'Need_to_ready',
'Move':'Move',
'Pause':'Pause'}

replica_stage = [stage_dic['Not_in_home'],stage_dic['Not_in_home'],stage_dic['Not_in_home'],stage_dic['Not_in_home'],
                 stage_dic['No_schedule'],stage_dic['No_schedule'],stage_dic['No_schedule'],stage_dic['No_schedule'],
                 stage_dic['Safety_margin'],stage_dic['Safety_margin'],stage_dic['Safety_margin'],stage_dic['Safety_margin'],
                 stage_dic['Need_to_ready'],stage_dic['Need_to_ready'],stage_dic['Need_to_ready'],stage_dic['Need_to_ready'],
                 stage_dic['Move'],stage_dic['Move'],stage_dic['Move'],stage_dic['Move']]

def get_stage_from_JSON () :
    ts_h = str(datetime.datetime.now())[11:13]
    ts_m = str(int(int(str(datetime.datetime.now())[14:16])/10)*10)
    if(ts_m == '0'):ts_m = '00'
     
    
    conn = sqlite3.connect("stationdb.sqlite3", isolation_level=None)
    
    c = conn.cursor()
    c.execute("SELECT stage_uri FROM kid where id = 1")
    
    
    dir = c.fetchone()[0]
    conn.close()
    
    f = open(dir)
    data = json.load(f)
    current_stage = data['timetable']['mon'][ts_h][ts_m]['stage']
    f.close()
    
    return current_stage

@sched.scheduled_job('cron', hour='0-23', minute='*/10', id='req')
def req():
    print('\n\n',datetime.datetime.now())
    current_stage = DB_fetch.get_current_stage()
    next_stage = get_stage_from_JSON()
    
    print("current_stage = %s, and next_stage = %s"%(current_stage,next_stage))
    if (current_stage == next_stage):
        print('curr == next')
        state_manager.state_manager()
    else:
        print('curr != next')
        DB_reset.reset_alert_cnt()
        DB_reset.reset_lazy_cnt()
        DB_reset.reset_stage_rep()
        remote_control.pause_sound()
        DB_mod.set_current_stage(next_stage)
        state_manager.state_manager()
        
if __name__ == "__main__" : 
    DB_reset.reset_all()
    sched.start()
    while True:
        time.sleep(1)   

