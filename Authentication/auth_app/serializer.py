from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserData
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib import auth
from .utils import generate_token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    refresh = serializers.CharField(read_only =True)
    access = serializers.CharField(read_only =True)

    class Meta:
        model = UserData
        fields = ['email', 'password', 'refresh', 'access']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email = email, password = password)
        try:
            user_data = UserData.objects.get(email=email)
            # print(user_data.id)
            # org_id = O

        except:
            raise serializers.ValidationError({'status': 'failed', 'message': 'enter valid email'})
        if not user_data.is_active:
            raise AuthenticationFailed({'status': 'failed', 'message': 'Account is not active.'})
        if not user:
            raise AuthenticationFailed({'status': 'failed', 'message': 'Invalid credentials, Try Again.'})

        tokens = generate_token(user)
        refresh_token = tokens['refresh']
        access_token = tokens['access']
        
        return {
            'email': user.email,
            'refresh': refresh_token,
            'access': access_token
            }

    

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         return token

#     def validate(self, attrs):
#         # Check if 'email' is in the request data
#         email = attrs.get('email')
#         if not email:
#             raise serializers.ValidationError("Email is required.")
#         data = super().validate(attrs)
#         return data
    

# class LogoutSerializer(serializers.Serializer):
#     refresh_token = serializers.CharField(required=True)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token)
        except TokenError:
            serializers.ValidationError({
                'status': 'failed',
                'message': 'Bad refresh token'
            })




