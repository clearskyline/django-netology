from django.shortcuts import get_object_or_404
from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SensorsView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class AddMeasurement(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorDataViewSet(ViewSet, RetrieveUpdateAPIView):
    serializer_class = SensorSerializer

    @staticmethod
    def retrieve_sensor(request, pk=None):
        queryset = Sensor.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = SensorDetailSerializer(instance)
        return Response(serializer.data)

    def update_sensor(self, request, pk=None):
        queryset = Sensor.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
