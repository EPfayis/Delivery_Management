from .models import *
from General_Components.NameSpaces import *

class TblItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblItemMaster
        fields = ["name","rate","is_active"]