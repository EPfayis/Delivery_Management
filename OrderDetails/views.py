from django.shortcuts import render
from General_Components.NameSpaces import *

from ItemMaster.models import TblItemMaster
from .models import TblItemDetails
from .models import TblStatus
from .models import TblOrder
import  json

# Create your views here.

class InsertOrder(APIView):
    def post(self,request):
        try:
            date = request.POST["Order_Date"]
            item_list =json.loads(request.POST["Items"])
            customer = request.POST["Customer"]
            delivery_boy = request.POST["Delivery_Boy"]
            _Tblstatus = TblStatus(date= date,status= "Order Received")
            is_delivered = False
            total_amt = float(0)

            print(item_list)

            _customer = User.objects.get(id= customer)
            _delivery_boy = User.objects.get(id= delivery_boy)

            #Calculating the Total Amount of items from request
            for i in item_list:
                total_amt = total_amt + float(i["rate"])
            print(total_amt)

            _TblOrder = TblOrder(order_date= date,
                                 customer= _customer,
                                 delivery_boy= _delivery_boy,
                                 is_delivered= is_delivered,
                                 total_amt= total_amt)
            _TblOrder.save()

        except Exception as e:
            return JsonResponse({
                "Message" : "An error Occured While Saving the Order",
                "Error" : str(e),
                "Status" : False
            })
        try:
            _Tblstatus.save()
            _TblOrder.status.add(_Tblstatus)

            for i in item_list:

                item_id = i["Item_Id"]
                rate = float(i["rate"])
                qty = float(i["Qty"])
                total = rate * qty
                _TblItemMaster =TblItemMaster.objects.get(id= item_id)

                _TblItemDetails = TblItemDetails(item_id= _TblItemMaster,
                                                 rate= rate,
                                                 qty= qty,
                                                 total= total)
                _TblItemDetails.save()
                _TblOrder.items.add(_TblItemDetails)

            return JsonResponse({
                "Message": "Successfully Saved",
                "Status": True
            })

        except Exception as e:

            # _TblOrder.delete()
            return JsonResponse({
                "Message" : "An Error Occured While Saving the Order Subs",
                "Error" : str(e),
                "Status" : False
            })


