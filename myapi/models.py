from django.db import models

class Recipent(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MeetingReport(models.Model):
    created_at= models.DateTimeField(auto_now_add= True)
    transcript= models.TextField()
    analysis= models.JSONField()

