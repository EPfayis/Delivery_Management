from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from UserDetails import views as View_UserDetails

# Create your views here.
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        obj_usr_det = None
        user_type = ""
        if user.is_superuser == False:
            obj_usr_det = View_UserDetails.getUserDetails(user.id)
            user_type = obj_usr_det.UserType
        else:
            user_type = "Super_User"

        return Response({
            'Status': True,
            'Token': token.key,
            'user_type' : user_type,
        })
