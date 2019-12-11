from django.shortcuts import render
from General_Components.NameSpaces import *
from .models import TblUserDetails
from General_Components.Logic_Collections import *


# Create your views here.

class InsertUserDetails(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:
            print(self.request.user.id)
            
            if Logic_UserDetails.ClsUserDetails.getSpecificField(self.request.user.id,"is_superuser") == False:

                return JsonResponse({
                    "Message" : "Only super user can create other users",
                    "Status" : False
                })

            Name = request.POST["Name"]
            UserName = request.POST["User_Name"]
            UserType = request.POST["User_Type"]
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



