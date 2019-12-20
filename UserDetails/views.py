from django.shortcuts import render
from General_Components.NameSpaces import *
from .models import TblUserDetails
from General_Components.Logic_Collections import *


# Create your views here.

user_types = ["CR","DB","MD"]

class GetUserTypes(APIView):
    def get(self,request):
        return JsonResponse({
            "User_Type": user_types
        })

class InsertUserDetails(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:
            print(self.request.user.id)
            
            if getSpecificField(self.request.user.id,"is_superuser",True) == False:

                return JsonResponse({
                    "Message" : "Only super user can create other users",
                    "Status" : False
                })

            Name = request.POST["Name"]
            UserName = request.POST["User_Name"]
            UserType = request.POST["User_Type"]
            if UserType not in user_types:
                return JsonResponse({
                    "Message": "An error occured while saving the user",
                    "Error": "Invalid UserType",
                    "Status": False
                })
            Pwd =make_password(request.POST["PassWord"])
            Email = request.POST.get("Email","")
            Address = request.POST["Address"]
            Mob = request.POST["Mobile"]

            _Tbl_User = User(first_name= Name,
                            is_superuser= 0,
                            username= UserName,
                            password= Pwd,
                            email= Email,
                            is_staff= 1,
                            is_active= 1
                            )
            _Tbl_User.save()

            _TblUserDetails = TblUserDetails(UserId= _Tbl_User,
                                             UserType= UserType,
                                             Address= Address,
                                             Mobile= Mob
                                             )
            _TblUserDetails.save()

            return JsonResponse({
                "Message": "Successfully Saved the user",
                "Status": True
            })

        except  Exception as e:
            return JsonResponse({
                "Message" : "An error occured while saving the user",
                "Error" : str(e),
                "Status" : False
            })

def getSpecificField(UsrId, Field,is_in_parent):
    if is_in_parent == True:
        Usr = User.objects.filter(id=UsrId)
        a = list(Usr.values())
        return (a[0][Field])
    else:
        obj_userdetails = TblUserDetails.objects.filter(UserId_id= UsrId)
        a = list(obj_userdetails.values())
        return (a[0][Field])

