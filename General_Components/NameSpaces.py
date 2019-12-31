from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
import json
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from General_Components.Logic_Collections import DynamicFieldsModelSerializer
from General_Components.Logic_Collections import ExtraFieldModelSerializer
from django.db.models import Q


def getErrorDict(message,error):
    d = {
        "Message" : message,
        "Error" : error,
        "Status" : False
    }
    return d
def getSuccessDict(message):
    d = {
        "Message" : message,
        "Status" : True
    }
    return d