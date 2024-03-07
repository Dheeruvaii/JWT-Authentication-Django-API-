
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserRegisterSerializer,CustomTokenObtainPairSerializer,UserProfileSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny ,IsAuthenticated
from django.db import IntegrityError

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserRegisterSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except IntegrityError:
    #         return Response({"error": "The name is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data={
            'message':" User Registerd successfully",
            'data':serializer.data
        }
        return Response(response_data, status=201)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page=self.paginate_queryset(queryset)
        if page is not None:
            
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                 'message':"User-Registerd-Lists",
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
    
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    def create(self,request):
            refresh_token=request.get(request)
            token=RefreshToken(refresh_token)
            token.blacklist()
            return token



# class LogoutViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['post'])
#     def logout(self, request):
#         refresh_token = request.data.get("refresh_token")
        
#         if not refresh_token:
#             return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
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
