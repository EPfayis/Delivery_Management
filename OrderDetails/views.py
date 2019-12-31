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

def deliveryBoyCommitOnOrder(usr,action,order_id):

    try:
        if action != "C":
            return "Invalid Action Detected"

        if usr.UserType != "DB":
            return "Only Delivery Boy Can Commit With An Order"

        print("User validation completed")


        obj_tblorder = TblOrder.objects.get(id= order_id)
        obj_tblorder_temp = obj_tblorder


        if obj_tblorder.is_approved == False:
            return "This Order Is Not Approved"

        if obj_tblorder.delivery_boy_id != None:
            return "This Order Is Already Committed"

        print("Order validation completed")

        obj_tblorder.delivery_boy = usr
        obj_tblorder.save()

        print("DB Added To Order")

        return "1"

    except Exception as e:
        return str(e)

def approveOrRejectOrder(order_id,action,usr,description = ""):

    is_order_updated = False
    is_statusdetails_added = False
    is_statusdetails_saved = False

    try:
        usr_type = usr.UserType
        obj_userdetails = usr

        if usr_type != "MD":
            return "Only Manager Can Approve Or Reject The Order"
        if usr.is_approved == False:
            return "Your Account Is Not Approved"

        obj_tblorder = TblOrder.objects.get(id= order_id)
        obj_temp_order = obj_tblorder
        print("--> Order object created")

        print(obj_tblorder.delivery_boy)
        if obj_tblorder.delivery_boy != None:
            return "Delivery Boy Assigned. Can't Change The Approval"

        if action == "A":
            print("--> Action Detected")

            obj_tblorder.is_approved = True
            obj_tblorder.is_rejected = False
            obj_tblorder.approved_by = obj_userdetails
            obj_tblorder.save()
            is_order_updated = True
            print("--> Order updated")

            obj_tblstatusdetails = TblStatusDetails(date= datetime.now(),
                                                    description= description,
                                                    user= obj_userdetails,
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
            obj_tblorder.approved_by = obj_userdetails
            obj_tblorder.save()
            is_order_updated = True
            print("--> Order updated")

            obj_tblstatusdetails = TblStatusDetails(date=datetime.now(),
                                                    description= description,
                                                    user=obj_userdetails,
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

def addNewStatusToOrder(order_id,status_id,delivery_boy_id,description):

    is_status_det_saved = False
    is_status_det_added_to_order = False

    try:
        obj_user_det = TblUserDetails.objects.get(id= delivery_boy_id)
        obj_order = TblOrder.objects.get(id= order_id)
        obj_tblstatus = getSpecificStatus(status_id)

        if obj_order.is_approved == False:
            return "This Order Is Not Approved"
        if obj_order.is_delivered == True:
            return "This Order Is Delivered. Can't Add New Status"
        if obj_order.delivery_boy != obj_user_det:
            return "Only The Curresponding Delivery Boy Can Add New Status"

        obj_status_det = TblStatusDetails(date= datetime.now(),
                                          description= description,
                                          status= obj_tblstatus,
                                          user= obj_user_det)
        obj_status_det.save()
        is_status_det_saved = True

        obj_order.status.add(obj_status_det)
        is_status_det_added_to_order = True

        return "1"

    except Exception as e:

        if is_status_det_added_to_order == True:
            obj_order.status(obj_status_det).delete()

        if is_status_det_saved == True:
            obj_status_det.delete()

        return str(e)

def deliverTheOrder(order_id,usr_id,description):

    is_order_updated = False
    is_statusdetails_added = False
    is_statusdetails_saved = False

    try:
        obj_tblorder = TblOrder.objects.get(id= order_id)
        obj_temp_order = obj_tblorder
        del_boy = obj_tblorder.delivery_boy

        if obj_tblorder.is_approved == False:
            return "This Order Is Not Approved"

        if del_boy == None:
            return "No Delivery Boy Assigned For This Order"

        obj_usr_det = TblUserDetails.objects.get(id= usr_id)

        if del_boy != obj_usr_det:
            return "Only corresponding delivery boy can make an order delivered"

        obj_tblorder.is_delivered = True
        obj_tblorder.save()
        is_order_updated = True
        print("--> Order updated")

        obj_tblstatusdetails = TblStatusDetails(date=datetime.now(),
                                                description=description,
                                                user=del_boy,
                                                status=getSpecificStatus("4"))
        obj_tblstatusdetails.save()
        is_statusdetails_saved = True
        print("--> Status Details Saved")

        obj_tblorder.status.add(obj_tblstatusdetails)
        is_statusdetails_added = True
        print("--> Status Details Added To Order")

        return "1"


    except Exception as e:
        if is_statusdetails_added == True:
            obj_tblorder.status(obj_tblstatusdetails).remove()

        if is_statusdetails_saved == True:
            obj_tblstatusdetails.delete()

        if is_order_updated == True:
            obj_temp_order.save()

        return str(e)





class StatusManager(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    addDefaultStaus()

    def post(self,request):
        try:
            if self.request.user.is_superuser == False:
                return JsonResponse(getErrorDict("Validation Error Occured",
                                                 "You Don't Have The Permission To Add New Status"))

            stts = request.POST["StatusName"]
            obj_tblstatus = TblStatus(name= stts,is_public= True)
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

        if usr.UserType != "CR":
            return("Only Customer can make an order")
        if usr.is_approved == False:
            return "Your Account is Not Approved"
        if len(items) == 0:
            return("Cannot Accept The Order Without Item")
        return ("1")

    def post(self,request):

        is_order_saved = False
        is_status_details_saved = False
        is_Items_Added = False

        Received_items = []

        try:

            obj_user = self.request.user
            obj_userdetails = View_UserDetails.getUserDetails(obj_user)

            #Accepting the request
            #-------------------------

            date = datetime.now()
            customer = obj_userdetails
            delivery_boy = ""
            approved_by = ""
            Items = json.loads(request.POST["ItemList"])

            print("Request Accepted")

            # validating the Request
            #------------------------

            val = self.postValidate(obj_userdetails,list(Items))
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
                                                     user= customer,
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
            obj_user = self.request.user
            obj_userdetails = View_UserDetails.getUserDetails(obj_user)

            usr_type = obj_userdetails.UserType


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
            obj_user = request.user
            obj_userdetails = View_UserDetails.getUserDetails(obj_user)

            usr_type = obj_userdetails.UserType

            action = request.POST["Action"]
            order_id = request.POST["Oreder_Id"]
            dscrptn = request.POST["Description"]
            print("Request Accepted")

            msg = ""
            if action == "C":
                msg = deliveryBoyCommitOnOrder(obj_userdetails,action,order_id)
            elif action == "D":
                msg = deliverTheOrder(order_id,obj_userdetails.id,dscrptn)
            else:
                msg = approveOrRejectOrder(order_id,action,obj_userdetails,dscrptn)
            print("(Approval | Rejection | Commit) Performed")

            if msg == "1":
                if action == "D":
                    msg = "Order Delivered"
                elif action == "R":
                    msg = "Order rejected"
                elif action == "A":
                    msg = "Order Approved"
                else:
                    msg = "Successfully Commited With The Order"

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

    def put(self,request):
        try:

            obj_usr = self.request.user;
            obj_usr_det = View_UserDetails.getUserDetails(obj_usr)

            if obj_usr_det.UserType != "DB":
                return JsonResponse(getErrorDict("Validation Error Occured","Only Delivery Boy Can Add The Status"))

            order_id = request.POST["Order_ID"]
            status_id = request.POST["Status_ID"]
            description = request.POST["Description"]

            msg = addNewStatusToOrder(order_id,status_id,obj_usr_det.id,description)

            if msg != "1":
                return JsonResponse(getErrorDict("An Error Occured While Adding The Status",msg))


            return JsonResponse(getSuccessDict("Status Successfully Added To Order"))


        except Exception as  e:
            return JsonResponse(getErrorDict("An Error Occured While Adding The Status",str(e)))

    def delete(self,request):
        try:

            obj_user = self.request.user.id
            obj_userdetails = View_UserDetails.getUserDetails(obj_user)

            order_id = request.POST["Order_Id"]

            if getSpecificFieldOfOrder(order_id, "customer_id") != obj_userdetails.id:
                return JsonResponse(
                    {
                    "Message" : "Only The Ordered Customer can Delete The Order",
                    "Status" : False
                    }
                )


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

