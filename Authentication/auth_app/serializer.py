from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserData

# class UserProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name', 'phone_number', 'age', 'gender')

class UserRegisterSerializer(serializers.ModelSerializer):
    
    # profile = UserProfileSerializer(required=False)

    class Meta:
        model = UserData
        fields = ['email','password']
        # fields = ('email', 'password', 'profile')
        # extra_kwargs = {'password': {'write_only': True}}

    
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = UserData.objects.create(**validated_data)
    #     UserProfile.objects.create(user=user, **profile_data)
    #     return user
    
   


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data