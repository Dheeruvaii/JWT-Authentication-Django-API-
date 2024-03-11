
# Create your views here.
from rest_framework import generics,status,views,permissions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserSerializer,CustomTokenObtainPairSerializer,LogoutSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.decorators import api_view
from .serializer import CookieSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.middleware import csrf


class RegisterViewSet(viewsets.ModelViewSet):
    queryset=UserData.objects.all()
    serializer_class=UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data={
            'message':" object created successfully",
            'data':serializer.data
        }
        return Response(response_data, status=201)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page=self.paginate_queryset(queryset)
        if page is not None:
            
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                 'message':"Users - lists",
                # 'message': "paginated tag-list",
                'data': serializer.data
            })
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': "Object retrieved successfully",
            'data': serializer.data
        })

    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': "Object updated successfully",
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response ({
             'message': "Object updated successfully"
    

        })
    



class LoginViewSet(ViewSet):
    """
    This class is for login and also sets the cookies in the user's browser
    """
    serializer_class = CustomTokenObtainPairSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = Response()
            data = serializer.data

            response.set_cookie(
                key='REFRESH_TOKEN',
                value=(data['refresh']),
                domain='.localhost.com',
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=False,
                httponly=True,
            )
            response.set_cookie(
                key='ACCESS_TOKEN',
                value=(data['access']),
                domain='.localhost.com',
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=False,
                httponly=True,
            )
            response['X-CSRFToken'] = csrf.get_token(request)
            response.data = {
                'status': 'successful',
                'data': data,
                'message': 'Login successful. Take token from cookies'
            }
            return response

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(viewsets.ViewSet):
    serializer_class=LogoutSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken(request.data.get('refresh_token'))
        # token.blacklist()
        return Response({'message': 'User logged out successfully'},status=status.HTTP_204_NO_CONTENT)

