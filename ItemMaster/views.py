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

            obj_user = self.request.user
            obj_iserdetails = View_UserDetails.getUserDetails(self.request.user.id)
            #usr_id =View_UserDetails.getUserDetails(self.request.user.id).id

            if obj_iserdetails.UserType != "MD":
                return JsonResponse({
                    "Message": "Only Manager can Create The Items",
                    "Status": False
                })
            print("User Veryfied as manager")

            if obj_iserdetails.is_approved == False:
                return JsonResponse(getErrorDict("An Error Occured While Creating The Item",
                                                 "Your Account is Not Approved"))
            print("User approval Veryfied")

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
