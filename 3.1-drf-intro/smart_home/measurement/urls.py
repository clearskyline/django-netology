from django.urls import path
from measurement.views import SensorsView, SensorDataViewSet, AddMeasurement


urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', SensorDataViewSet.as_view({'get': 'retrieve_sensor', 'patch': 'update_sensor'})),
    path('measurements/', AddMeasurement.as_view())
]
