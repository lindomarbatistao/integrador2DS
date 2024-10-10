from django.urls import path, include
from . import views
from app_smart.api.viewsets import CreateUserAPIViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app_smart.api.viewsets import CreateUserAPIViewSet
from rest_framework.routers import DefaultRouter
from .views import upload_csv_view, load_temperature_data, upload_csv_view_test
from app_smart.api.filters import SensorFilterView

from app_smart.api.viewsets import (
    CreateUserAPIViewSet,
    SensorViewSet,
    # TemperaturaDataViewSet
)


router = DefaultRouter()	
router.register(r'sensores', SensorViewSet)
# router.register(r'temperatura', load_temperature_data)

urlpatterns = [
 path('', views.abre_index, name='abre_index'),
 path('api/create_user/', CreateUserAPIViewSet.as_view(), name='create_user'),
 path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     
 path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 path('api/', include(router.urls)),
 path('api/upload_csv/', upload_csv_view, name='upload_csv'),
 path('api/test/', upload_csv_view_test, name='upload_csv'),
 path('api/sensor_filter/', SensorFilterView.as_view(), name='sensor_filter'),
 path('api/temperatura/', load_temperature_data, name='temperatura_data')
]



