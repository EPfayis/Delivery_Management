from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TblUserDetails(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    UserType = models.CharField(max_length=50,null= True)
    Address = models.CharField(max_length= 300,null= False)
    Mobile = models.CharField(max_length= 20)
