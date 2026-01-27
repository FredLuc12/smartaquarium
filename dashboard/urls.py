from django.urls import path
from .views import capteur_view, dashboard_view, profile_view, toggle_actionneur_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]
from django.urls import path
from .views import dashboard_view, sensors_api
from .views import profile_view, capteur_view, toggle_actionneur_view, settings_view


# app_name = "dashboard"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("api/sensors/", sensors_api, name="sensors_api"),
    path("profil/", profile_view, name="profile"),
    path("parametre/", settings_view, name="settings"),
    path("capteur/", capteur_view, name="capteur"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path("actionneurs/<int:pk>/toggle/", toggle_actionneur_view, name="actionneur_toggle")
]
