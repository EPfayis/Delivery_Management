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
from OrderDetails import views as View_OrderDetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Login/',Viwe_Login.Login.as_view()),
    path('InserUser/',View_UserDetails.InsertUserDetails.as_view()),
    path('SaveItem/', View_ItemMaster.InsertItems.as_view()),
    path('SaveOrder/', View_OrderDetails.InsertOrder.as_view())

]
