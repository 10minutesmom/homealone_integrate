#from django.shortcuts import render
from rest_framework import viewsets
#from rest_framework.response import APIView
from my_api.serializers import KidSerializer,ScheduleSerializer,DictSerializer
from my_api.models import Kid,Schedule
#from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import pickle
#from .models import Kid
#from .serializers import SpeciesSerializer
from rest_framework.parsers import JSONParser
from datetime import datetime
def getNextTime(init_time):
   hour=int(init_time.split(':')[0])
   min=int(init_time.split(':')[1])
   min=min+10#add minutes
   if(min==60):
      hour=hour+1
      min=00

   if(hour<10):
      init_time='0'+str(hour)+":"+str(min).zfill(2)
   else:
      init_time=str(hour)+':'+str(min).zfill(2)
   return init_time
def getPrevTime(init_time):
   hour=int(init_time.split(':')[0])
   min=int(init_time.split(':')[1])
   min=min-10#add minutes
   if(min<0):
      hour=hour-1
      min=50    

   if(hour<10):
      init_time='0'+str(hour)+":"+str(min).zfill(2)
   else:
      init_time=str(hour)+':'+str(min).zfill(2)
   return init_time 
success_message={
   'message':'success'
}
fail_message={
   'message:':'fail'
}
null_dict={
    "id": "0",
    "title": "",
    "location": "",
    "scheduleType": "",
    "readyTime": 0,
    "movingTime": 0
          }
def time_parser(start_time,end_time):
    init_time=start_time
    time_list=[]
    while(True):
        time_list.append(init_time)
        hour=int(init_time.split(':')[0])
        min=int(init_time.split(':')[1])
        min=min+10#add minutes
        if(min==60):
            hour=hour+1
            min=0

        if(hour<10):
            init_time='0'+str(hour)+":"+str(min).zfill(2)
        else:
            init_time=str(hour)+':'+str(min).zfill(2)
        if(init_time==end_time):
            return time_list



#file_open = open("file path", 'r', encoding="UTF-8")
def schedule_All(uid):
   file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"
   with open(file_path, 'r',encoding='UTF-8') as file:
      data = json.load(file)
      #print(type(data))
   return JsonResponse(data)

#def schedule_recent(uid):
   #file_path = r"C:\Users\조세연\myproject\Scripts\my_django_project\my_api\schedule.json"
   #with open(file_path, 'r',encoding='UTF-8') as file:
      #data=json.load(file)
   #day,time_hr,time_min='mon',str(13),str(20)
   #rst_data=data[day][time_hr][time_min]
   #return JsonResponse(rst_data)
class KidsViewSet(viewsets.ModelViewSet):
   queryset = Kid.objects.all()
   serializer_class = KidSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

@api_view(['POST'])
def schedule_All_recent(request):
    if request.method=='POST':
        body=json.loads(request.body.decode('UTF-8'))
        file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"
        with open(file_path,"w")as outfile:
            json.dump(body,outfile,ensure_ascii=False)
        return HttpResponse(body)
    else:
        return HttpResponse("Fail")
   #return HttpResponse(self)
   
@api_view(['POST'])
def schedule_add(request):
   if request.method=='POST':
      body=json.loads(request.body.decode('UTF-8'))
      file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"#file path of schedule data
      with open(file_path,'r',encoding='UTF-8')as file:
         data=json.load(file) #LOAD DATASET

      date_time=body['time']
      start_time=date_time['startHour']+":"+date_time['startMin']#parsing starttime
      end_time=date_time['endHour']+":"+date_time['endMin']#parsing endtime
      day=date_time['day']#parsing day
      parsed_data=data['timetable']
      parsed_data=parsed_data[day]
      time_parsed_list=time_parser(start_time,end_time)
      
      del body['uid']
      del body['time']
      for i in time_parsed_list:#checking schedule exists
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         if(parsed_data[dy][mth]['id']!='0'):
            return JsonResponse(fail_message)
      for i in time_parsed_list:#modify dict
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         parsed_data[dy][mth]=body
      with open(file_path,"w",encoding='UTF-8')as outfile:
         json.dump(data,outfile,ensure_ascii=False)
      return JsonResponse(success_message)

@api_view(['POST'])
def schedule_modify(request):#Load->delete->insert
   if request.method=='POST':
      body=json.loads(request.body.decode('UTF-8'))
      file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"#file path of schedule data
      with open(file_path,'r',encoding='UTF-8')as file:
         data=json.load(file) #LOAD DATASET

      dl_date_time=body['prevTime']
      dl_start_time=dl_date_time['startHour']+":"+dl_date_time['startMin']#parsing starttime
      dl_end_time=dl_date_time['endHour']+":"+dl_date_time['endMin']#parsing endtime
      dl_day=dl_date_time['day']#parsing day
      dl_parsed_data=data['timetable']
      dl_parsed_data=dl_parsed_data[dl_day]
      dl_time_parsed_list=time_parser(dl_start_time,dl_end_time)
      dl_time_parsed_list.append(dl_end_time)

      for i in dl_time_parsed_list:#checking schedule exists
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         if(dl_parsed_data[dy][mth]['id']=='0'): #if empty, we cannot erase
            return JsonResponse({'message':'fail'})
      
      for i in dl_time_parsed_list:#modify dict
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         dl_parsed_data[dy][mth]=null_dict#delete
      
      del body['prevTime']
      
      date_time=body['time']
      start_time=date_time['startHour']+":"+date_time['startMin']#parsing starttime
      end_time=date_time['endHour']+":"+date_time['endMin']#parsing endtime
      day=date_time['day']#parsing day
      parsed_data=data['timetable']
      parsed_data=parsed_data[day]
      time_parsed_list=time_parser(start_time,end_time)
      del body['uid']
      del body['time']
      for i in time_parsed_list:#checking schedule exists
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         if(parsed_data[dy][mth]['id']!='0'):
            return JsonResponse({'message':'failed'})
      for i in time_parsed_list:#modify dict
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         parsed_data[dy][mth]=body
      with open(file_path,"w",encoding='UTF-8')as outfile:
         json.dump(data,outfile,ensure_ascii=False)
      return JsonResponse({'message':'successed'})

@api_view(['POST'])
def schedule_delete(request):#Load->delete->insert
   if request.method=='POST':
      body=json.loads(request.body.decode('UTF-8'))
      file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"#file path of schedule data
      with open(file_path,'r',encoding='UTF-8')as file:
         data=json.load(file) #LOAD DATASET

      dl_date_time=body['time']
      dl_start_time=dl_date_time['startHour']+":"+dl_date_time['startMin']#parsing starttime
      dl_end_time=dl_date_time['endHour']+":"+dl_date_time['endMin']#parsing endtime
      dl_day=dl_date_time['day']#parsing day
      dl_parsed_data=data['timetable']
      dl_parsed_data=dl_parsed_data[dl_day]
      dl_time_parsed_list=time_parser(dl_start_time,dl_end_time)
      dl_time_parsed_list.append(dl_end_time)

      for i in dl_time_parsed_list:#checking schedule exists
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         if(dl_parsed_data[dy][mth]['id']=='0'): #if empty, we cannot erase
            return JsonResponse({'message':'fail'})
      
      for i in dl_time_parsed_list:#modify dict
         dy=i.split(":")[0]
         mth=i.split(":")[1]
         dl_parsed_data[dy][mth]=null_dict#delete
      with open(file_path,"w",encoding='UTF-8')as outfile:
         json.dump(data,outfile,ensure_ascii=False)
      return JsonResponse({'message':'success'})
@api_view(['GET'])
def schedule_recent(request):
   if request.method=='GET':
      file_path = r"C:\Users\조세연\Desktop\bin\schedule_origin.json"
      with open(file_path, 'r',encoding='UTF-8') as file:
         data = json.load(file)
      now=datetime.now()
      dayNum=datetime.today().weekday()
      if(dayNum==0):
         c_day='mon'
      elif(dayNum==1):
         c_day='tue'
      elif(dayNum==2):
         c_day='wed'
      elif(dayNum==3):
         c_day='thu'
      elif(dayNum==4):
         c_day='fri'
      else:
         c_day='weekend'
      c_min=(now.minute)
      if(c_min==0):
         c_min='00'
         c_hour=str(now.hour).zfill(2)
      elif(c_min<=10):
         c_min='10'
         c_hour=str(now.hour).zfill(2)
      elif(c_min<=20):
         c_min='20'
         c_hour=str(now.hour).zfill(2)
      elif(c_min<=30):
         c_min='30'
         c_hour=str(now.hour).zfill(2)
      elif(c_min<=40):
         c_min='40'
         c_hour=str(now.hour).zfill(2)
      elif(c_min<=50):
         c_min='50'
         c_hour=str(now.hour).zfill(2)
      else:
         c_min='00'
         c_hour=now.hour+1
         c_hour=str(c_hour).zfill(2)
      dl_parsed_data=data['timetable']
      date_time=c_hour+':'+c_min
      c_hour,c_min=date_time.split(":")[0].zfill(2),date_time.split(":")[1].zfill(2)###
      if(dl_parsed_data[c_day][c_hour][c_min]['id']=='0'):#schedule empty check
         while(True):#if it is empty, we should find upcoming schedule
            date_time=getNextTime(date_time)#next 10 minutes
            c_hour,c_min=date_time.split(":")[0],date_time.split(":")[1]#spliting into hour,minutes
            if(c_hour=='24'):#
               return JsonResponse({'message':'No schedule!!'})#
            if(dl_parsed_data[c_day][c_hour][c_min]['id']!='0'):#checkingS if its zero
               rtData=dl_parsed_data[c_day][c_hour][c_min]#insert data into rtDATA(Return data)
               break #find schedule
         c_hour,c_min,cid=date_time.split(":")[0],date_time.split(":")[1],dl_parsed_data[c_day][c_hour][c_min]['id']#get current hour, get current id
         startHour,startMin=c_hour,c_min#setting up startHour,startMin
         while(True):
            date_time=getNextTime(date_time)#next time
            c_hour,c_min=date_time.split(":")[0],date_time.split(":")[1]
            if(dl_parsed_data[c_day][c_hour][c_min]['id']!=cid):
               break
         endHour,endMin=date_time.split(":")[0],date_time.split(":")[1] #endHour,endMin
         time={
        'day':c_day,
        'startHour':startHour,
        'startMin':startMin,
        'endHour':endHour,
        "endMin":endMin
         }
         rtData.update(time)
         return JsonResponse(rtData)#####
      else:#schedule exists
         uid=dl_parsed_data[c_day][c_hour][c_min]['id']#get uid
         init_time=date_time #앞으로 갈때 찾으려고 저장함
         prev_time=getPrevTime(init_time)#get prevTime
         prev_hour,prev_min=prev_time.split(":")[0],prev_time.split(":")[1]
         prev_id=dl_parsed_data[c_day][prev_hour][prev_min]['id']#get prev_id
         if(uid==prev_id):#If it exists, it is continuing schedule
            while(True):
               date_time=getNextTime(date_time)#get next date_time(10 minutes)
               c_hour,c_min=date_time.split(":")[0],date_time.split(":")[1]#slicing hour,min
               if(c_hour=='24'):
                  return JsonResponse({'message':'No schedule left!'})
               if(dl_parsed_data[c_day][c_hour][c_min]['id']!=uid and dl_parsed_data[c_day][c_hour][c_min]['id']!='0'):#checking id is not null and not 중복
                  rtData,cid=dl_parsed_data[c_day][c_hour][c_min],dl_parsed_data[c_day][c_hour][c_min]['id']#rt data랑 cid찾음
                  break
            startHour,startMin=date_time.split(":")[0],date_time.split(":")[1]#set up startHour and startMin
            while(True):#endhour찾기
               date_time=getNextTime(date_time)
               c_hour,c_min=date_time.split(":")[0],date_time.split(":")[1]
               if(dl_parsed_data[c_day][c_hour][c_min]['id']!=cid):#find different uid
                  break#end of loop
            endHour,endMin=date_time.split(":")[0],date_time.split(":")[1]
            time={
               'day':c_day,
               'startHour':startHour,
               'startMin':startMin,
               'endHour':endHour,
               "endMin":endMin
               }
            rtData.update(time)
            return JsonResponse(rtData)
         else:#schedule ended, new schedule starts at timeunit
            rtData=dl_parsed_data[c_day][c_hour][c_min]#current data into rtData
            startHour,startMin=init_time.split(":")[0],init_time.split(":")[1]
            while(True):
               date_time=getNextTime(date_time)#getting next time
               c_hour,c_min=date_time.split(":")[0],date_time.split(":")[1]
               if(dl_parsed_data[c_day][c_hour][c_min]['id']!=uid):
                  break
            endHour,endMin=date_time.split(":")[0],date_time.split(":")[1]#endHour get
            time={
            'day':c_day,
            'startHour':startHour,
            'startMin':startMin,
            'endHour':endHour,
            "endMin":endMin}
            rtData.update(time)
            return JsonResponse(rtData)





