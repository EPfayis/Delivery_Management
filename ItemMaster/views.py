from django.shortcuts import render
from .models import TblItemMaster
from General_Components.NameSpaces import *
from UserDetails import views as View_UserDetails

# Create your views here.

class ItemsManager(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:

            usr_id = self.request.user.id

            if View_UserDetails.getSpecificField(usr_id,"UserType",False) != "MD":
                return JsonResponse({
                    "Message": "Only Manager can Create The Items",
                    "Status": False
                })
            print("User Veryfied")

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


def getSpecificField(itm_id,field):

    obj_itemmaster = TblItemMaster.objects.filter(id= itm_id)
    a = list(obj_itemmaster.values())
    return a[0][field]
