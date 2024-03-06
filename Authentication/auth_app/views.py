
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *


# view for registering users

class RegisterViewSet(viewsets.ModelViewSet):
    queryset=UserData.objects.all()
    serializer_class=UserSerializer


    # def obtain_token_pair(self,request):
    #     view=TokenObtainPairView.as_view()
    #     response=view(request=request)
    #     return response
    
    # def refresh_token(self,request):
    #     refresh=request.data.get('refresh')
    #     if refresh:
    #         refresh_token=RefreshToken(request=request)
    #         token={'access':str(refresh_token.access_token)}
    #         return Response(token)
        
    #     else:
    #         return Response("token is required")
