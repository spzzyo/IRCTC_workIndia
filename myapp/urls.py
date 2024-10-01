from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView, custom_user_login,admin_only_view, general_view


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/custom-login/', custom_user_login, name='custom_login'),
    path('api/admin-only/', admin_only_view, name='admin_only_view'), 
    path('api/general/', general_view, name='general_view'),
]
