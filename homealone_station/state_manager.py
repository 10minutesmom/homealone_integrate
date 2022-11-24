import time
import json
import datetime
import sqlite3
import DB_fetch
import DB_mod
import remote_control
import sms_function
import DB_reset

stage_dic = {'Not_in_home':'Not_in_home',
'No_schedule':'No_schedule',
'Safety_margin':'Safety_margin',
'Need_to_ready':'Need_to_ready',
'Move':'Move',
'Pause':'Pause'}

state_dic = {
'Hibernation_state' : 'Hibernation_state',
'Lazy_state': 'Lazy_state',
'Alert_state' :'Alert_state',
'Emergency_state' :'Emergency_state',
'Late' :'Late',
}

is_kid_ready_dic = {
'laying' : 'laying',
'sitting' : 'sitting',
'standing' : 'standing'
}

def state_reaction():
    cur_is_kid_home = bool(DB_fetch.get_is_kid_home)
    cur_where_is_kid = DB_fetch.get_where_is_kid
    cur_is_kid_ready = DB_fetch.get_is_kid_ready
    
    if (DB_fetch.get_current_state() == state_dic['Hibernation_state']):
        print('current state is : %s' %state_dic['Hibernation_state'])
        DB_reset.reset_lazy_cnt()
        DB_reset.reset_alert_cnt()
        print("lazy_cnt = ",DB_fetch.get_lazy_cnt())
        
    elif (DB_fetch.get_current_state() == state_dic['Lazy_state']):
        print('current state is : %s' %state_dic['Lazy_state'])
        DB_reset.reset_alert_cnt()
        print("lazy_cnt = ",DB_fetch.get_lazy_cnt())
        if(DB_fetch.get_lazy_cnt() == 2):
            remote_control.send_direction() #update is_kid_home, where_is_kid,is_kid_ready
            DB_reset.reset_lazy_cnt()
            return 0
        DB_mod.set_lazy_cnt(DB_fetch.get_lazy_cnt()+1)  
        
    elif (DB_fetch.get_current_state() == state_dic['Alert_state']):
        print('current state is : %s' %state_dic['Alert_state'])
        DB_reset.reset_lazy_cnt()
        print("lazy_cnt = ",DB_fetch.get_lazy_cnt())
        print("alert_cnt = ",DB_fetch.get_alert_cnt())
        if(DB_fetch.get_stage_rep() != 0):
            remote_control.send_direction()
        DB_mod.set_alert_cnt(DB_fetch.get_alert_cnt()+1)
        print("alert_cnt increased by 1 : result : %d" %DB_fetch.get_alert_cnt())  
        
    elif (DB_fetch.get_current_state() == state_dic['Emergency_state']):
        print('current state is : %s' %state_dic['Emergency_state'])
        DB_reset.reset_lazy_cnt()
        print("lazy_cnt = ",DB_fetch.get_lazy_cnt())
        print("alert_cnt = ",DB_fetch.get_alert_cnt())
        remote_control.send_direction() #update is_kid_home, where_is_kid,is_kid_ready
        sms_function.send_sms("Test message")
        DB_mod.set_alert_cnt(DB_fetch.get_alert_cnt()+1)  

    # For late state implement

    # elif (DB_fetch.get_current_state() == state_dic['Emergency_state']):
    #     print('current state is : %s' %state_dic['Emergency_state'])
    #     reset_lazy_cnt()
    #     print("lazy_cnt = ",DB_fetch.get_lazy_cnt())
    #     print("alert_cnt = ",DB_fetch.get_alert_cnt())
    #     remote_control.send_direction()#update is_kid_home, where_is_kid,is_kid_ready
    #     sms_function.send_sms("아이가 집에 없습니다.")
    #     DB_mod.set_alert_cnt(DB_fetch.get_lazy_cnt()+1)  
 

def state_manager():
    current_stage = DB_fetch.get_current_stage()

    print( '''is_kid_home : %d\n
cur_where_is_kid : %s\n
cur_is_kid_ready : %s\n
DB_fetch.get_stage_rep : %d\n'''
          %(DB_fetch.get_is_kid_home(),DB_fetch.get_where_is_kid(),DB_fetch.get_is_kid_ready(),DB_fetch.get_stage_rep()))
    
    if (current_stage == stage_dic['Not_in_home']):
        print('current_stage == %s' %stage_dic['Not_in_home'])
        DB_mod.set_current_state(state_dic['Hibernation_state'])
        
    elif (current_stage == stage_dic['No_schedule']):
        print('current_stage == %s' %stage_dic['No_schedule'])
        print('alert_cnt == %d'%DB_fetch.get_alert_cnt())
        
        #initialization
        if(DB_fetch.get_stage_rep() == 0):
            remote_control.send_direction() #update is_kid_home, where_is_kid,is_kid_ready
            
        if(DB_fetch.get_is_kid_home() == True):
            DB_mod.set_current_state(state_dic['Lazy_state'])
        
        elif(DB_fetch.get_is_kid_home() == False):
            if(DB_fetch.get_alert_cnt()<=2):
                DB_mod.set_current_state(state_dic['Alert_state'])
            else:
                DB_mod.set_current_state(state_dic['Emergency_state'])
                    
        state_reaction()
        DB_mod.set_stage_rep(DB_fetch.get_stage_rep()+1)
        
    elif (current_stage == stage_dic['Safety_margin']):
        print('current stage is : ',stage_dic['Safety_margin'])
        DB_mod.set_current_state(state_dic['Hibernation_state'])
        if(DB_fetch.get_stage_rep()==0):
            remote_control.play_sound()
    
    elif (current_stage == stage_dic['Need_to_ready']):
        print('current_stage == %s' %stage_dic['Need_to_ready'])
        
        #initialization
        if(DB_fetch.get_stage_rep() == 0):
            remote_control.send_direction() #update is_kid_home, where_is_kid,is_kid_ready
            remote_control.play_sound()
            
            if(DB_fetch.get_is_kid_ready() == is_kid_ready_dic['laying']):
                remote_control.play_sound()
                DB_mod.set_current_state(state_dic['alert_state'])
                
            else:
                remote_control.pause_sound()
                DB_mod.set_current_state(state_dic['alert_state'])
            return 0

        if(DB_fetch.get_is_kid_ready() == is_kid_ready_dic['laying'] or is_kid_ready_dic['sitting']):
            remote_control.play_sound()
            DB_mod.set_current_state(state_dic['alert_state'])
        else:
            remote_control.pause_sound()
            DB_mod.set_current_state(state_dic['alert_state'])
            
        state_reaction()   
        DB_mod.set_stage_rep(DB_fetch.get_stage_rep()+1)
        
    elif (current_stage == stage_dic['Move']):
        print('current_stage == %s' %stage_dic['Move'])
        
        #initialization
        if(DB_fetch.get_stage_rep() == 0):
            remote_control.send_direction() #update is_kid_home, where_is_kid,is_kid_ready
            remote_control.play_sound()
            return 0
        
        if(DB_fetch.get_is_kid_home == True):
            remote_control.play_sound()
            DB_mod.set_current_state(state_dic['alert_state'])
            
        else:
            remote_control.pause_sound()
            DB_mod.set_current_state(state_dic['alert_state'])
            
        state_reaction()   
        DB_mod.set_stage_rep(DB_fetch.get_stage_rep()+1)
        
    elif (current_stage == stage_dic['Pause']):
        print('current_stage == %s' %stage_dic['Pause'])