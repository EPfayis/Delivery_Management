from General_Components.NameSpaces import *
from .models import TblUserDetails

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]

class TblUserDetailsSerializer(serializers.ModelSerializer):

    UserId = UserSerializer(many=False, read_only=True)
    class Meta:
        model = TblUserDetails
        fields = ["UserId","Address","Mobile"]