"""Delivery_Mangement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Login import views as Viwe_Login
from UserDetails import views as View_UserDetails
from ItemMaster import views as View_ItemMaster
from OrderDetails import views as View_Order_Details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Login/',Viwe_Login.Login.as_view()),
    path('UserTypes/',View_UserDetails.GetUserTypes.as_view()),
    path('UserDetails/',View_UserDetails.UserDetails.as_view()),
    path('Item/', View_ItemMaster.ItemsManager.as_view()),
    path('Status/', View_Order_Details.StatusManager.as_view()),
    path('Order/', View_Order_Details.OrderManager.as_view()),
]
