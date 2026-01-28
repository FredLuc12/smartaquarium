from django.urls import path
from .views import capteur_view, dashboard_view, profile_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]
from django.urls import path
from .views import dashboard_view, sensors_api

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("api/sensors/", sensors_api, name="sensors_api"),
    path("profil/", profile_view, name="profile"),
    # path("parametre/", parametre_view, name="parametre"),
    path("capteur/", capteur_view, name="capteur"),
    # path("logout/", LogoutView.as_view(), name="logout"),
]
