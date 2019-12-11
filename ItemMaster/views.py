from django.shortcuts import render
from .models import TblItemMaster
from General_Components.NameSpaces import *

# Create your views here.

class InsertItems(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self,request):
        try:

            name = request.POST["Item_Name"]
            rate =float(request.POST["Item_Rate"])

            _ItemMaster = TblItemMaster(name= name,
                                        rate= rate)
            _ItemMaster.save()

            return JsonResponse({
                "Message": "Successfully Saved ",
                "Status": True
            })

        except Exception as e:
            return JsonResponse({
                "Message" : "An Error Occured While Saving the Item",
                "Error" : str(e),
                "Status" : False
            })