from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class todo(models.Model):
    added_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
