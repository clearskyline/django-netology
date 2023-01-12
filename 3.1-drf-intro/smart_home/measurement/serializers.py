from measurement.models import Sensor, Measurement
from rest_framework import serializers


class SensorSerializer(serializers.ModelSerializer):
    sensor_image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'sensor_image']


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'temperature', 'measure_date']


class SensorDetailSerializer(serializers.ModelSerializer):
    measure_sensor = MeasurementSerializer(read_only=True, many=True)
    sensor_image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'sensor_image', 'measure_sensor']
