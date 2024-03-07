from rest_framework import serializers
from .models import UserProfile
from auth_app.serializer import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    # user=UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'age', 'gender']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = instance.user  # Access the related UserData instance
        representation['email'] = user_data.email
        representation['name'] = user_data.name
        representation['password'] = user_data.password  # Note: This might not be ideal to expose in the response
        # Add more user fields as needed
        return representation