from django.db import models
import uuid
from auth_app.models import UserData


class UserProfile(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserData, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)
    generated_uuid = models.UUIDField(default=uuid.uuid4, editable=False) 
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


    def __str__(self):
        return self.first_name
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_user_email(self):
        return self.user.email

    def get_user_date_joined(self):
        return self.user.date_joined

    def get_user_is_admin(self):
        return self.user.is_admin