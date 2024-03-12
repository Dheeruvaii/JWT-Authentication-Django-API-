from django.urls import path,include
from .views import RegisterViewSet,LoginAPIView,LogoutViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'Users', RegisterViewSet, basename='Users-lists')
# router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginAPIView.as_view(),name="login_view"),
    # path('logout/',LogoutAPIView.as_view(),name="logout_view")


    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]