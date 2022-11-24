from rest_framework import serializers
from my_api.models import  Kid,Schedule

class KidSerializer(serializers.ModelSerializer):
   class Meta:
       model = Kid
       fields = ('id', 'name', 'is_kid_home', 'where_is_kid', 'is_kid_ready','schedule_uri','stage_uri')
       #fields={'is_kid_home', 'where_is_kid'}

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Schedule
        fields="__all__"

class DictSerializer(serializers.Serializer):
    dict=serializers.JSONField()

