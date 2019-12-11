from django.db import models
from ItemMaster.models import TblItemMaster
from django.contrib.auth.models import User
from django.contrib.auth.models import User as DBUser

# Create your models here.

#Table to store the Itemdetails in an order
class TblItemDetails(models.Model):
    item_id = models.ForeignKey(TblItemMaster,on_delete= models.PROTECT)
    rate = models.FloatField(null= False,blank= False)
    qty = models.FloatField(null= False,blank= False)
    total = models.FloatField(null= False,blank= False)


#Table to store the status of the order
class TblStatus(models.Model):
    date = models.DateField(null= False,blank= False)
    status = models.CharField(max_length= 50,blank= False,null= False)

# Table to store the details of the order
class TblOrder(models.Model):
    order_date = models.DateField(null= False,blank= False)
    items = models.ManyToManyField(TblItemDetails)
    customer =models.ForeignKey(User,on_delete= models.PROTECT)
    delivery_boy = models.ForeignKey(User,related_name= "DBoy_USER",on_delete= models.PROTECT)
    status = models.ManyToManyField(TblStatus)
    total_amt = models.FloatField(null= False,blank= False)
    is_delivered = models.BooleanField(null= False,blank= False)





