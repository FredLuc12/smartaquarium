from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Capteur, Mesure, Actionneur, Alerte
from django.shortcuts import get_object_or_404, redirect

@login_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès")
            return redirect("profile")  # 🔴 TRÈS IMPORTANT
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {"form": form})

@login_required
def capteur_view(request):
    """
    Vue purement front pour l’instant : on affiche juste la page capteurs.
    Le backend branchera plus tard la vraie liste via le contexte ou une API.
    """
    # pour l’instant on ne passe rien de spécial, le template gèrera l’état “vide”
    return render(request, "dashboard/sensors.html")

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")

def sensors_api(request):
    data = list(SensorData.objects.values().order_by("-created_at")[:10])
    return JsonResponse(data, safe=False)

from .models import Capteur

@login_required
def capteur_view(request):
    capteurs = Capteur.objects.all().order_by("nom")
    return render(request, "dashboard/sensors.html", {"capteurs": capteurs})

from .models import Alerte

@login_required
def dashboard_view(request):
    alertes = Alerte.objects.select_related("capteur").order_by("-horodatage")[:5]
    actionneurs = Actionneur.objects.all().order_by("nom")
    return render(
        request,
        "dashboard/dashboard.html",
        {"alertes": alertes, "actionneurs": actionneurs},
    )

@login_required
def toggle_actionneur_view(request, pk):
    if request.method != "POST":
        # On ne permet que le POST pour modifier l'état
        return redirect("dashboard")

    # 1) récupérer l’actionneur
    actionneur = get_object_or_404(Actionneur, pk=pk)

    # 2) inverser son état
    actionneur.etat = not actionneur.etat

    # 3) sauver
    actionneur.save()

    # 4) rediriger vers le dashboard (ou la page d’où vient la requête)
    return redirect("dashboard/settings")