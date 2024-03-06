from django.urls import path,include
from .views import RegisterViewSet,LoginViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'Users', RegisterViewSet, basename='Users-lists')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('',include(router.urls)),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]