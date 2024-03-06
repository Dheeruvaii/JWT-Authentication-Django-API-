from django.urls import path,include
from .views import RegisterViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'Users', RegisterViewSet, basename='Users-lists')





urlpatterns = [
    path('',include(router.urls))
]

# urlpatterns = [
#     path('api/register/', RegisterView.as_view(), name="sign_up"),
# ]