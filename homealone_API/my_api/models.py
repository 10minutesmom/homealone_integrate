from django.db import models


class Kid(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=10)
    is_kid_home=models.IntegerField()
    where_is_kid=models.CharField(max_length=10)
    is_kid_ready=models.CharField(max_length=10)
    schedule_uri=models.CharField(max_length=10)
    stage_uri=models.CharField(max_length=10)
    def __str__(self):
       return self.name
class Schedule(models.Model):
    schedule_dt=models.JSONField()

    
