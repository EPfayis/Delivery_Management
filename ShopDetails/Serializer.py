from General_Components.NameSpaces import *
from .models import *
from UserDetails.Serializer import *
from ItemMaster.Serializer import *

class TblLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TblLocation
        fields = ["id","name",]


class TblShopSerializer(serializers.ModelSerializer):

    city = TblLocationSerializer(many= False,read_only= True)
    super_manager = TblUserDetailsSerializer(many= False,read_only= True)
    managers = TblUserDetailsSerializer(many= True,read_only= False)
    items= TblItemSerializer(many= True,read_only= False)

    class Meta:
        model = TblShopDetails
        fields = ["id",
                  "shop_name",
                  "shop_address",
                  "city",
                  "super_manager",
                  "managers",
                  "items",
                  "is_approved",
                  "is_active"]