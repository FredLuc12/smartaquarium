# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .forms import ProfileForm
# from .models import SensorData


# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import SensorData
# from .forms import ProfileForm

# @login_required
# def dashboard_view(request):
#     return render(request, "dashboard/dashboard.html")

# @login_required
# def profile_view(request):
#     if request.method == "POST":
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profil mis à jour avec succès")
#             return redirect("profile")  # 🔴 TRÈS IMPORTANT
#     else:
#         form = ProfileForm(instance=request.user)

#     return render(request, "dashboard/profile.html", {"form": form})

# @login_required
# def capteur_view(request):
#     """
#     Vue purement front pour l’instant : on affiche juste la page capteurs.
#     Le backend branchera plus tard la vraie liste via le contexte ou une API.
#     """
#     # pour l’instant on ne passe rien de spécial, le template gèrera l’état “vide”
#     return render(request, "dashboard/sensors.html")

# @login_required
# def settings_view(request):
#     return render(request, "dashboard/settings.html")

# def sensors_api(request):
#     data = list(SensorData.objects.values().order_by("-created_at")[:10])
#     return JsonResponse(data, safe=False)

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import SensorData
import requests
import logging

# Logger pour debug
logger = logging.getLogger(__name__)

# URL de l'API (nom du service Docker)
API_URL = "http://smartaquarium-api:8000"


@login_required
def dashboard_view(request):
    """
    Dashboard principal avec données de l'API FastAPI
    """
    context = {
        'capteurs': [],
        'alertes': [],
        'actionneurs': [],
        'mesures_recentes': [],
        'api_error': None
    }
    
    try:
        # Récupère les capteurs
        capteurs_response = requests.get(f"{API_URL}/api/capteurs/", timeout=5)
        if capteurs_response.status_code == 200:
            context['capteurs'] = capteurs_response.json()
        
        # Récupère les alertes actives
        alertes_response = requests.get(f"{API_URL}/api/alertes/active", timeout=5)
        if alertes_response.status_code == 200:
            context['alertes'] = alertes_response.json()
        
        # Récupère les actionneurs
        actionneurs_response = requests.get(f"{API_URL}/api/actionneurs/", timeout=5)
        if actionneurs_response.status_code == 200:
            context['actionneurs'] = actionneurs_response.json()
        
        # Récupère les mesures récentes (toutes ou par capteur)
        mesures_response = requests.get(f"{API_URL}/api/mesures/", timeout=5)
        if mesures_response.status_code == 200:
            context['mesures_recentes'] = mesures_response.json()[:10]  # 10 dernières
            
    except requests.exceptions.ConnectionError:
        logger.error("Impossible de se connecter à l'API")
        context['api_error'] = "L'API backend n'est pas accessible"
    except requests.exceptions.Timeout:
        logger.error("Timeout lors de la connexion à l'API")
        context['api_error'] = "L'API backend ne répond pas"
    except Exception as e:
        logger.error(f"Erreur API: {e}")
        context['api_error'] = f"Erreur: {str(e)}"
    
    return render(request, "dashboard/dashboard.html", context)


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {"form": form})


@login_required
def capteur_view(request):
    """
    Vue page capteurs avec données API
    """
    context = {
        'capteurs': [],
        'api_error': None
    }
    
    try:
        # Récupère tous les capteurs avec leurs dernières mesures
        capteurs_response = requests.get(f"{API_URL}/api/capteurs/", timeout=5)
        if capteurs_response.status_code == 200:
            capteurs = capteurs_response.json()
            
            # Pour chaque capteur, récupère sa dernière mesure
            for capteur in capteurs:
                try:
                    mesure_response = requests.get(
                        f"{API_URL}/api/mesures/capteur/{capteur['id']}/latest", 
                        timeout=3
                    )
                    if mesure_response.status_code == 200:
                        capteur['derniere_mesure'] = mesure_response.json()
                except:
                    capteur['derniere_mesure'] = None
            
            context['capteurs'] = capteurs
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des capteurs: {e}")
        context['api_error'] = "Impossible de charger les capteurs"
    
    return render(request, "dashboard/sensors.html", context)


@login_required
def settings_view(request):
    context = {
        'actionneurs': [],
        'api_error': None
    }
    
    try:
        actionneurs_response = requests.get(f"{API_URL}/api/actionneurs/", timeout=5)
        if actionneurs_response.status_code == 200:
            context['actionneurs'] = actionneurs_response.json()
    except Exception as e:
        logger.error(f"Erreur settings: {e}")
        context['api_error'] = "Impossible de charger les actionneurs"
    
    return render(request, "dashboard/settings.html", context)



@login_required
def sensors_api(request):
    """
    API JSON pour récupérer les données des capteurs
    (utilisé pour les updates JavaScript en temps réel)
    """
    try:
        # Appel à l'API FastAPI
        response = requests.get(f"{API_URL}/api/capteurs/", timeout=5)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({'error': 'API error'}, status=500)
    except Exception as e:
        logger.error(f"Erreur sensors_api: {e}")
        return JsonResponse({'error': str(e)}, status=500)
