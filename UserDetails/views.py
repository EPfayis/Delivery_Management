from django.shortcuts import render
from rest_framework.permissions import AllowAny

from General_Components.NameSpaces import *
from .models import TblUserDetails
from General_Components.Logic_Collections import *
from UserDetails.Serializer import TblUserDetailsSerializer
from django.db.models import Q
from ShopDetails.models import *
from ShopDetails import views as View_ShopDetails

# Create your views here.

user_types = ["CR","DB","MD","SMD"]

class GetUserTypes(APIView):
    def get(self,request):
        return JsonResponse({
            "User_Type": user_types
        })

class UserDetails(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TblUserDetailsSerializer

    def post(self,request):
        try:

            Name = request.POST["Name"]
            UserName = request.POST["User_Name"]
            UserType = request.POST["User_Type"]
            shop_id = ""
            obj_shop = None

            if UserType not in user_types:
                return JsonResponse({
                    "Message": "An error occured while saving the user",
                    "Error": "Invalid UserType",
                    "Status": False
                })
            if UserType == "SMD":
                if str(self.request.user) == "AnonymousUser" or self.request.user.is_superuser == False:
                    return JsonResponse({
                        "Message" : "You Don't Have The The Permission To Create Sub Manager",
                        "Status" : False
                    })
                obj_usr_det = getUserDetails(self.request.user)

                if obj_usr_det.UserType != "MD":
                    return JsonResponse(getErrorDict("Validation Error Occured","You Don't Have The The Permission To Create Sub Manager"))

                shop_id = request.POST["shop_id"]
                obj_shop = TblShopDetails.objects.get(id= shop_id)

                if obj_shop.super_manager != obj_usr_det:
                    return JsonResponse({
                        getErrorDict("Validation Error Occured","You Are Not The Super Manager Of This Shop")
                    })

            Pwd =make_password(request.POST["Password"])
            Email = request.POST.get("Email","")
            Address = request.POST["Address"]
            Mob = request.POST["Mobile"]

            is_approved = False
            if UserType == "CR" or UserType == "SMD":
                is_approved = True
            else:
                is_approved = False

            _Tbl_User = User(first_name= Name,
                            is_superuser= 0,
                            username= UserName,
                            password= Pwd,
                            email= Email,
                            is_staff= 1,
                            is_active= 1
                            )
            _Tbl_User.save()

            _TblUserDetails = TblUserDetails(user= _Tbl_User,
                                             UserType= UserType,
                                             Address= Address,
                                             Mobile= Mob,
                                             is_approved= is_approved,
                                             )
            _TblUserDetails.save()

            if UserType == "SMD":

                obj_shop.managers.add(obj_usr_det)

                return JsonResponse({
                    getSuccessDict("Successfully Added The Sub Manager")
                })

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

    def get_queryset(self):
        try:
            usr_typs =self.request.GET.get("User_Types","")
            is_approved = self.request.GET.get("Is_Approved","")
            search_text = self.request.GET.get("Search_Text","")
            print(self.request.get_host())
            if usr_typs == "":
                usr_typs = []
            else:
                usr_typs = usr_typs.split(",")

            qs = None

            if len(usr_typs) == 0 and is_approved == "":
                print("No Aprv No Type")
                qs = TblUserDetails.objects.all()
            elif len(usr_typs) != 0 and is_approved != "":
                print("Aprv Type")
                qs = TblUserDetails.objects.filter(UserType__in = usr_typs,is_approved= is_approved)
            else:
                if len(usr_typs) != 0:
                    print("No Aprv Type")
                    qs = TblUserDetails.objects.filter(UserType__in= usr_typs)
                else:
                    print("Aprv No Type")
                    qs = TblUserDetails.objects.filter(is_approved= is_approved)



            qs = qs.filter(Q(Mobile__contains= search_text)|
                           Q(user__in= User.objects.filter(Q(first_name__contains= search_text)|
                                                         Q(email__contains= search_text)|
                                                         Q(username__contains = search_text)
                                                        )
                            )
                          )

            return qs

        except Exception as e:
            return JsonResponse(
                {
                    "Message" : "An Error Occured While Processing the Request",
                    "Error" : str(e),
                    "Status": False
                }
            )

    def patch(self,request):
        try:
            if str(self.request.user) == "AnonymousUser":
                return JsonResponse({
                    "Message" : "You Don't Have The Permission To Approve The Users",
                    "Status" : False
                })

            obj_user = self.request.user
            obj_user_det = None

            action = request.POST["action"]
            r_usr = request.POST["user_id"]

            obj_r_user = TblUserDetails.objects.get(id= r_usr)

            if obj_user.is_superuser == True:
            # super user can't approve the sub manager account
                if obj_r_user.UserType == "SMD":
                    return JsonResponse(getErrorDict("Validation Error Occured",
                                                     "You Don't Have The Permission To Approve This User"))

            else:
            # if non super_user approves an account,some more validations required
                obj_user_det = getUserDetails(obj_user)

                if obj_user_det.UserType != "MD" or obj_r_user.UserType != "SMD":
                # Manager can approve only sub manager account
                    return JsonResponse(getErrorDict("Validation Error Occured",
                                                     "You Don't Have The Permission To Approve This User"))
                else:
                # if a manager going to approve a sub manager account
                    shop_id = request.POST["shop_id"]
                    obj_shop = TblShopDetails.objects.get(id= shop_id)

                    if obj_shop.super_manager != obj_user_det:
                    # The approving person should be the owner of the shop
                        return JsonResponse(getErrorDict("Validation Error Occured",
                                                         "You Are Not Recognized As The Owner Of This Shop"))
                    if View_ShopDetails.isManagerOfTheShop(obj_shop,obj_r_user) == False:
                    # the sub manager should be in his shop
                        return JsonResponse(getErrorDict("Validation Error Occured",
                                                         "This Account Is Not Recognized As The Sub Manager Of Your Shop"))


            if action == "A":
                obj_r_user.is_approved = True
                obj_r_user.save()
            elif action == "R":
                obj_r_user.is_approved = False
                obj_r_user.save()
            else:
                return JsonResponse(
                    {
                    "Message": "An Error Occured While Changing the Approval",
                    "Error" : "Invalid action Detected",
                    "Status": False
                    }
                )

            return JsonResponse(
                {
                    "Message": "Successfully Changed the Approval",
                    "Status": True
                }
            )

        except Exception as e:
            return JsonResponse(
                {
                    "Message": "An Error Occured",
                    "Error": str(e),
                    "Status": False
                }
            )


def getUserDetails(usr):
    if type(usr) == str:
        return TblUserDetails.objects.get(user_id= usr)
    elif type(usr) == User:
        return TblUserDetails.objects.get(user= usr)
    elif type(usr) == int:
        return TblUserDetails.objects.get(user_id= usr)
    else:
        return None

def getSpecificField(Usr_details_Id, Field,is_in_parent):

    obj_userdetails = TblUserDetails.objects.filter(id= Usr_details_Id)

    a = []
    if is_in_parent == False:
        a = list(obj_userdetails.values())
        return (a[0][Field])
    else:
        a = obj_userdetails.first().user.__dict__
        return a[Field]



