from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    sensor_image = models.ImageField(upload_to='Images', default='Images/None/sensor-img.jpg', blank=True, null=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measure_sensor')
    temperature = models.DecimalField(decimal_places=5, max_digits=20)
    measure_date = models.DateTimeField(auto_now_add=True)
