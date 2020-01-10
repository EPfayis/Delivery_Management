from django.shortcuts import render
from .models import TblItemMaster
from General_Components.NameSpaces import *
from UserDetails import views as View_UserDetails
from ShopDetails.models import TblShopDetails
from ShopDetails import views as View_ShopDetails

# Create your views here.

class ItemsManager(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:

            obj_user = self.request.user
            obj_userdetails = View_UserDetails.getUserDetails(self.request.user.id)

            shop_id = request.POST["shop_id"]
            obj_shop = TblShopDetails.objects.get(id= shop_id)

            if View_ShopDetails.isManagerOfTheShop(obj_shop,obj_userdetails) == False:
                return JsonResponse({
                    getErrorDict("Validation Error Occured","You Are Not Recoganized As The Manager Of The Shop")
                })

            # if obj_userdetails.UserType != "MD":
            #     return JsonResponse({
            #         "Message": "Only Manager can Create The Items",
            #         "Status": False
            #     })

            print("User Veryfied as manager")

            if obj_userdetails.is_approved == False:
                return JsonResponse(getErrorDict("An Error Occured While Creating The Item",
                                                 "Your Account is Not Approved"))
            print("User approval Veryfied")

            name = request.POST["Item_Name"]
            rate =float(request.POST["Item_Rate"])

            _ItemMaster = TblItemMaster(name= name,
                                        rate= rate,
                                        is_active= True)
            _ItemMaster.save()
            obj_shop.items.add(_ItemMaster)

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

    def patch(self,request):
        try:
            obj_user = self.request.user
            obj_userdetails = View_UserDetails.getUserDetails(self.request.user.id)

            shop_id = request.POST["shop_id"]
            obj_shop = TblShopDetails.objects.get(id=shop_id)

            if View_ShopDetails.isManagerOfTheShop(obj_shop, obj_userdetails) == False:
                return JsonResponse({
                    getErrorDict("Validation Error Occured", "You Are Not Recoganized As The Manager Of The Shop")
                })

            item_id_list = request.POST["ItemId_list"]
            item_id_list = convertStringToListByComma(item_id_list)
            item_list =[]
            for i in item_id_list:
                item_list.append(TblItemMaster.objects.get(id= i))
            for i in item_list:
                if View_ShopDetails.isItemOfTheShop(obj_shop,i) == False:
                    return JsonResponse({
                        getErrorDict("Validation Error Occured", "Provided Items Are Not Recognized As The Items In Your Shop")
                    })

            action = request.POST["Action"]

            msg = []

            for i in item_list:
                if action == "A":
                    i.is_active = True
                    i.save()
                    msg.append("Successfully Activated The Item '" + str(i) + "'")
                elif action == "D":
                    i.is_active == False
                    i.save()
                    msg.append("Successfully Deactivated The Item '" + str(i) + "'")
                else:
                    return JsonResponse({
                        getErrorDict("Validation Error Occured","Invalid Action Detected")
                    })
            return JsonResponse({
                getSuccessDict(msg)
            })

        except Exception as e:
            return JsonResponse({getErrorDict("An Error Occured",str(e))})

def getSpecificField(itm_id,field):

    obj_itemmaster = TblItemMaster.objects.filter(id= itm_id)
    a = list(obj_itemmaster.values())
    return a[0][field]
