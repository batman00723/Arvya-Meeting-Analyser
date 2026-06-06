from django.db import models


class MeetingReport(models.Model):
    created_at= models.DateTimeField(auto_now_add= True)
    transcript= models.TextField()
    analysis= models.JSONField()