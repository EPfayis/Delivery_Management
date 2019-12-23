from General_Components.NameSpaces import *
from .models import *

from UserDetails.Serializer import TblUserDetailsSerializer

class TblItemDetailsSerializer(serializers.ModelSerializer):

    item = serializers.StringRelatedField(many= False,read_only= True)

    class Meta:
        model = TblItemDetails
        fields = ["item","rate","qty","total_amt"]


class TblOrderSerializer(serializers.ModelSerializer):
    items = TblItemDetailsSerializer(many= True, read_only= True)
    #delivery_boy = serializers.PrimaryKeyRelatedField(many= False, read_only= True)
    # customer = TblUserDetailsSerializer(many= False,read_only= True)
    # approved_by = TblUserDetailsSerializer(many= False,read_only= True)

    class Meta:
        model = TblOrder
        fields = ["id",
                  "date",
                  "total_amt",
                  "is_delivered",
                  "is_approved",
                  "is_rejected",
                  "items",]

                  # "customer",
                  # "approved_by"]