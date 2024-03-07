from django.urls import path,include
from .views import UserProfileViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('',include(router.urls)),

]