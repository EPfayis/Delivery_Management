from django.db import models

# Create your models here.

class TblItemMaster(models.Model):

    name = models.CharField(max_length= 100, null= False,blank= False)
    rate = models.FloatField(blank= False,null= False)
    is_active = models.BooleanField(null= False,blank= False,default= True)

    def __str__(self):
        return "%s" % (self.name)

