from django.urls import path
from .views import dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]
from django.urls import path
from .views import dashboard_view, sensors_api

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("api/sensors/", sensors_api, name="sensors_api"),
]
