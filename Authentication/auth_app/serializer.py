from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserData
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user 
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            serializers.ValidationError({
                'status': 'failed',
                'message': 'Bad refresh token'
            })


class CookieSerializer(serializers.Serializer):
    ACCESS_TOKEN = serializers.CharField(required=False)
    REFRESH_TOKEN = serializers.CharField(required=False)

    def validate(self, attrs):
        access_token = attrs.get('ACCESS_TOKEN')
        refresh_token = attrs.get('REFRESH_TOKEN')
        
        if not (access_token and refresh_token):
            raise serializers.ValidationError("Access token and refresh token are required.")
        
        # Validate tokens if needed
        
        return attrs