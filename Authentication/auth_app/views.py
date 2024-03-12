
# Create your views here.
from rest_framework import generics,status,views,permissions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserSerializer,LogoutSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.middleware import csrf
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


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
    



        
class LogoutAPIView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract the refresh token from the validated data
                refresh_token = serializer.validated_data['refresh']
                
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({'message': 'Bad refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    """
        This class is for login and also set the cookies in user browser
        """
class LoginAPIView(APIView):
    
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get tokens from serializer data
        tokens = serializer.validated_data
        
        # Set cookies in the response
        response = Response({
            'message': "User Logged in Successfully",
            'data': serializer.data  # This line might not be necessary if you're not using serializer data elsewhere
        })
        response.set_cookie(
            key='REFRESH_TOKEN',
            value=tokens['refresh'],
            domain='.localhost.com',
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],  # Use refresh token lifetime here
            secure=False,
            httponly=True,
        )
        response.set_cookie(
            key='ACCESS_TOKEN',
            value=tokens['access'],
            domain='.localhost.com',
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=False,
            httponly=True,
        )
        return response

   
   
   """
   this methods for builtin customtokenobtain class 


   # class LoginAPIView(APIView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             tokens = serializer.validated_data
#             return Response({
#                 'message': 'Login successful',
#                 'tokens': tokens
#             }, status=status.HTTP_200_OK)
#         else:
#             # If serializer validation fails, return the errors
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   """