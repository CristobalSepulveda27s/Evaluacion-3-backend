from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from productos.views import ProductoViewSet, CustomTokenObtainPairView, RegisterView, ProfileView
from .views import home  # Importa la vista home

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/', include(router.urls)),
]