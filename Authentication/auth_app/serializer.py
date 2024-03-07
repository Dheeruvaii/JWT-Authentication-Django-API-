from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserData,UserProfile


from rest_framework import serializers
from .models import UserData, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'age', 'gender')

class UserRegisterSerializer(serializers.ModelSerializer):
    
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = UserData
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = UserData.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(
                user=user,
                first_name=profile_data.get('first_name', ''),
                last_name=profile_data.get('last_name', ''),
                phone_number=profile_data.get('phone_number', ''),
                age=profile_data.get('age', 0),
                gender=profile_data.get('gender', '')
            )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data