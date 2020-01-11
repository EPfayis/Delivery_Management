from django.shortcuts import render
from General_Components.NameSpaces import *
from UserDetails import views as View_UserDetails
from ShopDetails import views as View_ShopDetails
from .models import *
from .Serializer import *

# Create your views here.

class LocationManager(ListAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TblLocationSerializer

    def post(self,request):
        try:

            obj_user = self.request.user
            obj_user_det = None
            is_anonymous = True

            if str(obj_user) != "AnonymousUser":
                is_anonymous = False


            if is_anonymous == True:
                return JsonResponse(getErrorDict("Validation Error Occured","You are not a super user"))
            else:
                if obj_user.is_superuser == False:
                    return JsonResponse(getErrorDict("Validation Error Occured", "You are not a super user"))

            location = request.POST["Location"]
            location = location.upper()

            if TblLocation.objects.filter(name= location).count() > 0:
                return JsonResponse(getErrorDict("Validation Error Occured","This Location Already Exist"))


            obj_tbllocaion = TblLocation(name= location)
            obj_tbllocaion.save()

            return JsonResponse(getSuccessDict("Successfully Added The Location"))

        except Exception as e:
            return JsonResponse(getErrorDict("An Error Occured", str(e)))

    def get_queryset(self):
        qs = TblLocation.objects.all()
        return qs

class ShopManager(ListAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TblShopSerializer

    def post(self,request):

        is_shop_created = False
        is_manager_added = False

        try:
            obj_usr = self.request.user

            obj_usr_det = None
            is_anonymous = True

            if str(obj_usr) != "AnonymousUser":
                is_anonymous = False

            if is_anonymous == True:
                return JsonResponse(getErrorDict("Validation Error Occured","Only Manager Can Create Shop"))

            obj_usr_det = View_UserDetails.getUserDetails(obj_usr)

            if obj_usr_det.UserType != "MD":
                return JsonResponse(getErrorDict("Validation Error Occured","Only Manager Can Create A Shop"))

            print("User Validation Completed")

            shop_name = request.POST["shop_name"]
            shop_address = request.POST["address"]
            city_id = request.POST["city_id"]

            obj_tbllocaton = TblLocation.objects.get(id= city_id)

            print("Request Accepted")

            obj_tblshop = TblShopDetails(shop_name= shop_name.upper(),
                                         shop_address= shop_address,
                                         city= obj_tbllocaton,
                                         super_manager= obj_usr_det,
                                         is_approved= False,
                                         is_active= False,)
            print("Shop object Created")

            obj_tblshop.save()
            is_shop_created = True

            print("Shop Details Saved")

            obj_tblshop.managers.add(obj_usr_det)
            is_manager_added = True

            print("Super Manager Added To Manager List")

            return JsonResponse(getSuccessDict("Successfully Added The Shop Details"))

        except Exception as e:
            if is_manager_added == True:
                obj_tblshop.managers(obj_usr_det).remove()

            if is_shop_created == True:
                obj_tblshop.delete()

            return JsonResponse(getErrorDict("An Error Occured",str(e)))

    def patch(self,request):
        try:
            obj_user = self.request.user

            if str(obj_user) == STR_ANONYMOUS_USER:
                return JsonResponse(getValErrorDict("Invalid User Detected"))


            shop_id = request.POST["Shop_Id"]
            action = request.POST["Action"]

            obj_shop = TblShopDetails.objects.get(id=shop_id)

            if obj_user.is_superuser == False:
                obj_userdetails = View_UserDetails.getUserDetails(self.request.user.id)

                if View_ShopDetails.isManagerOfTheShop(obj_shop, obj_userdetails) == False:
                    return JsonResponse({
                        getErrorDict("Validation Error Occured", "You Are Not Recoganized As The Manager Of The Shop")
                    })

                msg = ""
                if action == "A":
                    obj_shop.is_active = True
                    obj_shop.save()
                    msg = "Shop Activated"
                elif action == "D":
                    obj_shop.is_active =False
                    obj_shop.save()
                    msg = "Shop Deactivated"
                else:
                    return JsonResponse(
                        getErrorDict("Validation Error Occured","Invalid Action Detected")
                    )
                return JsonResponse(getSuccessDict(msg))
            else:
                msg = ""
                if action == "A":
                    obj_shop.is_approved = True
                    obj_shop.save()
                    msg = "Shop Approved"
                elif action == "D":
                    obj_shop.is_approved = False
                    obj_shop.save()
                    msg = "Shop Approval Canceled"
                else:
                    return JsonResponse(
                        getErrorDict("Validation Error Occured", "Invalid Action Detected")
                    )
                return JsonResponse(getSuccessDict(msg))

        except Exception as e:
            return JsonResponse(
                getErrorDict("An Error Occured", str(e))
            )

    def get_queryset(self):

        city = self.request.GET.get("city_id",'')
        qs = TblShopDetails.objects.all()

        if city and city != '':
            obj_city = TblLocation.objects.get(id=city)
            qs = TblShopDetails.objects.filter(city= obj_city)

        return qs


def isManagerOfTheShop(obj_shop,obj_user_det):
    return obj_shop.managers.filter(pk=obj_user_det.id).exists()

def isItemOfTheShop(obj_shop,obj_item):
    return obj_shop.items.filter(pk=obj_item.id).exists()