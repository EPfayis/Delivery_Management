from django.db import models
from General_Components.NameSpaces import *
from UserDetails.models import TblUserDetails
from ItemMaster.models import TblItemMaster

# Create your models here.

class TblLocation(models.Model):
    name = models.CharField(max_length= 100,blank= False,null= False)


class TblShopDetails(models.Model):
    shop_name = models.CharField(max_length= 300,null= False,blank= False)
    shop_address = models.CharField(max_length= 400, blank= False, null= False)
    city = models.ForeignKey(TblLocation,null= False,blank= False,on_delete= models.PROTECT)
    super_manager = models.ForeignKey(TblUserDetails,null= False,blank= False,on_delete= models.PROTECT)
    managers = models.ManyToManyField(TblUserDetails,blank= False,related_name= "UserManager")
    items = models.ManyToManyField(TblItemMaster,blank= False)
    is_approved = models.BooleanField(null= False,blank= False)
    is_active = models.BooleanField(blank= False,null= False)
