from django.db import models
from General_Components.NameSpaces import *
from ItemMaster.models import TblItemMaster
from UserDetails.models import TblUserDetails
from ShopDetails.models import TblShopDetails

# Create your models here.


class TblStatus(models.Model):
    name = models.CharField(max_length= 50,null= False,blank= False,unique= True)
    is_public = models.BooleanField(null= False,blank= False)

    def __str__(self):
        return "%s" %(self.name)

class TblStatusDetails(models.Model):
    date = models.DateTimeField(null= False)
    user = models.ForeignKey(TblUserDetails, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(TblStatus,on_delete= models.PROTECT,null=True)
    description = models.CharField(max_length= 150)

class TblItemDetails(models.Model):
    item = models.ForeignKey(TblItemMaster,null= False,on_delete= models.PROTECT)
    rate = models.FloatField(null= False, blank= False)
    qty = models.FloatField(null= False,blank= False)
    total_amt = models.FloatField(null= False,blank= False)

class TblOrder(models.Model):
    date = models.DateTimeField(null= False,blank= False)
    customer = models.ForeignKey(TblUserDetails,null= False,blank= False,on_delete= models.PROTECT,related_name="Customer_User")
    delivery_boy = models.ForeignKey(TblUserDetails,null=True,blank= False,on_delete= models.PROTECT,related_name="Db_User")
    approved_by = models.ForeignKey(TblUserDetails,null= True,blank= False,on_delete= models.PROTECT,related_name="Approved_Usr")
    total_amt = models.FloatField(null= False,blank= False)
    is_delivered = models.BooleanField(null= False,blank= False)
    is_approved = models.BooleanField(null= False,blank= False)
    is_rejected = models.BooleanField(null= False,blank= False)
    items = models.ManyToManyField(TblItemDetails)
    status = models.ManyToManyField(TblStatusDetails)
    shop = models.ForeignKey(TblShopDetails,null= True,on_delete= models.PROTECT)

