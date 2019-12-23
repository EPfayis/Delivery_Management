from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from General_Components.NameSpaces import *
from OrderDetails.Serializer import TblOrderSerializer
from .models import *
from UserDetails.models import TblUserDetails
from UserDetails import views as View_UserDetails

# Create your views here.

def addDefaultStaus():

    st = [
        "Order Received", # with id 1
        "Order Approved",# with id 2
        "Order Rejected",# with id 3
        "Order Delivered",# with id 4
    ]

    qs = TblStatus.objects.all()
    if qs.count() == 0:
        for i in st:
            obj_tbl_status = TblStatus(name= i,is_public= False)
            obj_tbl_status.save()

def getSpecificStatus(id):
    addDefaultStaus()
    ob = TblStatus.objects.get(id= id)
    return ob

def deleteOrder(id):

    obj_tblorder = TblOrder.objects.get(id= id)

    items = []
    status = []

    for i in obj_tblorder.items.all():
        items.append(i)
    for i in obj_tblorder.status.all():
        status.append(i)

    obj_tblorder.delete()
    for i in items:
        i.delete()
    for i in status:
        i.delete()

def approveOrRejectOrder(order_id,action,usr):
    try:
        usr_type = View_UserDetails.getSpecificField(usr,"UserType",False)
        obj_user = User.objects.get(id= usr)

        if usr_type != "MD":
            return "Only Manager Can Approve Or Reject The Order"

        is_order_updated = False
        is_statusdetails_added = False
        is_statusdetails_saved = False



        obj_tblorder = TblOrder.objects.get(id= order_id)
        obj_temp_order = obj_tblorder
        print("--> Order object created")

        if action == "A":
            print("--> Action Detected")

            obj_tblorder.is_approved = True
            obj_tblorder.is_rejected = False
            obj_tblorder.approved_by = obj_user
            obj_tblorder.save()
            is_order_updated = True
            print("--> Order updated")

            obj_tblstatusdetails = TblStatusDetails(date= datetime.now(),
                                                    description= "Order is Approved",
                                                    user= obj_user,
                                                    status= getSpecificStatus("2"))
            obj_tblstatusdetails.save()
            is_statusdetails_saved = True
            print("--> Status Details Saved")

            obj_tblorder.status.add(obj_tblstatusdetails)
            is_statusdetails_added = True
            print("--> Status Details Added To Order")

            return "1"

        elif action == "R":
            print("--> Action Detected")

            obj_tblorder.is_approved = False
            obj_tblorder.is_rejected = True
            obj_tblorder.approved_by = obj_user
            obj_tblorder.save()
            is_order_updated = True
            print("--> Order updated")

            obj_tblstatusdetails = TblStatusDetails(date=datetime.now(),
                                                    description="Order is Rejected",
                                                    user=obj_user,
                                                    status=getSpecificStatus("3"))
            obj_tblstatusdetails.save()
            is_statusdetails_saved = True
            print("--> Status Details Saved")

            obj_tblorder.status.add(obj_tblstatusdetails)
            is_statusdetails_added = True
            print("--> Status Details Added To Order")

            return "1"

        else:
            print("--> Action Detection Failed")
            return "Provided Action Is Not Valid"

    except Exception as e:

        if is_statusdetails_added == True:
            obj_tblorder.status(obj_tblstatusdetails).remove()

        if is_statusdetails_saved == True:
            obj_tblstatusdetails.delete()

        if is_order_updated == True:
            obj_temp_order.save()

        return str(e)


def getSpecificFieldOfOrder(id,field):
    row = TblOrder.objects.filter(id= id)
    a = list(row.values())
    return a[0][field]


class StatusManager(APIView):

    addDefaultStaus()

    def post(self,request):
        try:
            stts = request.POST["Status Name"]
            obj_tblstatus = TblStatus(name= stts)
            obj_tblstatus.save()

            return JsonResponse({
                "Message" : "Successfully Saved The Status",
                "Status" : True
            })
        except Exception as e:
            return JsonResponse({
                "Message": "An Error Occured While The Status",
                "Error" : str(e),
                "Status": False
            })

    def get(self,request):
        addDefaultStaus()
        qs = TblStatus.objects.filter(is_public= True)
        return JsonResponse({
            "Status List" : list(qs.values())
        })

class OrderManager(ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = TblOrderSerializer

    def postValidate(self,usr,items = []):

        if View_UserDetails.getSpecificField(usr, "UserType", False) != "CR":
            return("Only Customer can make an order")
        if len(items) == 0:
            return("Cannot Accept The Order Without Item")
        return ("1")

    def post(self,request):

        is_order_saved = False
        is_status_details_saved = False
        is_Items_Added = False

        Received_items = []

        try:
            user_id = self.request.user.id

            #Accepting the request
            #-------------------------

            date = datetime.now()
            customer = User.objects.get(id= user_id)
            delivery_boy = ""
            approved_by = ""
            Items = json.loads(request.POST["ItemList"])

            print("Request Accepted")

            # validating the Request
            #------------------------

            val = self.postValidate(user_id,list(Items))
            if val != "1":
                return JsonResponse({
                    "Message" : "Request Validation Failed",
                    "Error" : val,
                    "Status" : False
                })

            print("Request Validated Successfully")

            Received_items.clear()
            net_amt = 0
            for i in Items:
                obj_itemmaster = TblItemMaster.objects.get(id=i["ItemId"])
                q = float(i["Qty"])
                rate = float(obj_itemmaster.rate)
                net_amt = net_amt + (q * rate)

                obj_itemdetails = TblItemDetails(item= obj_itemmaster,
                                                 qty= q,
                                                 rate= rate,
                                                 total_amt= q * rate)
                obj_itemdetails.save()

                Received_items.append(obj_itemdetails)


            print("Net Amount Calculated,Items Detailes Saved and stored in list")

            obj_tblorder = TblOrder(date= date,
                                    customer= customer,
                                    is_approved= False,
                                    is_delivered= False,
                                    is_rejected= False,
                                    total_amt= net_amt)
            obj_tblorder.save()
            is_order_saved = True

            print("TblOrder Saved")

            obj_tblstatus_datails = TblStatusDetails(date=date,
                                                     status=getSpecificStatus(1),
                                                     description="Waiting for the approval")
            obj_tblstatus_datails.save()
            is_status_details_saved = True
            print("Status Details Saved")

            obj_tblorder.status.add(obj_tblstatus_datails)
            print("Status Details Added To TblOrder")


            for i in Received_items:

                obj_tblorder.items.add(i)

            is_Items_Added = True
            print("All Items Are added to TblOrder")

            return JsonResponse({
                "Message" : "Succesfully Saved",
                "Status" : True
            })

        except Exception as e:

            if is_order_saved == True:
                obj_tblorder.delete()
            for i in Received_items:
                i.delete()
            if is_status_details_saved == True:
                obj_tblstatus_datails.delete()

            return JsonResponse({
                "Message": "An Error occured while saving the Order",
                "Error" : str(e),
                "Status": False
            })

    def get_queryset(self):
        try:
            usr = self.request.user.id
            usr_type = View_UserDetails.getSpecificField(usr,"UserType",False)

            approved = self.request.GET.get("Is_Approved", "")
            rejected = self.request.GET.get("Is_Rejected","")
            delivered = self.request.GET.get("Is_Delivered","")

            from_date =self.request.GET.get("From_Date","")
            to_date = self.request.GET.get("To_Date","")

            qs = None

            if from_date == "" and to_date == "":
                qs = TblOrder.objects.all()
            else:
                qs = TblOrder.objects.filter(date__range=(from_date,to_date))

            if usr_type == "MD":

                if approved != "":
                    qs.filter(is_approved= approved)
                if rejected != "":
                    qs.filter(is_rejected= rejected)
                if delivered != "":
                    qs.filter(is_delivered= delivered)

            return qs

        except Exception as e:
            pass


    def patch(self,request):
        try:
            usr = request.user.id
            usr_type = View_UserDetails.getSpecificField(usr, "UserType", False)

            action = request.POST["Action"]
            order_id = request.POST["Oreder_Id"]
            print("Request Accepted")

            msg = ""
            msg = approveOrRejectOrder(order_id,action,usr)
            print("Approval or Rejection Performed")

            if msg == "1":
                if action == "R":
                    msg = "Order rejected"
                else:
                    msg = "Order Approved"

                return JsonResponse({
                    "Message" : msg,
                    "Status" : True
                })
            else:
                return JsonResponse({
                    "Message": "An Error Occured",
                    "Error" : msg,
                    "Status": False
                })
        except Exception as e:
            return JsonResponse({
                "Message": "An Error Occured While Processing the request",
                "Error": str(e),
                "Status": False
            })

    def delete(self,request):
        try:

            usr_id = self.request.user.id
            order_id = request.POST["Order_Id"]

            if getSpecificFieldOfOrder(order_id, "customer_id") != usr_id:
                return JsonResponse({
                    "Message" : "Only The Ordered Customer can Delete The Order",
                    "Status" : False
                })


            deleteOrder(order_id)

            return JsonResponse({
                "Message": "Successfully Deleted",
                "Status": True
            })

        except Exception as e:
            return JsonResponse({
                "Message": "An Error Occured While Deleteing The Order",
                "Error" : str(e),
                "Status": False
            })

