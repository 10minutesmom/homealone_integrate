from django.urls import include, path
from rest_framework import routers
#from my_api.views import SpeciesListAPIView
#from my_api.views import index
from . views import *
from django.contrib import admin
from my_api.views import KidsViewSet,ScheduleViewSet
router = routers.DefaultRouter()
router.register(r'kids', KidsViewSet)
router.register(r'schedule',ScheduleViewSet)

urlpatterns = [
  #path('get/', views.SpeciesListAPIView.as_view()),
   #path('',views.index, name='index')
path('', include(router.urls)),
path('/scheduleAllinit', schedule_All, name='schedule_All'),
#path('schedulepost',schedule_post,name='schedule_post')
path('/scheduleallrecent',schedule_All_recent, name='schedule_All_recent'),
path('/scheduleadd',schedule_add,name='schedule_add'),
path('/schedulemodify',schedule_modify,name='schedule_modify'),
path('/scheduledelete',schedule_delete,name='schedule_delete'),
path('/schedulerecent',schedule_recent,name='schedule_recent'),

#path('scheduleAdd/',schedule_Add, name='schedule_Add'),
#path('scheduleModify/',schedule_Modify, name='schedule_Modify'),
#path('scheduledelete/',schedule_delete, name='schedule_delete'),

]