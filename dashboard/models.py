from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)          # temperature, ph, niveau_eau…
    unit = models.CharField(max_length=20, blank=True)
    min_threshold = models.FloatField(null=True, blank=True)
    max_threshold = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="data")
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Actuator(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)          # pompe, led, nourrisseur…
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ActuatorLog(models.Model):
    actuator = models.ForeignKey(Actuator, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=10)  # "ON" or "OFF"
    timestamp = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="alerts")
    level = models.CharField(max_length=20, choices=[("warning","Warning"),("critical","Critical")])
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)