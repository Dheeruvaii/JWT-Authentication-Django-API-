from rest_framework import serializers
from .models import UserProfile
from auth_app.serializer import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    # user=UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user','first_name', 'last_name', 'phone_number', 'age', 'gender']

 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        authentication_data = {
            'id':instance.user.generated_uuid,
            'name': instance.user.name  ,
            'email': instance.user.email  ,
            'password': instance.user.password
        }
        representation['users']=authentication_data
        return representation