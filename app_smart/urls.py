from django.urls import path, include
from . import views
from app_smart.api.viewsets import CreateUserAPIViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app_smart.api.viewsets import CreateUserAPIViewSet, SensorViewSet
from rest_framework.routers import DefaultRouter
from .views import upload_csv_view

router = DefaultRouter()	
router.register(r'sensores', SensorViewSet)

urlpatterns = [
 path('', views.abre_index, name='abre_index'),
 path('api/create_user/', CreateUserAPIViewSet.as_view(), name='create_user'),
 path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     
 path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 path('api/', include(router.urls)),
 path('api/upload_csv/', upload_csv_view, name='upload_csv'),
]



